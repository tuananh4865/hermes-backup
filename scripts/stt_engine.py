#!/usr/bin/env python3
"""
STT Engine - Faster Whisper cho Vietnamese + English Mixed Language
Supports: Vietnamese (vi), English (en), Mixed
"""

import os
import sys
import tempfile
import subprocess
from pathlib import Path

# Faster Whisper
from faster_whisper import WhisperModel


class STTEngine:
    """Vietnamese + English Speech-to-Text Engine"""
    
    # Supported languages
    LANGUAGES = {
        "vi": "Vietnamese",
        "en": "English", 
        "auto": "Auto Detect"
    }
    
    # Model sizes: tiny(39MB), base(74MB), small(244MB), medium(769MB)
    MODELS = ["tiny", "base", "small", "medium", "large-v3"]
    
    def __init__(self, model_size="small", device="cpu"):
        """
        Initialize STT engine.
        
        Args:
            model_size: Model size (tiny/base/small/medium/large-v3)
            device: cpu/cuda/mps
        """
        if model_size not in self.MODELS:
            raise ValueError(f"Model must be one of: {self.MODELS}")
        
        self.model_size = model_size
        self.device = device
        
        print(f"Loading faster-whisper ({model_size}, {device})...")
        self.model = WhisperModel(model_size, device=device)
        print("Model loaded!")
    
    def convert_audio(self, input_path, output_path=None):
        """
        Convert audio to 16kHz mono WAV for optimal STT.
        
        Args:
            input_path: Audio file path (m4a, mp3, wav, flac, ogg, etc.)
            output_path: Output WAV path (optional, auto-generated)
        
        Returns:
            Path to converted WAV file
        """
        if output_path is None:
            output_path = tempfile.mktemp(suffix=".wav")
        
        # Use ffmpeg to convert
        cmd = [
            "ffmpeg", "-y", "-i", input_path,
            "-ar", "16000",          # 16kHz sample rate (speech standard)
            "-ac", "1",              # Mono channel
            "-acodec", "pcm_s16le",  # 16-bit PCM
            output_path
        ]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            raise RuntimeError(f"ffmpeg error: {result.stderr}")
        
        return output_path
    
    def transcribe(self, audio_path, language="auto", convert=True):
        """
        Transcribe audio to text.
        
        Args:
            audio_path: Path to audio file
            language: "auto" (detect), "vi" (Vietnamese), "en" (English)
            convert: Auto-convert to 16kHz WAV if True
        
        Returns:
            dict with keys: text, segments, language, language_prob
        """
        # Convert if needed
        if convert:
            wav_path = self.convert_audio(audio_path)
        else:
            wav_path = audio_path
        
        try:
            # Auto detect if language="auto"
            lang_param = None if language == "auto" else language
            
            segments, info = self.model.transcribe(
                wav_path,
                language=lang_param,
                word_timestamps=True
            )
            
            # Collect results
            segment_list = []
            full_text = []
            
            for segment in segments:
                segment_list.append({
                    "start": segment.start,
                    "end": segment.end,
                    "text": segment.text.strip()
                })
                full_text.append(segment.text.strip())
            
            return {
                "text": " ".join(full_text),
                "segments": segment_list,
                "language": info.language,
                "language_prob": info.language_probability
            }
        
        finally:
            # Cleanup temp file if we created it
            if convert:
                try:
                    os.unlink(wav_path)
                except:
                    pass
    
    def transcribe_vietnamese(self, audio_path):
        """Transcribe with Vietnamese language model."""
        return self.transcribe(audio_path, language="vi")
    
    def transcribe_english(self, audio_path):
        """Transcribe with English language model."""
        return self.transcribe(audio_path, language="en")
    
    def transcribe_mixed(self, audio_path):
        """
        Transcribe mixed Vietnamese/English audio.
        Uses auto-detect for best results.
        """
        return self.transcribe(audio_path, language="auto")
    
    def interactive(self):
        """Interactive STT mode."""
        print("\n" + "="*50)
        print("🎙️  STT Engine - Vietnamese + English")
        print("="*50)
        print("Commands:")
        print("  vi <file>   - Transcribe as Vietnamese")
        print("  en <file>   - Transcribe as English")
        print("  mixed <file> - Auto-detect language")
        print("  quit        - Exit")
        print()
        
        while True:
            try:
                cmd = input("> ").strip().split()
                
                if not cmd:
                    continue
                
                if cmd[0] == "quit":
                    break
                
                elif cmd[0] in ("vi", "en", "mixed") and len(cmd) > 1:
                    lang_map = {"vi": "vi", "en": "en", "mixed": "auto"}
                    lang = lang_map[cmd[0]]
                    result = self.transcribe(" ".join(cmd[1:]), language=lang)
                    
                    print(f"\n📝 Transcript ({lang}, prob: {result['language_prob']:.2f}):")
                    print(result['text'])
                    print()
                
                else:
                    print("Invalid command. Try: vi <file>, en <file>, mixed <file>")
            
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Faster Whisper STT Engine")
    parser.add_argument(
        "--model", "-m",
        default="small",
        choices=STTEngine.MODELS,
        help="Model size (default: small)"
    )
    parser.add_argument(
        "--device", "-d",
        default="cpu",
        choices=["cpu", "cuda", "mps"],
        help="Device to use (default: cpu)"
    )
    parser.add_argument(
        "--language", "-l",
        default="auto",
        choices=["auto", "vi", "en"],
        help="Language mode (default: auto)"
    )
    parser.add_argument(
        "audio",
        nargs="?",
        help="Audio file to transcribe"
    )
    
    args = parser.parse_args()
    
    # Initialize engine
    engine = STTEngine(model_size=args.model, device=args.device)
    
    if args.audio:
        # Single file transcription
        result = engine.transcribe(args.audio, language=args.language)
        
        print(f"\n📝 Transcript:")
        print(result['text'])
        print(f"\nLanguage: {result['language']} (prob: {result['language_prob']:.2f})")
        
        # Save to file
        output_path = args.audio + ".txt"
        with open(output_path, "w") as f:
            f.write(result['text'])
        print(f"💾 Saved to: {output_path}")
    
    else:
        # Interactive mode
        engine.interactive()


if __name__ == "__main__":
    main()
