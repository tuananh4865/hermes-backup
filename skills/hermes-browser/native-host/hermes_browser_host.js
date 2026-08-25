// Hermes Browser Control — Native Messaging Host v0.2.0
// Phase 6.5: Hybrid Native Messaging + WebSocket server
//
// BUG DISCOVERED: chrome.runtime.connectNative is ONE-WAY (extension → native host).
// Native host CANNOT call extension. So we need a different approach.
//
// SOLUTION (Phase 6.5): Two-part architecture
// 1. Extension SW opens chrome.runtime.connectNative at startup (keeps port alive)
// 2. Python wrapper connects to ws://localhost:9876 (WE ARE THE WS SERVER)
// 3. Native host bridges WS ↔ Chrome Native Messaging port
//
// IMPORTANT: We act as BOTH:
// - WebSocket server (for Python wrapper to connect)
// - Native messaging host (for Chrome extension to spawn)
//
// Since Chrome spawns native host with stdin/stdout, we need to handle
// BOTH simultaneously:
// - When launched BY CHROME: read commands from stdin, write responses to stdout
// - When launched MANUALLY (for WS server mode): run WS server, no chrome protocol
//
// We detect mode by checking if stdin is a TTY (Chrome uses pipes, manual uses TTY).
//
// Actually, simpler: we ALWAYS run as WS server. The protocol is:
//   Chrome extension SW → opens chrome.runtime.connectNative → Chrome spawns us
//   → we read stdin and write stdout (Chrome protocol)
//   → we ALSO start a WS server in parallel for Python wrapper
//
// This works because:
// - Chrome spawning us gives us stdin/stdout pipes
// - We can ALSO open a WS server on localhost:9876
// - Python wrapper connects to WS server
// - When Python sends a tool call, we put it on stdin (Chrome takes it? no, we need to think)
//
// ACTUAL CORRECT FLOW:
// 1. Chrome extension SW opens chrome.runtime.connectNative() → gives us stdin/stdout
// 2. SW sends a tool call via stdin (Chrome Native Messaging protocol)
// 3. We (this script) execute the tool call OR forward to SW
// 4. We send response back via stdout
//
// But the TOOLS are in SW, not native host. So who calls them?
//
// TRUE PATTERN: SW MUST PROACTIVELY POLL native host for commands
// - SW opens chrome.runtime.connectNative (port open)
// - Native host opens a WebSocket server (ws://localhost:9876)
// - Python wrapper connects to WS, sends tool call
// - Native host writes the tool call to a message queue (in-memory or file)
// - SW uses setInterval/chrome.alarms to poll native host via port.onMessage
// - Native host replies with queued commands
// - SW executes commands, sends results back via port
// - Native host writes results to WS clients
//
// This is the right pattern. Native host is the BRIDGE.
//
// IMPLEMENTATION:
// 1. Native host opens WS server
// 2. Native host opens stdin (Chrome protocol) - SW will push messages
// 3. When SW sends "register" → we acknowledge, idle state
// 4. When Python sends tool call via WS → we send "request" to SW via stdout
// 5. SW processes, sends "response" via stdin
// 6. We forward response to WS client
//
// This works because lowercase:
// - SW initiates connection (chrome.runtime.connectNative)
// - Chrome spawns native host with stdin/stdout
// - We can write to stdout anytime (native host → SW)
// - SW can read from stdin and process
// - We can ALSO run WS server on different port
// - Two-way communication achieved!
//
// LIMITATION: SW MUST keep the port open. If SW times out (5 min idle),
// Chrome kills the native host. We need to use chrome.alarms to keep SW alive.

const PORT = 9876;
const WS_HOST = '127.0.0.1';

let wsServer = null;
let wsClients = new Set();
let pendingRequests = new Map();  // id → ws that asked
let swReady = false;

// === Chrome Native Messaging Protocol (stdin/stdout) ===
function readFrame() {
  return new Promise((resolve, reject) => {
    const header = Buffer.alloc(4);
    let headerDone = 0;

    const onData = (chunk) => {
      if (headerDone < 4) {
        const need = 4 - headerDone;
        const take = Math.min(chunk.length, need);
        chunk.copy(header, headerDone, 0, take);
        headerDone += take;
        if (headerDone < 4) return;
        if (headerDone === 4) {
          const length = header.readUInt32LE(0);
          if (length > 1024 * 1024) {
            return reject(new Error(`Message too long: ${length}`));
          }
          // Read body next
          handleBody(length, chunk.slice(take));
        }
      }
    };

    const handleBody = (length, leftover) => {
      let body = leftover;
      const onMoreData = (chunk) => {
        body = Buffer.concat([body, chunk]);
        if (body.length >= length) {
          process.stdin.removeListener('readable', onMoreData);
          const msg = body.slice(0, length).toString('utf8');
          resolve(msg);
        }
      };
      process.stdin.on('readable', onMoreData);
      // Drain any buffered
      const chunk = process.stdin.read();
      if (chunk) onMoreData(chunk);
    };

    process.stdin.on('readable', () => {
      const chunk = process.stdin.read();
      if (chunk) onData(chunk);
    });
  });
}

function sendMessage(msg) {
  const body = Buffer.from(JSON.stringify(msg), 'utf8');
  const header = Buffer.alloc(4);
  header.writeUInt32LE(body.length, 0);
  process.stdout.write(header);
  process.stdout.write(body);
}

// === WebSocket Server ===
async function startWSServer() {
  const WebSocket = require('ws');
  wsServer = new WebSocket.Server({ port: PORT, host: WS_HOST });

  return new Promise((resolve, reject) => {
    wsServer.on('listening', () => {
      console.error(`[Hermes WS] Listening on ws://${WS_HOST}:${PORT}`);
      resolve();
    });

    wsServer.on('error', (err) => {
      console.error(`[Hermes WS] Server error: ${err.message}`);
      reject(err);
    });

    wsServer.on('connection', (ws) => {
      console.error('[Hermes WS] Client connected');
      wsClients.add(ws);

      ws.on('message', (data) => {
        try {
          const msg = JSON.parse(data.toString());
          if (msg.method === 'tools/call') {
            // Forward to SW via Chrome Native Messaging port
            forwardToSW(msg).then((response) => {
              ws.send(JSON.stringify(response));
            }).catch((err) => {
              ws.send(JSON.stringify({
                jsonrpc: '2.0',
                id: msg.id,
                error: { code: -32603, message: err.message },
              }));
            });
          } else if (msg.method === 'ping') {
            ws.send(JSON.stringify({
              jsonrpc: '2.0', id: msg.id, result: { ok: true, ts: Date.now() },
            }));
          } else if (msg.method === 'status') {
            ws.send(JSON.stringify({
              jsonrpc: '2.0', id: msg.id,
              result: { host: 'com.hermes.browser_extension', v0_2_0: true, swReady },
            }));
          } else {
            ws.send(JSON.stringify({
              jsonrpc: '2.0', id: msg.id,
              error: { code: -32601, message: `Method not found: ${msg.method}` },
            }));
          }
        } catch (e) {
          console.error('[Hermes WS] Bad message:', e.message);
        }
      });

      ws.on('close', () => {
        console.error('[Hermes WS] Client disconnected');
        wsClients.delete(ws);
      });

      ws.on('error', (err) => {
        console.error('[Hermes WS] Client error:', err.message);
        wsClients.delete(ws);
      });
    });
  });
}

// === Forward to Service Worker via Chrome Native Messaging ===
const requestCallbacks = new Map();
let nextRequestId = 1;

async function forwardToSW(request) {
  if (!swReady) {
    return {
      jsonrpc: '2.0',
      id: request.id,
      error: { code: -32603, message: 'Extension Service Worker not connected. Load Hermes Browser Control extension in Chrome first.' },
    };
  }

  return new Promise((resolve) => {
    const id = request.id;
    requestCallbacks.set(id, resolve);
    sendMessage({
      jsonrpc: '2.0',
      id: id,
      method: 'tools/call',
      params: request.params,
    });

    // Timeout after 10s
    setTimeout(() => {
      if (requestCallbacks.has(id)) {
        requestCallbacks.delete(id);
        resolve({
          jsonrpc: '2.0',
          id: id,
          error: { code: -32603, message: 'Service Worker timeout' },
        });
      }
    }, 10000);
  });
}

// === Main loop: read from stdin (Chrome Native Messaging) ===
async function main() {
  console.error(`[${HOST_NAME}] Starting v0.2.0 (PID ${process.pid})`);

  // Start WebSocket server FIRST
  try {
    await startWSServer();
  } catch (err) {
    console.error(`[${HOST_NAME}] Failed to start WS server: ${err.message}`);
    // Continue — might be in pure Chrome mode
  }

  // Set up stdin handlers for Chrome Native Messaging
  process.stdin.on('end', () => {
    console.error(`[${HOST_NAME}] Chrome closed stdin`);
    // Keep WS server alive even if Chrome disconnects
  });

  process.stdin.on('error', (err) => {
    console.error(`[${HOST_NAME}] stdin error:`, err.message);
  });

  // Read messages from Chrome (SW pushes tool results + registrations)
  while (true) {
    try {
      const raw = await readFrame();
      const msg = JSON.parse(raw);

      if (msg.method === 'register') {
        // SW registered itself
        swReady = true;
        console.error(`[${HOST_NAME}] Service Worker registered`);
        sendMessage({ jsonrpc: '2.0', id: msg.id, result: { ok: true } });
      } else if (msg.method === 'tools/result') {
        // SW returned a tool result
        const cb = requestCallbacks.get(msg.id);
        if (cb) {
          requestCallbacks.delete(msg.id);
          cb({
            jsonrpc: '2.0',
            id: msg.id,
            result: msg.result,
          });
        }
      } else {
        // Unknown message from SW
        console.error(`[${HOST_NAME}] Unknown message from SW:`, msg.method);
      }
    } catch (err) {
      console.error(`[${HOST_NAME}] Error reading stdin:`, err.message);
    }
  }
}

const HOST_NAME = 'com.hermes.browser_extension';
main();
