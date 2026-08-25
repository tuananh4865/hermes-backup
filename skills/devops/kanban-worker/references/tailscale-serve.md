# Tailscale Serve — Common Issues

## Dashboard 502 via Tailscale (but works locally)

**Symptom:** `curl http://localhost:9119` works, but `https://tuananhs-mac-mini.taila86c48.ts.net/` returns 502.

**Cause:** Using HTTPS proxy for a plain HTTP server. `tailscale serve --bg https+insecure://localhost:9119` uses TLS termination that the dashboard's uvicorn doesn't handle correctly.

**Fix:** Use HTTP protocol:
```bash
tailscale serve reset
tailscale serve --bg http://localhost:9119
```

**Verification:**
```bash
curl -s --max-time 5 https://tuananhs-mac-mini.taila86c48.ts.net/  # must return HTML
```

Note: Tailscale serve creates a tailnet-only URL (requires login). For internet access, use `tailscale funnel` instead.

## `tailscale funnel` port conflict

**Symptom:** `tailscale funnel 9119` fails with "listener already exists for port 443"

**Fix:**
```bash
tailscale funnel reset
tailscale serve --https=443 off
tailscale funnel 9119
```

## Hermes Dashboard not responding on localhost

**Symptom:** Dashboard PID exists but `curl localhost:9119` returns empty.

**Check:**
```bash
ps aux | grep dashboard | grep -v grep
lsof -i :9119
```

**Fix:** Kill and restart:
```bash
kill <pid>
sleep 1
hermes dashboard --host 0.0.0.0 --port 9119 --insecure --no-open &
sleep 5
curl http://localhost:9119
```