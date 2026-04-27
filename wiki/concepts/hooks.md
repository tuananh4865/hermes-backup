---
confidence: high
last_verified: 2026-04-11
relationships:
  - 🔗 automation (extracted)
  - 🔗 git (extracted)
  - 🔗 events (inferred)
last_updated: 2026-04-11
tags:
  - hooks
  - automation
  - git
  - webhooks
---

# Hooks

> Hooks are callbacks triggered by events — allowing code to run automatically when something happens.

## Overview

Hooks let you attach custom behavior to events:
- **Git hooks**: Run scripts on commit, push, etc.
- **Webhooks**: HTTP callbacks when events occur
- **Software hooks**: Event listeners in applications

## Git Hooks

Git hooks run during git operations.

### Common Hooks

| Hook | When | Use Case |
|------|------|----------|
| **pre-commit** | Before commit | Lint, format, tests |
| **prepare-commit-msg** | Before message | Auto-fill template |
| **commit-msg** | After message | Validate format |
| **post-commit** | After commit | Notify, deploy |
| **pre-push** | Before push | Run tests |
| **post-push** | After push | Deploy, notify |

### Setting Up

```bash
# Enable hook
ln -s ../../scripts/pre-commit.sh .git/hooks/pre-commit

# Or use a tool like Husky
npx husky install
```

### Example: Pre-commit Lint
```bash
#!/bin/bash
# .git/hooks/pre-commit

echo "Running pre-commit checks..."

# Run lint
if ! npm run lint; then
    echo "Lint failed. Fix errors before committing."
    exit 1
fi

# Run tests
if ! npm test; then
    echo "Tests failed. Fix errors before committing."
    exit 1
fi

echo "All checks passed!"
```

### Example: Commit Message Validation
```bash
#!/bin/bash
# .git/hooks/commit-msg

COMMIT_MSG=$(cat "$1")
PATTERN="^(feat|fix|docs|style|refactor|test|chore):"

if ! [[ "$COMMIT_MSG" =~ $PATTERN ]]; then
    echo "Invalid commit message format."
    echo "Use: feat: add new feature"
    exit 1
fi
```

## Webhooks

HTTP callbacks triggered by events.

### How Webhooks Work

```
1. User sets up webhook URL at service
2. Event occurs (payment, PR, etc.)
3. Service sends POST request to URL
4. Your server receives and processes
5. Return 200 to acknowledge
```

### Receiving Webhooks

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/webhook/github', methods=['POST'])
def github_webhook():
    payload = request.json
    event = request.headers.get('X-GitHub-Event')
    
    if event == 'push':
        branch = payload['ref']
        # Deploy code
        deploy(branch)
    
    elif event == 'pull_request':
        pr = payload['pull_request']
        # Run CI checks
        run_checks(pr)
    
    return jsonify({'status': 'ok'}), 200
```

### Verifying Webhooks

```python
import hmac
import hashlib

def verify_github_signature(payload, signature, secret):
    expected = 'sha256=' + hmac.new(
        secret.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(expected, signature)

# In route:
if not verify_github_signature(request.data, request.headers.get('X-Hub-Signature-256'), SECRET):
    return 'Invalid signature', 401
```

### Webhook Providers

| Service | Events | Docs |
|---------|--------|------|
| **GitHub** | push, PR, issues | Link |
| **Stripe** | payment, subscription | Link |
| **Slack** | message, reaction | Link |
| **Discord** | message, member | Link |

## Software Hooks

### React Hooks
```tsx
import { useState, useEffect } from 'react';

function Component() {
    const [state, setState] = useState(initialValue);
    
    useEffect(() => {
        // Runs after render
        fetchData();
        return () => cleanup();  // Cleanup on unmount
    }, [dependency]);  // Re-run when dependency changes
    
    return <div>{state}</div>;
}
```

### Observer Pattern
```python
class Hooks:
    def __init__(self):
        self.hooks = {}
    
    def register(self, event, callback):
        if event not in self.hooks:
            self.hooks[event] = []
        self.hooks[event].append(callback)
    
    def trigger(self, event, *args, **kwargs):
        for callback in self.hooks.get(event, []):
            callback(*args, **kwargs)

# Usage
hooks = Hooks()
hooks.register('user_created', lambda u: send_welcome_email(u))
hooks.register('user_created', lambda u: create_default_settings(u))
hooks.trigger('user_created', user)
```

## CI/CD Hooks

### GitHub Actions
```yaml
name: CI
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci
      - run: npm test
      - run: npm run lint
```

### Pre-Merge Hooks
```bash
# Ensure all checks pass before merge
#!/bin/bash
set -e

echo "Running pre-merge checks..."

# Unit tests
npm test

# Integration tests  
npm run test:integration

# Security scan
npm audit --audit-level=moderate

# Build
npm run build

echo "All checks passed. Ready to merge."
```

## Hook Best Practices

### Git Hooks
1. Keep scripts fast (or async)
2. Provide clear error messages
3. Allow bypass (with `--no-verify` for emergencies)
4. Document required hooks

### Webhooks
1. **Respond quickly**: Process async, acknowledge fast
2. **Verify signatures**: Don't trust payloads blindly
3. **Handle retries**: Return 200 quickly, process in queue
4. **Idempotency**: Same event may arrive multiple times

### Hook Security
```python
# Always validate webhook source
def validate_webhook(request, secret):
    # Check IP allowlist
    if request.remote_addr not in ALLOWED_IPS:
        return False
    
    # Verify signature
    if not verify_signature(request, secret):
        return False
    
    return True
```

## Related Concepts

- [[automation]] — Automating with hooks
- [[git]] — Git operations that trigger hooks
- [[events]] — Event-driven architecture
- [[webhooks]] — HTTP webhook patterns

## External Resources

- [Git Hooks Documentation](https://git-scm.com/docs/githooks)
- [Husky](https://typicode.github.io/husky/)
- [GitHub Webhooks](https://docs.github.com/en/webhooks)
- [Webhook Guide](https://webhooks.fyi/)