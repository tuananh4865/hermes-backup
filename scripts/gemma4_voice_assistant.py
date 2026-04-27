#!/usr/bin/env python3
"""
gemma4 Voice Assistant - Voice input → gemma4:e2b transcript → VieNeu-TTS response
Requirements:
  - pip install ollama
  - pip install pygame (for audio playback)
  - ollama pull gemma4:e2b
  - VieNeu-TTS installed
"""

import ollama
import base64
import os
import sys
import tempfile
import argparse

# Audio recording
try:
    import pyaudio
    import wave
    HAS_PYAUDIO = True
except ImportError:
    HAS_PYAUDIO = False
    print("⚠️ pyaudio not installed. Run: pip install pyaudio")

# TTS
try:
    from vieneu import Vieneu
    HAS_VIENEU = True
except ImportError:
    HAS_VIENEU = False
    print("⚠️ vieneu not installed. Run: pip install vieneu")

# Audio playback
try:
    import pygame
    pygame.mixer.init()
    HAS_PYGAME = True
except ImportError:
    HAS_PYGAME = False
    print("⚠️ pygame not installed. Run: pip install pygame")


def record_audio(duration=5, sample_rate=16000, channels=1):
    """Record audio from microphone."""
    if not HAS_PYAUDIO:
        raise RuntimeError("pyaudio required for recording")
    
    p = pyaudio.PyAudio()
    stream = p.open(
        format=pyaudio.paInt16,
        channels=channels,
        rate=sample_rate,
        input=True,
        frames_per_buffer=1024
    )
    
    print(f"🎙️ Recording ({duration}s)...")
    frames = []
    for _ in range(int(sample_rate / 1024 * duration)):
        data = stream.read(1024)
        frames.append(data)
    
    stream.stop_stream()
    stream.close()
    p.terminate()
    
    # Save to temp file
    temp_file = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
    wf = wave.open(temp_file.name, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    wf.setframerate(sample_rate)
    wf.writeframes(b''.join(frames))
    wf.close()
    
    return temp_file.name


def encode_audio(audio_path):
    """Encode audio file to base64."""
    with open(audio_path, 'rb') as f:
        return base64.b64encode(f.read()).decode('utf-8')


def transcribe_with_gemma4(audio_path):
    """Transcribe audio using gemma4:e2b."""
    # Read audio file
    with open(audio_path, 'rb') as f:
        audio_data = f.read()
    
    # Encode to base64 for Ollama
    audio_b64 = base64.b64encode(audio_data).decode('utf-8')
    
    # Build message with inline audio
    # Ollama supports audio via base64 data URI
    response = ollama.chat(
        model='gemma4:e2b',
        messages=[{
            'role': 'user',
            'content': f'<audio data="audio/wav;base64,{audio_b64}"/>\nPlease transcribe exactly what is spoken in this audio file.'
        }]
    )
    
    return response['message']['content']


def chat_with_gemma4(prompt, audio_path=None):
    """Chat with gemma4:e2b, optionally with audio context."""
    messages = [{'role': 'user', 'content': prompt}]
    
    if audio_path:
        with open(audio_path, 'rb') as f:
            audio_data = f.read()
        audio_b64 = base64.b64encode(audio_data).decode('utf-8')
        messages[0]['content'] = f'<audio data="audio/wav;base64,{audio_b64}"/>\n{prompt}'
    
    response = ollama.chat(
        model='gemma4:e2b',
        messages=messages
    )
    
    return response['message']['content']


def speak_text(text, voice_id=None):
    """Speak text using VieNeu-TTS."""
    if not HAS_VIENEU:
        print("⚠️ VieNeu-TTS not available. Text:", text[:100])
        return None
    
    tts = Vieneu()
    audio = tts.infer(text=text)
    
    temp_file = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
    tts.save(audio, temp_file.name)
    
    if HAS_PYGAME:
        pygame.mixer.music.load(temp_file.name)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    
    return temp_file.name


def voice_assistant_loop():
    """Main voice assistant loop."""
    print("=" * 50)
    print("🎙️ gemma4 Voice Assistant")
    print("=" * 50)
    print("Commands:")
    print("  record - Hold to record voice (then release to send)")
    print("  transcribe <file> - Transcribe audio file")
    print("  chat <text> - Chat with gemma4")
    print("  speak <text> - Speak text with VieNeu-TTS")
    print("  quit - Exit")
    print()
    
    while True:
        try:
            cmd = input("🎤 Command (or just speak): ").strip()
            
            if cmd == 'quit':
                break
            
            elif cmd == 'record':
                # Record audio
                audio_file = record_audio(duration=5)
                print(f"📁 Recorded to: {audio_file}")
                
                # Transcribe
                print("🔄 Transcribing with gemma4:e2b...")
                transcript = transcribe_with_gemma4(audio_file)
                print(f"📝 Transcript: {transcript}")
                
                # Chat response
                print("💬 Getting gemma4 response...")
                response = chat_with_gemma4(transcript, audio_path=audio_file)
                print(f"🤖 Response: {response}")
                
                # Speak response
                if response:
                    print("🔊 Speaking response...")
                    speak_text(response)
                
                # Cleanup
                os.unlink(audio_file)
            
            elif cmd.startswith('transcribe '):
                audio_file = cmd.split(' ', 1)[1]
                if os.path.exists(audio_file):
                    transcript = transcribe_with_gemma4(audio_file)
                    print(f"📝 Transcript: {transcript}")
                else:
                    print(f"❌ File not found: {audio_file}")
            
            elif cmd.startswith('chat '):
                text = cmd.split(' ', 1)[1]
                response = chat_with_gemma4(text)
                print(f"🤖 Response: {response}")
            
            elif cmd.startswith('speak '):
                text = cmd.split(' ', 1)[1]
                speak_text(text)
            
            else:
                # Treat as voice input
                if cmd:
                    print("💬 Sending to gemma4...")
                    response = chat_with_gemma4(cmd)
                    print(f"🤖 Response: {response}")
        
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")


def transcribe_file(audio_path):
    """Transcribe a single audio file."""
    if not os.path.exists(audio_path):
        print(f"❌ File not found: {audio_path}")
        return
    
    print(f"🎙️ Transcribing: {audio_path}")
    transcript = transcribe_with_gemma4(audio_path)
    print(f"\n📝 Transcript:\n{transcript}")
    
    # Save to file
    output_path = audio_path + '.txt'
    with open(output_path, 'w') as f:
        f.write(transcript)
    print(f"💾 Saved to: {output_path}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='gemma4 Voice Assistant')
    parser.add_argument('command', nargs='?', default=None,
                        help='Command: record, transcribe <file>, chat <text>, speak <text>')
    parser.add_argument('args', nargs='*', help='Arguments for command')
    
    args = parser.parse_args()
    
    if args.command == 'transcribe' and args.args:
        transcribe_file(args.args[0])
    else:
        voice_assistant_loop()
