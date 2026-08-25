// Standalone test: verify WebSocket server works (no Chrome, just Node.js)
const WebSocket = require('ws');

const PORT = 9876;
const SERVER_TYPE = process.argv[2] || 'server'; // 'server' or 'client'

if (SERVER_TYPE === 'server') {
  const wss = new WebSocket.Server({ port: PORT, host: '127.0.0.1' });
  console.log(`WS server listening on ws://127.0.0.1:${PORT}`);

  wss.on('connection', (ws) => {
    console.log('Client connected');
    ws.on('message', (data) => {
      console.log('Received:', data.toString());
      try {
        const msg = JSON.parse(data.toString());
        // Echo with fake result
        ws.send(JSON.stringify({
          jsonrpc: '2.0',
          id: msg.id,
          result: { echo: msg.params, ts: Date.now() },
        }));
      } catch (e) {
        ws.send(JSON.stringify({ error: 'Bad JSON' }));
      }
    });
  });
} else {
  // Test client
  const ws = new WebSocket(`ws://127.0.0.1:${PORT}`);
  ws.on('open', () => {
    console.log('Connected');
    ws.send(JSON.stringify({
      jsonrpc: '2.0', id: 1, method: 'tools/call',
      params: { name: 'navigate', arguments: { url: 'https://example.com' } },
    }));
  });
  ws.on('message', (data) => {
    console.log('Got response:', data.toString());
    ws.close();
    process.exit(0);
  });
  ws.on('error', (e) => {
    console.error('Error:', e.message);
    process.exit(1);
  });
}
