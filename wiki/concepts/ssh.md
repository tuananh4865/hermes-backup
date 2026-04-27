---
title: "Ssh"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [ssh, networking, security, remote-access, encryption, devops]
---

# Ssh

## Overview

SSH (Secure Shell) is a cryptographic network protocol that provides a secure, encrypted channel for operating network services over an unsecured network. Originally developed as a replacement for insecure protocols like Telnet, rlogin, and FTP, SSH encrypts all traffic between client and server, protecting against eavesdropping, connection hijacking, and other attacks. It is the essential tool for remote system administration, secure file transfer, and encrypted communication between computers.

SSH operates on a client-server model: an SSH client initiates a connection to an SSH server listening on port 22 (by default), authenticates using cryptographic keys or passwords, and then provides a secure channel for remote command execution, interactive terminal sessions, or data transfer. The protocol supports multiple authentication methods, with public key authentication being the most secure and commonly recommended for production environments.

The SSH protocol family includes several related tools: `ssh` for remote shell access, `scp` and `sftp` for file transfers, and `sshfs` for mounting remote filesystems locally. SSH tunneling (port forwarding) allows arbitrary [[TCP]] connections to be tunneled through the encrypted session, enabling secure access to services that would otherwise be transmitted in plaintext.

## Key Concepts

**Public Key Authentication**: The most secure authentication method in SSH uses asymmetric cryptography. The user generates a key pair — a private key kept secret on the client machine and a public key stored on the server in `~/.ssh/authorized_keys`. When connecting, the server verifies that the client possesses the corresponding private key without ever transmitting the private key over the network.

```bash
# Generate an SSH key pair
ssh-keygen -t ed25519 -C "your_email@example.com"

# The command creates:
# ~/.ssh/id_ed25519      (private key - NEVER share)
# ~/.ssh/id_ed25519.pub  (public key - add to server's authorized_keys)
```

**Encryption Algorithms**: SSH supports multiple symmetric encryption algorithms (AES, ChaCha20), asymmetric algorithms (RSA, DSA, ECDSA, Ed25519), and key exchange methods (Diffie-Hellman groups). Modern SSH configurations prioritize strong algorithms like AES-256 and Ed25519, moving away from deprecated options like 3DES and SHA-1.

**SSH Config File**: Users can configure connection parameters in `~/.ssh/config`, enabling short hostname aliases, automatic key selection, and per-host settings:

```
Host myserver
    HostName server.example.com
    User ubuntu
    Port 22
    IdentityFile ~/.ssh/id_ed25519
    ForwardAgent yes
```

**SSH Agents**: An SSH agent is a background program that holds decrypted private keys in memory, allowing connections to multiple servers without re-entering passphrases. `ssh-agent` and `ssh-add` manage keys in the agent, while `AgentForwarding` allows the agent to be used from a remote server.

**Known Hosts**: SSH clients maintain a `~/.ssh/known_hosts` file containing fingerprints of servers the user has connected to. On first connection, the server's fingerprint is recorded; on subsequent connections, the client verifies the server hasn't changed (which could indicate a man-in-the-middle attack).

## How It Works

An SSH connection proceeds through several stages:

1. **TCP Connection**: The client connects to port 22 on the server via [[TCP]].
2. **Protocol Version Exchange**: Client and server agree on SSH protocol versions (SSH-2.0 is the current standard).
3. **Key Exchange (KEX)**: The client and server negotiate a session key using Diffie-Hellman or elliptic curve Diffie-Hellman, establishing the symmetric encryption for the session. This phase is protected by the server authenticating itself with its host key.
4. **Service Request**: The client requests a specific service (typically `ssh-userauth`).
5. **Authentication**: The user authenticates via password, public key, or keyboard-interactive methods.
6. **Session**: An interactive shell or command execution channel is opened. Multiple logical channels (stdin/stdout/stderr, port forwards, etc.) can multiplex over the single connection.

The entire exchange after the initial TCP handshake is encrypted, making it safe to use even over hostile networks like public WiFi.

## Practical Applications

**Remote Server Administration**: System administrators use SSH to access and manage servers, run commands, edit configuration files, and monitor system resources. This is the fundamental tool for cloud infrastructure management on providers like AWS, GCP, and Azure.

**Secure File Transfer**: `scp` copies files over SSH:

```bash
# Copy local file to remote server
scp ./deployment.jar ubuntu@server.example.com:/opt/app/

# Copy remote directory to local machine
scp -r ubuntu@server.example.com:/var/logs ./local-logs/

# Using SFTP for interactive transfers
sftp ubuntu@server.example.com
```

**Git over SSH**: Instead of HTTPS, developers often use SSH URLs for [[Git]] repositories, enabling authenticated pushes without entering credentials repeatedly:

```bash
git clone git@github.com:username/repo.git
git remote add origin git@github.com:username/repo.git
```

**SSH Tunneling / Port Forwarding**: Encrypted tunnels for secure access to internal services:

```bash
# Local port forwarding: access remote MySQL as if it were local
ssh -L 3306:localhost:3306 ubuntu@server.example.com

# Dynamic port forwarding (SOCKS proxy)
ssh -D 1080 ubuntu@server.example.com

# Remote port forwarding: expose local service to remote server
ssh -R 8080:localhost:3000 ubuntu@server.example.com
```

## Examples

Hardening SSH server configuration (`/etc/ssh/sshd_config`):

```
# Use strong protocol version
Protocol 2

# Disable password authentication (require key-based login)
PasswordAuthentication no
PermitRootLogin no
PubkeyAuthentication yes

# Limit users who can SSH in
AllowUsers ubuntu admin

# Disable empty passwords
PermitEmptyPasswords no

# Set idle timeout
ClientAliveInterval 300
ClientAliveCountMax 2

# Limit authentication attempts
MaxAuthTries 3

# Use modern ciphers
Ciphers chacha20-poly1305@openssh.com,aes256-gcm@openssh.com
```

Connecting with key-based authentication and agent forwarding:

```bash
# Add key to agent (enter passphrase once)
ssh-add ~/.ssh/id_ed25519

# Connect with agent forwarding (allows ssh from server to other servers)
ssh -A ubuntu@myserver

# On remote server, you can now ssh to other servers using your local keys
```

## Related Concepts

- [[Git]] - Version control often accessed via SSH
- [[TCP]] - The transport protocol SSH runs on
- [[Encryption]] - The cryptographic foundation of SSH
- [[Network Security]] - Protecting network communications
- [[Linux]] - Servers often administered via SSH
- [[DevOps]] - Practices heavily reliant on SSH for infrastructure management

## Further Reading

- [OpenSSH Official Documentation](https://www.openssh.com/manual.html)
- [SSH Config File Documentation](https://man.openbsd.org/ssh_config.5)
- [Mozilla SSH Guidelines](https://infosec.mozilla.org/guidelines/openssh)

## Personal Notes

SSH is one of those foundational tools that every developer and system administrator needs to master. I keep my `~/.ssh/config` well-organized with named hosts for every server I manage — it eliminates remembering IP addresses and automates key selection. I exclusively use Ed25519 keys for new connections and store nothing sensitive without a passphrase. The `ssh -A` agent forwarding feature is incredibly useful for Git workflows on remote servers, but I apply it selectively because it does have security implications if the remote server is untrusted.
