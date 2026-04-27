#!/opt/homebrew/bin/python3.14
"""
Multi-modal Ingestion — OCR images, extract PDFs, transcribe audio

Usage:
    python3 ingest_multimodal.py --ocr image.png
    python3 ingest_multimodal.py --pdf document.pdf
    python3 ingest_multimodal.py --audio recording.m4a
    python3 ingest_multimodal.py --batch *.png
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path
from typing import Optional

# ═══════════════════════════════════════════════════════════════
# CONFIG
# ═══════════════════════════════════════════════════════════════

WIKI_PATH = Path("/Volumes/Storage-1/Hermes/wiki")
RAW_ASSETS = WIKI_PATH / "raw" / "assets"

# ═══════════════════════════════════════════════════════════════

def ocr_image(image_path: str) -> Optional[str]:
    """OCR an image using macOS built-in OCR (via sips + tesseract)"""
    try:
        # Check if tesseract is installed
        result = subprocess.run(['which', 'tesseract'], capture_output=True)
        if result.returncode != 0:
            # Fallback: use AppleScript for simple screen capture OCR
            return None
        
        # Convert to tiff first
        tiff_path = '/tmp/ocr_input.tiff'
        subprocess.run(['sips', '-s', 'format', 'tiff', image_path, '--out', tiff_path], check=True)
        
        # Run OCR
        result = subprocess.run(['tesseract', tiff_path, 'stdout', '-l', 'eng+viet'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            return result.stdout.strip()
        return None
    except Exception as e:
        print(f"OCR error: {e}")
        return None

def extract_pdf_text(pdf_path: str) -> Optional[str]:
    """Extract text from PDF using web_extract or fallback"""
    try:
        # Try using web_extract style (for arXiv papers)
        from web_extract import extract_from_pdf
        return extract_from_pdf(pdf_path)
    except:
        # Fallback: use pdftotext if available
        try:
            result = subprocess.run(['pdftotext', pdf_path, '-'], capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout.strip()
        except:
            pass
        return None

def transcribe_audio(audio_path: str) -> Optional[str]:
    """Transcribe audio using Whisper"""
    try:
        import whisper
        model = whisper.load_model("base")
        result = model.transcribe(audio_path)
        return result["text"].strip()
    except ImportError:
        print("Whisper not installed. Run: pip install openai-whisper")
        return None
    except Exception as e:
        print(f"Transcription error: {e}")
        return None

def save_ocr_result(text: str, image_path: str) -> Path:
    """Save OCR result to wiki"""
    from datetime import datetime
    
    filename = Path(image_path).stem + "-ocr.md"
    filepath = RAW_ASSETS / filename
    
    content = f"""---
title: "OCR: {Path(image_path).name}"
date: {datetime.now().strftime('%Y-%m-%d')}
type: ocr
tags: []
source: {image_path}
---

# OCR Result: {Path(image_path).name}

{text}
"""
    
    RAW_ASSETS.mkdir(parents=True, exist_ok=True)
    filepath.write_text(content)
    return filepath

def save_pdf_result(text: str, pdf_path: str) -> Path:
    """Save PDF extraction result"""
    from datetime import datetime
    
    filename = Path(pdf_path).stem + "-content.md"
    filepath = RAW_ASSETS / filename
    
    content = f"""---
title: "PDF Content: {Path(pdf_path).name}"
date: {datetime.now().strftime('%Y-%m-%d')}
type: pdf-extract
tags: []
source: {pdf_path}
---

# PDF Content: {Path(pdf_path).name}

{text[:10000]}  # First 10k chars
"""
    
    RAW_ASSETS.mkdir(parents=True, exist_ok=True)
    filepath.write_text(content)
    return filepath

def save_transcription(text: str, audio_path: str) -> Path:
    """Save audio transcription"""
    from datetime import datetime
    
    filename = Path(audio_path).stem + "-transcript.md"
    filepath = RAW_ASSETS / filename
    
    content = f"""---
title: "Transcription: {Path(audio_path).name}"
date: {datetime.now().strftime('%Y-%m-%d')}
type: transcription
tags: []
source: {audio_path}
---

# Transcription: {Path(audio_path).name}

{text}
"""
    
    RAW_ASSETS.mkdir(parents=True, exist_ok=True)
    filepath.write_text(content)
    return filepath

def main():
    parser = argparse.ArgumentParser(description='Multi-modal ingestion')
    parser.add_argument('--ocr', metavar='IMAGE', help='OCR an image')
    parser.add_argument('--pdf', metavar='PDF', help='Extract text from PDF')
    parser.add_argument('--audio', metavar='AUDIO', help='Transcribe audio')
    parser.add_argument('--batch', nargs='+', help='Batch process files')
    args = parser.parse_args()
    
    if args.ocr:
        print(f"OCR: {args.ocr}")
        text = ocr_image(args.ocr)
        if text:
            filepath = save_ocr_result(text, args.ocr)
            print(f"Saved to {filepath}")
        else:
            print("OCR failed or tesseract not installed")
        return
    
    if args.pdf:
        print(f"Extracting PDF: {args.pdf}")
        text = extract_pdf_text(args.pdf)
        if text:
            filepath = save_pdf_result(text, args.pdf)
            print(f"Saved to {filepath}")
        else:
            print("PDF extraction failed")
        return
    
    if args.audio:
        print(f"Transcribing: {args.audio}")
        text = transcribe_audio(args.audio)
        if text:
            filepath = save_transcription(text, args.audio)
            print(f"Saved to {filepath}")
        else:
            print("Transcription failed")
        return
    
    if args.batch:
        for filepath in args.batch:
            ext = Path(filepath).suffix.lower()
            if ext in ['.png', '.jpg', '.jpeg', '.tiff', '.heic']:
                print(f"OCR: {filepath}")
                text = ocr_image(filepath)
                if text:
                    save_ocr_result(text, filepath)
            elif ext == '.pdf':
                print(f"PDF: {filepath}")
                text = extract_pdf_text(filepath)
                if text:
                    save_pdf_result(text, filepath)
            elif ext in ['.m4a', '.mp3', '.wav', '.mp4']:
                print(f"Audio: {filepath}")
                text = transcribe_audio(filepath)
                if text:
                    save_transcription(text, filepath)
        return
    
    parser.print_help()

if __name__ == '__main__':
    main()
