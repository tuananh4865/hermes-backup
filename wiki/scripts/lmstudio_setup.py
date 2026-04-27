#!/opt/homebrew/bin/python3.14
"""
LM Studio Setup Helper — Check connection and available models

Usage:
    python lmstudio_setup.py
"""

import requests

LM_STUDIO_URL = "http://192.168.0.187:1234/v1"

def check_connection():
    """Check if LM Studio is running and server is enabled"""
    try:
        response = requests.get(f"{LM_STUDIO_URL}/models", timeout=5)
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, f"Status: {response.status_code}"
    except requests.exceptions.ConnectionError:
        return False, "Cannot connect - server not running"
    except Exception as e:
        return False, str(e)

def main():
    print("=" * 60)
    print("LM Studio Connection Check")
    print("=" * 60)
    
    connected, data = check_connection()
    
    if connected:
        print("✓ Connected to LM Studio!")
        print()
        models = data.get("data", [])
        print(f"Found {len(models)} model(s):")
        print()
        
        for model in models:
            model_id = model.get("id", "unknown")
            print(f"  • {model_id}")
            
            # Show details if available
            if "metadata" in model:
                meta = model["metadata"]
                if "context_length" in meta:
                    print(f"      Context: {meta['context_length']:,} tokens")
        
        print()
        print("To use a model for wiki agent:")
        print(f"  python lmstudio_wiki_agent.py --model MODEL_ID")
        print()
        print("Or edit the DEFAULT_MODEL in lmstudio_wiki_agent.py")
        
    else:
        print("✗ Cannot connect to LM Studio")
        print()
        print(f"Error: {data}")
        print()
        print("To fix:")
        print("1. Open LM Studio")
        print("2. Load a model (e.g., Qwen2.5, Llama, etc.)")
        print("3. Press Cmd+Shift+L (or click 'Local Server' in sidebar)")
        print("4. Click 'Start Server'")
        print("5. Run this script again")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
