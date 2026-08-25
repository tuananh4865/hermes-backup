# GitHub Authentication Reference

Formerly a standalone skill. Content absorbed into `github-operations`.

## HTTPS Token Setup

```bash
# Configure gh to use HTTPS instead of SSH
gh auth setup-git
gh auth status
```

## SSH Key Configuration

```bash
# Generate new SSH key
ssh-keygen -t ed25519 -C "your_email@example.com"

# Add to ssh-agent
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

# Add to GitHub
gh ssh-key add ~/.ssh/id_ed25519.pub --title "Hermes Agent"

# Verify
ssh -T git@github.com
```

## Token Management

```bash
# Store token
gh auth token | pbcopy

# Check auth status
gh auth status
```
