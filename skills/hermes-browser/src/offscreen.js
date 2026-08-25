// Hermes Browser — Offscreen WebSocket Host
// Runs in offscreen document to host WebSocket server (MV3 extensions can't host
// WS servers directly from Service Worker).
//
// Architecture:
//   Python wrapper (Hermes Agent) → ws://localhost:9876 → THIS FILE
//     → chrome.runtime.sendMessage → Service Worker → chrome.tabs.* etc.
//     → WS response back to Python wrapper
//
// Version: 0.2.0

const WS_PORT = 9876;
let ws = null;
let pendingRequests = new Map();  // id → {resolve, reject, timer}

// Open WebSocket server (only once)
async function startWSServer() {
  // chrome.sockets.tcpServer is a Chrome App API, NOT available in MV3 extensions.
  // We use the native WebSocket API instead — but that makes us a CLIENT, not server.
  // WORKAROUND: We use a tiny "server" via the WebSocket API + accept incoming
  // by polling. Actually that's not possible without a real server.
  //
  // REAL SOLUTION: Use a custom protocol over HTTP via fetch long-polling,
  // OR use a native binary that hosts WebSocket (Node.js does this trivially).
  //
  // Since pure browser WebSocket SERVER is not possible without a server binary,
  // we fall back to: Python wrapper opens TWO connections — one sticky HTTP
  // to upload commands, one WebSocket from a SOCKET SERVER which we'll
  // implement as a separate native host process.
  //
  // For now, this offscreen document just relays messages to/from SW.
  console.log('[Hermes offscreen] Started, waiting for SW messages');

  // Listen for messages from SW
  chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
    if (msg.type === 'WS_CLIENT_REQUEST') {
      // Forward to SW for processing
      chrome.runtime.sendMessage({
        type: 'SW_HANDLE_REQUEST',
        id: msg.id,
        tool: msg.tool,
        params: msg.params,
      }).then((response) => {
        sendResponse(response);
      });
      return true; // async response
    }
  });
}

startWSServer();
