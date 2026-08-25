#!/usr/bin/env python3
"""
Voice Assistant - STT → TTS Pipeline (không có LLM)
Dùng cho transcription và voice synthesis trực tiếp.

Usage:
    python3 voice_assistant.py transcribe audio.wav     # Transcribe audio
    python3 voice_assistant.py speak "text"            # Speak text
    python3 voice_assistant.py voices                   # List voices
"""

import os
import sys
import tempfile
import subprocess
import argparse

# STT - Faster Whisper
from faster_whisper import WhisperModel

# TTS - VieNeu
try:
    from vieneu import Vieneu
    HAS_VIENEU = True
except ImportError:
    HAS_VIENEU = False
    print("Warning: VieNeu-TTS not installed (pip install vieneu)")


class VoiceAssistant:
    """Voice Assistant - STT + TTS only (no LLM)"""
    
    def __init__(self, stt_model="small", device="cpu", tts_voice=None):
        """
        Initialize Voice Assistant.
        
        Args:
            stt_model: faster-whisper model size (tiny/base/small/medium/large-v3)
            device: STT device (cpu/cuda/mps)
            tts_voice: VieNeu voice name (default: Xuân Vĩnh)
        """
        # STT Model
        print(f"Loading faster-whisper ({stt_model}, {device})...")
        self.stt = WhisperModel(stt_model, device=device)
        
        # TTS
        if HAS_VIENEU:
            print("Loading VieNeu-TTS...")
            self.tts = Vieneu()
            self.voices = dict(self.tts.list_preset_voices())
            print(f"Available voices: {list(self.voices.keys())}")
            
            # Set default voice
            if tts_voice and tts_voice in self.voices:
                self.current_voice = self.tts.get_preset_voice(tts_voice)
                self.current_voice_name = tts_voice
            else:
                # Default: Xuân Vĩnh (Nam - Miền Nam)
                default = "Xuân Vĩnh (Nam - Miền Nam)"
                if default in self.voices:
                    self.current_voice = self.tts.get_preset_voice(default)
                    self.current_voice_name = default
                else:
                    first = list(self.voices.keys())[0]
                    self.current_voice = self.tts.get_preset_voice(first)
                    self.current_voice_name = first
        
        print("Voice Assistant ready!\n")
    
    def convert_audio(self, input_path):
        """Convert any audio to 16kHz mono WAV."""
        output = tempfile.mktemp(suffix=".wav")
        subprocess.run([
            "ffmpeg", "-y", "-i", input_path,
            "-ar", "16000", "-ac", "1", "-acodec", "pcm_s16le",
            output
        ], capture_output=True)
        return output
    
    def transcribe(self, audio_path, language="auto"):
        """
        Transcribe audio to text.
        
        Args:
            audio_path: Path to audio file
            language: "auto", "vi", or "en"
        
        Returns:
            dict with text, segments, language, language_prob
        """
        wav = self.convert_audio(audio_path)
        
        try:
            lang_param = None if language == "auto" else language
            segments, info = self.stt.transcribe(wav, language=lang_param)
            
            segment_list = []
            full_text = []
            for s in segments:
                segment_list.append({
                    "start": s.start, 
                    "end": s.end, 
                    "text": s.text.strip()
                })
                full_text.append(s.text.strip())
            
            return {
                "text": " ".join(full_text),
                "segments": segment_list,
                "language": info.language,
                "language_prob": info.language_probability
            }
        finally:
            try:
                os.unlink(wav)
            except:
                pass
    
    def speak(self, text, voice=None, output_path=None):
        """
        Convert text to speech with VieNeu-TTS.
        
        Args:
            text: Text to synthesize
            voice: Voice name (optional)
            output_path: Output WAV path (optional)
        
        Returns:
            Path to generated audio file
        """
        if not HAS_VIENEU:
            print(f"[TTS] {text}")
            return None
        
        if output_path is None:
            output_path = tempfile.mktemp(suffix=".wav")
        
        if voice and voice in self.voices:
            voice_data = self.tts.get_preset_voice(voice)
        else:
            voice_data = self.current_voice
        
        audio = self.tts.infer(text=text, voice=voice_data)
        self.tts.save(audio, output_path)
        
        return output_path
    
    def list_voices(self):
        """List available TTS voices."""
        if not HAS_VIENEU:
            return []
        return list(self.voices.keys())
    
    def set_voice(self, voice_name):
        """Set the current TTS voice."""
        if voice_name in self.voices:
            self.current_voice = self.tts.get_preset_voice(voice_name)
            self.current_voice_name = voice_name
            return True
        return False


def main():
    parser = argparse.ArgumentParser(description="Voice Assistant - STT + TTS")
    parser.add_argument("command", nargs="?", default="interactive",
                        help="Command: interactive, transcribe, speak, voices")
    parser.add_argument("args", nargs="*", help="Arguments for command")
    parser.add_argument("--stt-model", "-m", default="small",
                        choices=["tiny", "base", "small", "medium", "large-v3"],
                        help="STT model size (default: small)")
    parser.add_argument("--device", "-d", default="cpu",
                        choices=["cpu", "cuda", "mps"],
                        help="STT device (default: cpu)")
    parser.add_argument("--voice", "-v", default=None,
                        help="TTS voice name")
    
    args = parser.parse_args()
    
    # Initialize
    assistant = VoiceAssistant(
        stt_model=args.stt_model,
        device=args.device,
        tts_voice=args.voice
    )
    
    # Execute command
    if args.command == "transcribe" and args.args:
        for audio_file in args.args:
            result = assistant.transcribe(audio_file)
            print(f"\n📝 {audio_file}")
            print(f"   Language: {result['language']} ({result['language_prob']:.0%})")
            print(f"   Transcript: {result['text']}")
    
    elif args.command == "speak" and args.args:
        text = " ".join(args.args)
        path = assistant.speak(text)
        if path:
            print(f"Speaker output: {path}")
    
    elif args.command == "voices":
        print("\nAvailable TTS voices:")
        for v in assistant.list_voices():
            print(f"  - {v}")
    
    elif args.command == "interactive":
        print("\n" + "="*50)
        print("Voice Assistant - STT + TTS")
        print("="*50)
        print("Commands:")
        print("  transcribe <file>   - Transcribe audio file")
        print("  speak <text>        - Speak text with TTS")
        print("  voices              - List TTS voices")
        print("  voice <name>        - Set TTS voice")
        print("  quit                - Exit")
        print()
        
        while True:
            try:
                cmd = input("> ").strip()
                if not cmd:
                    continue
                
                parts = cmd.split(maxsplit=1)
                action = parts[0]
                arg = parts[1] if len(parts) > 1 else ""
                
                if action == "quit":
                    break
                
                elif action == "transcribe" and arg:
                    result = assistant.transcribe(arg)
                    print(f"\n📝 {result['language']} ({result['language_prob']:.0%})")
                    print(f"   {result['text']}")
                
                elif action == "speak" and arg:
                    assistant.speak(arg)
                
                elif action == "voices":
                    for v in assistant.list_voices():
                        print(f"  - {v}")
                
                elif action == "voice" and arg:
                    if assistant.set_voice(arg):
                        print(f"Voice set to: {arg}")
                    else:
                        print(f"Unknown voice: {arg}")
                
                else:
                    print("Try: transcribe <file>, speak <text>, voices, voice <name>")
            
            except KeyboardInterrupt:
                print("\nBye!")
                break
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
