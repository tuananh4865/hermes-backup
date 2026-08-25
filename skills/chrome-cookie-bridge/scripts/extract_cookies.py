"""Extract Google cookies from Chrome profile using keychain decryption."""
import subprocess, sqlite3, json, hashlib, os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend


def get_chrome_key():
    """Get Chrome Safe Storage key from macOS keychain."""
    r = subprocess.run(
        ["security", "find-generic-password", "-s", "Chrome Safe Storage", "-w"],
        capture_output=True, text=True
    )
    return r.stdout.strip().encode("utf-8")


def derive_key(password):
    """Derive 16-byte key from Chrome password using PBKDF2."""
    return hashlib.pbkdf2_hmac("sha1", password, b"saltysalt", 1003, 16)


def decrypt_v10(encrypted_value, key):
    """Decrypt Chrome v10 cookie (macOS)."""
    if encrypted_value[:3] != b"v10":
        return None
    iv = b" " * 16  # 16 spaces
    ciphertext = encrypted_value[19:]  # Skip 'v10' (3) + IV (16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    # PKCS7 unpad
    try:
        unpadder = padding.PKCS7(128).unpadder()
        plaintext = unpadder.update(plaintext) + unpadder.finalize()
    except ValueError:
        pass
    return plaintext.decode("utf-8", errors="ignore")


def extract_cookies(chrome_db_path, output_file="cookies.json"):
    """Extract all cookies from Chrome DB and decrypt."""
    if not os.path.exists(chrome_db_path):
        print(f"� Chrome DB not found: {chrome_db_path}")
        return []

    password = get_chrome_key()
    key = derive_key(password)

    conn = sqlite3.connect(chrome_db_path)
    cur = conn.cursor()
    cur.execute("SELECT name, host_key, value, encrypted_value, path, is_secure, is_httponly, expires_utc FROM cookies")
    rows = cur.fetchall()
    conn.close()

    cookies = []
    for row in rows:
        name, host_key, value, encrypted_value, path, is_secure, is_httponly, expires_utc = row
        if not value and encrypted_value:
            value = decrypt_v10(encrypted_value, key)
        cookies.append({
            "name": name,
            "host": host_key,
            "value": value,
            "path": path,
            "secure": bool(is_secure),
            "httponly": bool(is_httponly),
            "expires_utc": expires_utc,
        })

    # Filter Google cookies
    google_cookies = [c for c in cookies if any(h in c["host"] for h in ["google.com", "youtube.com", "accounts.google.com", "labs.google"])]

    with open(output_file, "w") as f:
        json.dump(google_cookies, f, indent=2)

    print(f"✅ Extracted {len(google_cookies)} Google cookies from {len(cookies)} total")
    print(f"   Saved to {output_file}")
    return google_cookies


if __name__ == "__main__":
    import sys
    db_path = sys.argv[1] if len(sys.argv) > 1 else "/tmp/chrome-484-cookies.db"
    out_path = sys.argv[2] if len(sys.argv) > 2 else "/tmp/cdp-client/chrome-cookies.json"
    extract_cookies(db_path, out_path)
