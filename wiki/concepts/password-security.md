---
title: Password Security
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [password-security, security, authentication, cryptography]
---

# Password Security

Password security encompasses the practices, technologies, and policies for creating, storing, transmitting, and managing credentials securely. Passwords remain the dominant authentication mechanism for web applications, email systems, operating systems, and enterprise networks despite decades of alternative authentication methods. Their continued prevalence makes password security a critical concern for individuals and organizations alike, as compromised credentials are among the most common attack vectors for data breaches and unauthorized access.

## Overview

The fundamental challenge of password security lies in the tension between usability and security. Strong passwords—long, complex, unique per site—are difficult for humans to remember, leading to dangerous practices like reuse across multiple services or storage in insecure locations. Meanwhile, attackers employ increasingly sophisticated methods to crack passwords, from brute force attacks that try every possible combination to dictionary attacks that leverage common patterns and leaked password databases.

Modern password security extends beyond individual password strength to encompass entire authentication systems and organizational policies. This includes secure password storage using cryptographic hashing, transmission security through encrypted channels, rate limiting and account lockout mechanisms to prevent brute force attacks, and user education to promote better password practices. The field continues to evolve with emerging alternatives like passkeys that aim to eliminate passwords entirely.

## Key Concepts

**Password Hashing** is the practice of never storing passwords in plaintext. When a user creates a password, the system applies a cryptographic hash function to transform it into an irreversible representation. When the user authenticates, the submitted password is hashed again and compared against the stored hash. Good hashing algorithms (like bcrypt, scrypt, or Argon2) are intentionally slow and include salts—random data added to each password before hashing—to resist rainbow table attacks and make brute force attacks computationally expensive.

**Password Entropy** measures the randomness and unpredictability of a password, typically expressed in bits. A password with n bits of entropy would require an attacker to try 2^n possibilities on average to crack it. Entropy increases with length and character variety, but human-generated passwords often have less entropy than expected due to predictable patterns. The best approach prioritizes length over complexity, as longer passphrases are both more secure and more memorable.

**Multi-Factor Authentication (MFA)** adds additional verification layers beyond passwords. Something you know (password), something you have (phone or hardware token), and something you are (biometrics) combine to provide stronger authentication even if passwords are compromised. TOTP (Time-based One-Time Password) apps and hardware security keys provide robust second factors that resist phishing and replay attacks.

## How It Works

Password attack vectors include:

- **Brute Force**: Trying all possible character combinations
- **Dictionary Attacks**: Trying common words and phrases
- **Credential Stuffing**: Reusing passwords leaked from other breaches
- **Phishing**: Tricking users into revealing passwords
- **Keyloggers/Malware**: Capturing passwords as they're typed
- **Shoulder Surfing**: Observing password entry

Defensive measures address each vector:

- **Rate Limiting**: Slows brute force attempts
- **Account Lockout**: Temporarily disables accounts after failures
- **CAPTCHA**: Blocks automated attacks
- **Breach Monitoring**: Alerts users when their emails appear in leaks
- **Password Managers**: Enable unique, complex passwords without memorization

## Practical Applications

Organizations should implement comprehensive password policies that balance security with usability. Minimum length requirements (12+ characters recommended), prohibition of commonly breached passwords, and regular password changes for privileged accounts are common requirements. However, forced frequent changes often lead to weaker passwords, so modern guidance favors longer passwords with breach monitoring instead.

User education remains essential but insufficient on its own. Technical controls like [[authentication]] systems that enforce good practices, integration with [[web-security]] measures, and monitoring for compromised credentials provide defense in depth. Passwordless authentication approaches—including FIDO2/WebAuthn standards—represent the future direction, offering stronger security without password memorization burdens.

## Examples

Implementing secure password hashing in Python:
```python
import bcrypt

def hash_password(password: str) -> bytes:
    """Hash a password using bcrypt with automatic salt generation."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def verify_password(password: str, hashed: bytes) -> bool:
    """Verify a password against its bcrypt hash."""
    return bcrypt.checkpw(password.encode('utf-8'), hashed)

# Usage
stored_hash = hash_password("user's_secure_password")
assert verify_password("user's_secure_password", stored_hash)
assert not verify_password("wrong_password", stored_hash)
```

Checking passwords against the Have I Been Pwned database:
```python
import hashlib
import requests

def check_password_breached(password: str) -> bool:
    """Check if a password appears in known breaches via HIBP."""
    sha1_hash = hashlib.sha1(password.encode()).hexdigest().upper()
    prefix, suffix = sha1_hash[:5], sha1_hash[5:]
    
    response = requests.get(f"https://api.pwnedpasswords.com/range/{prefix}")
    return suffix in response.text
```

## Related Concepts

- [[authentication]] — Identity verification systems
- [[web-security]] — Broader web security context
- [[cryptography]] — Encryption and hashing fundamentals
- [[multi-factor-authentication]] — Additional authentication layers
- [[password-managers]] — Secure password storage tools

## Further Reading

- NIST Special Publication 800-63B — Digital Identity Guidelines (password recommendations)
- Have I Been Pwned — Check if your accounts were in data breaches
- "Security Engineering" by Ross Anderson — Comprehensive security reference

## Personal Notes

The single most impactful improvement most individuals can make is using a password manager. It enables unique, complex passwords for every service without memorization. Combined with MFA on important accounts, this dramatically reduces account takeover risk. For organizations, passwordless authentication (passkeys/FIDO2) offers the best path forward, eliminating entire classes of password attacks while improving user experience.
