# Chrome Safe Storage — Kỹ thuật giải mã

## Tổng quan

Chrome trên macOS mã hóa cookies trong SQLite database `~/Library/Application Support/Google/Chrome/Default/Cookies` bằng AES-128-CBC. Key derive từ keychain entry "Chrome Safe Storage".

## Flow giải mã

```
┌─────────────────────────────────────────┐
│ macOS Keychain                            │
│ Service: "Chrome Safe Storage"            │
│ Account: "Chrome"                         │
│ → Returns: base64-encoded password        │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│ PBKDF2 Key Derivation                     │
│ hash: SHA1                                │
│ salt: b"saltysalt" (16 bytes)             │
│ iterations: 1003                          │
│ key_length: 16 bytes (AES-128)            │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│ AES-128-CBC Decryption                    │
│ IV: b" " * 16 (16 spaces)                 │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│ Cookie Value (plaintext UTF-8)            │
└─────────────────────────────────────────┘
```

## Encryption Format Versions

| Version | Format | Decryption |
|---|---|---|
| **v10** | `b'v10' + IV(16 spaces) + AES-CBC` | Key từ Keychain |
| **v11** | `b'v11' + IV(12 bytes random + 4 zero bytes) + AES-CBC` | Key từ Keychain |
| v8 | Legacy (rare) | |
| v20 | Chromium 2023+ (newer platforms) | App-bound key |

**Chrome 151 trên macOS dùng v10 format** (verified 15/08/2026).

## Python Implementation

```python
import subprocess
import hashlib
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
    iv = b" " * 16
    ciphertext = encrypted_value[19:]  # Skip 'v10' (3) + IV (16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    try:
        unpadder = padding.PKCS7(128).unpadder()
        plaintext = unpadder.update(plaintext) + unpadder.finalize()
    except ValueError:
        pass
    return plaintext.decode("utf-8", errors="ignore")
```

## Cookie DB Schema (Chrome 151)

```sql
CREATE TABLE cookies(
    creation_utc INTEGER NOT NULL,
    host_key TEXT NOT NULL,
    top_frame_site_key TEXT NOT NULL,
    name TEXT NOT NULL,
    value TEXT NOT NULL,
    encrypted_value BLOB NOT NULL,
    path TEXT NOT NULL,
    expires_utc INTEGER NOT NULL,
    is_secure INTEGER NOT NULL,
    is_httponly INTEGER NOT NULL,
    last_access_utc INTEGER NOT NULL,
    has_expires INTEGER NOT NULL,
    is_persistent INTEGER NOT NULL,
    priority INTEGER NOT NULL,
    samesite INTEGER NOT NULL,
    source_scheme INTEGER NOT NULL,
    source_port INTEGER NOT NULL,
    last_update_utc INTEGER NOT NULL,
    source_type INTEGER NOT NULL,
    has_cross_site_ancestor INTEGER NOT NULL
);
```

## Time Format

Chrome sử dụng **Windows file time** (100-nanosecond intervals since January 1, 1601):

```python
CHROME_EPOCH_OFFSET = 11644473600000000  # microseconds

# Convert from Chrome to Unix:
unix_timestamp = (chrome_value / 1000000) - CHROME_EPOCH_OFFSET

# Convert from Unix to Chrome:
chrome_value = (unix_timestamp * 1000000) + CHROME_EPOCH_OFFSET
```

## Validation Rules

Chrome validates cookies on load:

1. **Expired cookies** (`expires_utc < now`) → dropped
2. **Future creation_utc** → dropped (anti-tampering)
3. **Wrong encrypted_value format** → dropped
4. **Path mismatch** → dropped
5. **Domain validation** → dropped if invalid

**Critical:** When injecting, **update `creation_utc` + `last_access_utc` to NOW** to avoid Chrome dropping them as "too old".

## Security Implications

- Malware có thể steal Chrome cookies = full account takeover
- Apple sandbox prevent most attacks but **user-space** access (Python scripts) can still decrypt
- **Defense**: Enable FileVault + macOS Keychain Access Control for "Chrome Safe Storage"
- Better defense: Use 1Password/Bitwarden + disable Chrome password saving
