#!/opt/homebrew/bin/python3.14
"""
Bookmarklet Generator for Obsidian Web Clipper

Usage:
    python generate-bookmarklet.py

Customize the SETTINGS below before running.
"""

# SETTINGS — Customize these before running

VAULT = ""  # Leave empty for default vault, or specify: "My Vault"

FOLDER = "Clippings/"  # Folder inside vault for clipped articles

TAGS = "clippings"  # Comma-separated: "ml, ai, paper"

import urllib.parse

def escape_js(s):
    """Escape string for JavaScript"""
    return s.replace('\\', '\\\\').replace("'", "\\'").replace('"', '\\"').replace('\n', '\\n').replace('\r', '')

def generate_bookmarklet():
    """Generate the bookmarklet code"""
    
    # Build JS without f-string to avoid brace escaping hell
    vault_esc = escape_js(VAULT)
    folder_esc = escape_js(FOLDER)
    tags_esc = escape_js(TAGS)
    
    js_code = (
        "javascript:(function(){"
        "Promise.all(["
        "import('https://unpkg.com/turndown@6.0.0?module'),"
        "import('https://unpkg.com/@tehshrike/readability@0.2.0')"
        "]).then(async([{default:Turndown},{default:Readability}])=>{"
        "const vault='" + vault_esc + "';"
        "const folder='" + folder_esc + "';"
        "let tags='" + tags_esc + "';"
        "const{title,byline,content}=new Readability(document.cloneNode(true)).parse();"
        "const markdownBody=new Turndown({headingStyle:'atx',hr:'---',bulletListMarker:'-',codeBlockStyle:'fenced',emDelimiter:'*'}).turndown(content);"
        "var date=new Date();"
        "const today=date.toISOString().split('T')[0];"
        "const author='';"
        "const authorBrackets=author?'\"[[\"+author+\"]]\"':'';"
        "const fileContent='---\\ncategory: \"[[Clippings]]\"\\nauthor: '+authorBrackets+'\\ntitle: \"'+title+'\"\\nsource: '+document.URL+'\\nclipped: '+today+'\\ntags: ['+tags+']\\n---\\n\\n'+markdownBody;"
        "document.location.href='obsidian://new?file='+encodeURIComponent(folder+title)+'&content='+encodeURIComponent(fileContent)+vault;"
        "})})();"
    )
    
    return js_code

def main():
    print("=" * 60)
    print("Obsidian Web Clipper Bookmarklet Generator")
    print("=" * 60)
    print()
    print(f"Settings:")
    print(f"  Vault:  {VAULT or '(default)'}")
    print(f"  Folder: {FOLDER}")
    print(f"  Tags:   {TAGS}")
    print()
    print("=" * 60)
    print("BOOKMARKLET CODE (copy the entire line below):")
    print("=" * 60)
    print()
    print(generate_bookmarklet())
    print()
    print("=" * 60)
    print("Instructions:")
    print("1. Select ALL text above (from 'javascript:' onwards)")
    print("2. Copy to clipboard")
    print("3. Create new bookmark in browser")
    print("4. Paste into URL/location field")
    print("=" * 60)

if __name__ == "__main__":
    main()
