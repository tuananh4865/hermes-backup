# Native Messaging Protocol — 4-byte LE Length + UTF-8 JSON

> **Reference:** Chrome's official Native Messaging API
> https://developer.chrome.com/docs/extensions/develop/concepts/native-messaging

## Frame Format

Every message exchanged between Chrome and the native host uses this exact frame format:

```
┌────────────────────────────────────────────────────────┐
│  4 bytes              │  UTF-8 JSON message              │
│  Length (LE uint32)  │  Variable length (matches the   │
│                       │  value in the header)            │
└────────────────────────────────────────────────────────┘
        Header                    Body
```

### Example (Node.js)

```js
// WRITE (host → Chrome)
const body = Buffer.from(JSON.stringify({jsonrpc: '2.0', id: 1, result: {ok: true}}), 'utf8');
const header = Buffer.alloc(4);
header.writeUInt32LE(body.length, 0);
process.stdout.write(header);
process.stdout.write(body);

// READ (Chrome → host)
const header = Buffer.alloc(4);
process.stdin.read(header, 0, 4);  // reads exactly 4 bytes
const length = header.readUInt32LE(0);
const body = Buffer.alloc(length);
process.stdin.read(body, 0, length);
const msg = JSON.parse(body.toString('utf8'));
```

### Example (Python)

```python
import struct, json, sys

def read_message():
    raw_length = sys.stdin.buffer.read(4)
    if len(raw_length) < 4:
        return None
    length = struct.unpack('<I', raw_length)[0]
    raw_body = sys.stdin.buffer.read(length)
    if len(raw_body) < length:
        return None
    return json.loads(raw_body.decode('utf-8'))

def send_message(msg):
    body = json.dumps(msg).encode('utf-8')
    sys.stdout.buffer.write(struct.pack('<I', len(body)))
    sys.stdout.buffer.write(body)
    sys.stdout.buffer.flush()
```

## Message Format (JSON-RPC 2.0)

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "navigate",
    "arguments": { "url": "https://example.com" }
  }
}
```

Response:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "url": "https://example.com",
    "title": "Example Domain",
    "ok": true
  }
}
```

Error:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "error": {
    "code": -32603,
    "message": "Failed to navigate: ERR_CONNECTION_REFUSED"
  }
}
```

## Edge Cases

| Case | Behavior |
|---|---|
| Length > 1 MB | Reject — Chrome caps messages at 1 MB |
| Length == 0 | Read 0 bytes — treated as empty body |
| stdin closes | Host should exit gracefully (process.exit(0)) |
| Invalid JSON | Return error code -32700 (Parse error) |
| Method not found | Return error code -32601 (Method not found) |
| Multiple messages | Host should handle them serially (single-threaded) |

## Verification Recipe

Test with a hand-written frame to validate the host:

```bash
# Build a frame with {"jsonrpc":"2.0","id":1,"method":"ping","params":{}}
LEN=$(echo -n '{"jsonrpc":"2.0","id":1,"method":"ping","params":{}}' | wc -c | xargs printf '%08x')
PAYLOAD='{"jsonrpc":"2.0","id":1,"method":"ping","params":{}}'

# Convert hex to 4-byte LE
python3 -c "import struct, sys; sys.stdout.buffer.write(struct.pack('<I', $LEN))" > /tmp/header.bin
echo -n "$PAYLOAD" > /tmp/body.json
cat /tmp/header.bin /tmp/body.json | /Users/tuananh4865/.hermes/node/bin/node \
  /Volumes/Storage-1/Hermes/skills/hermes-browser/native-host/hermes_browser_host.js
```

Expected output: `{"jsonrpc":"2.0","id":1,"result":{"ok":true,...}}`

## Phase Plan

- ✅ **Phase 2 (current):** Ping + status only
- Phase 3: 22 MCP tools (navigate, read_page, computer, etc.)
- Phase 4: Hermes CLI integration (MCP server on stdin)
- Phase 5: Privacy audit + wiki mirror

## Related Files

- `native-host/hermes_browser_host.js` — Node.js implementation (Phase 2)
- `src/service-worker.js` — Chrome extension side (calls this)
- `wiki/concepts/claude-chrome-extension-architecture-2026-08-13.md` — Reference
