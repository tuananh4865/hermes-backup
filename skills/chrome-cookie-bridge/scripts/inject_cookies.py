"""Inject Google cookies into Chrome CDP profile DB."""
import sqlite3, json, hashlib, os, time, subprocess
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend


def encrypt_v10(plaintext, key):
    """Encrypt in Chrome v10 format."""
    if isinstance(plaintext, str):
        plaintext = plaintext.encode("utf-8")
    padder = padding.PKCS7(128).padder()
    padded = padder.update(plaintext) + padder.finalize()
    iv = b" " * 16
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded) + encryptor.finalize()
    return b"v10" + iv + ciphertext


def get_chrome_key():
    r = subprocess.run(["security", "find-generic-password", "-s", "Chrome Safe Storage", "-w"], capture_output=True, text=True)
    return r.stdout.strip().encode("utf-8")


def derive_key(password):
    return hashlib.pbkdf2_hmac("sha1", password, b"saltysalt", 1003, 16)


def inject_cookies(src_db, dst_db, cookies_json):
    """Copy cookie rows from src to dst, updating timestamps."""
    with open(cookies_json) as f:
        cookies = json.load(f)

    password = get_chrome_key()
    key = derive_key(password)

    # Chrome epoch
    CHROME_EPOCH = 11644473600000000
    now_us = int(time.time() * 1000000)
    now_chrome = now_us + CHROME_EPOCH

    src = sqlite3.connect(src_db)
    src_cur = src.cursor()
    src_cur.execute("SELECT * FROM cookies")
    rows = src_cur.fetchall()
    src_cur.execute("PRAGMA table_info(cookies)")
    cols = [r[1] for r in src_cur.fetchall()]

    dst = sqlite3.connect(dst_db)
    dst_cur = dst.cursor()
    dst_cur.execute("DELETE FROM cookies")
    dst.commit()

    # Get full rows for Google cookies
    google_hosts = ['google.com', 'youtube.com', 'accounts.google.com', 'labs.google', 'gstatic.com']
    host_filter = " OR ".join([f"host_key LIKE '%{h}%'" for h in google_hosts])
    src_cur.execute(f"SELECT * FROM cookies WHERE {host_filter}")
    rows = src_cur.fetchall()

    inserted = 0
    for row in rows:
        new_row = list(row)
        # Update timestamps
        if 'creation_utc' in cols:
            new_row[cols.index('creation_utc')] = now_chrome
        if 'last_access_utc' in cols:
            new_row[cols.index('last_access_utc')] = now_chrome
        if 'last_update_utc' in cols:
            new_row[cols.index('last_update_utc')] = now_chrome

        placeholders = ", ".join(["?"] * len(cols))
        cols_str = ", ".join(cols)
        try:
            dst_cur.execute(f"INSERT OR REPLACE INTO cookies ({cols_str}) VALUES ({placeholders})", new_row)
            inserted += 1
        except Exception as e:
            pass

    dst.commit()
    print(f"✅ Inserted {inserted} Google cookies to {dst_db}")
    print(f"   Now restart Chrome CDP to load cookies")

    src.close()
    dst.close()


if __name__ == "__main__":
    import sys
    src = sys.argv[1] if len(sys.argv) > 1 else "/tmp/chrome-484-cookies.db"
    dst = sys.argv[2] if len(sys.argv) > 2 else "/tmp/chrome-for-flow/Default/Cookies"
    cookies = sys.argv[3] if len(sys.argv) > 3 else "/tmp/cdp-client/chrome-484-cookies.json"
    inject_cookies(src, dst, cookies)
