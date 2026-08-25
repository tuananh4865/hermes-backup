// Hermes Browser — Side Panel UI logic (Phase 3: tool buttons + output display)

const PANEL_PORT_NAME = 'hermes-panel';

let port = null;
let toolCallCounter = 0;

const $messages = document.getElementById('messages');
const $input = document.getElementById('input');
const $statusDot = document.getElementById('statusDot');
const $statusText = document.getElementById('statusText');
const $hostStatus = document.getElementById('hostStatus');
const $activeTab = document.getElementById('activeTab');
const $extVersion = document.getElementById('extVersion');
const $toolsList = document.getElementById('toolsList');

function setStatus(state, text) {
  $statusDot.className = 'status-dot ' + state;
  $statusText.textContent = text;
}

function appendMessage(role, text, data) {
  const div = document.createElement('div');
  div.className = 'message ' + role;

  const meta = document.createElement('div');
  meta.className = 'meta';
  meta.textContent = new Date().toLocaleTimeString();
  div.appendChild(meta);

  if (text) {
    div.appendChild(document.createTextNode(text));
  }

  if (data !== undefined) {
    const pre = document.createElement('pre');
    pre.style.cssText = 'margin: 6px 0 0; font-size: 11px; white-space: pre-wrap; max-height: 200px; overflow: auto; background: rgba(0,0,0,0.3); padding: 6px; border-radius: 4px;';
    pre.textContent = typeof data === 'string' ? data : JSON.stringify(data, null, 2);
    div.appendChild(pre);
  }

  $messages.appendChild(div);
  $messages.scrollTop = $messages.scrollHeight;
}

function connect() {
  port = chrome.runtime.connect({ name: PANEL_PORT_NAME });
  setStatus('', 'connecting...');

  port.onMessage.addListener((msg) => {
    console.log('[panel] ←', msg);
    switch (msg.type) {
      case 'PONG':
        appendMessage('system', '🔌 PONG received from service worker');
        break;
      case 'STATUS':
        renderStatus(msg);
        break;
      case 'TOOL_RESULT':
        appendMessage('assistant', `✅ ${msg.note || 'Tool result'}`, msg.result);
        break;
      case 'ERROR':
        appendMessage('system', `❌ Error: ${msg.error}`);
        break;
    }
  });

  port.onDisconnect.addListener(() => {
    setStatus('error', 'disconnected');
    setTimeout(connect, 1000);
  });
}

function renderStatus(s) {
  $extVersion.textContent = s.extensionVersion || '—';
  $hostStatus.textContent = s.nativeHostInstalled
    ? `installed (host reachable)`
    : `NOT installed — using direct SW execution`;
  $activeTab.textContent = s.activeTab
    ? `${s.activeTab.title.slice(0, 60)} — ${s.activeTab.url.slice(0, 80)}`
    : '—';
  if ($toolsList) {
    $toolsList.textContent = (s.availableTools || []).join(', ');
  }
  setStatus('connected', `v${s.extensionVersion} (${(s.availableTools || []).length} tools)`);
}

async function sendToolCall(tool, params = {}) {
  if (!port) {
    appendMessage('system', '❌ Not connected to service worker');
    return;
  }
  const id = ++toolCallCounter;
  appendMessage('user', `🔧 ${tool}(${JSON.stringify(params)})`);
  // Try direct first (faster, no native host needed for Phase 3)
  port.postMessage({ type: 'DIRECT_TOOL_CALL', id, tool, params });
}

// === BUTTON HANDLERS ===

document.getElementById('pingBtn').addEventListener('click', () => {
  if (!port) return;
  appendMessage('user', '🔌 PING');
  port.postMessage({ type: 'PING' });
});

document.getElementById('getStatusBtn')?.addEventListener('click', () => {
  if (!port) return;
  port.postMessage({ type: 'GET_STATUS' });
});

// TIER 1 buttons
document.getElementById('tabsBtn')?.addEventListener('click', () => sendToolCall('tabs_context_mcp'));
document.getElementById('readBtn')?.addEventListener('click', () => sendToolCall('read_page'));
document.getElementById('textBtn')?.addEventListener('click', () => sendToolCall('get_page_text'));

// TIER 2 buttons
document.getElementById('navigateBtn')?.addEventListener('click', () => {
  const url = prompt('Navigate to URL:', 'https://example.com');
  if (url) sendToolCall('navigate', { url });
});
document.getElementById('newTabBtn')?.addEventListener('click', () => {
  const url = prompt('New tab URL (blank if empty):', '');
  sendToolCall('tabs_create_mcp', { url: url || 'about:blank', active: true });
});
document.getElementById('closeTabBtn')?.addEventListener('click', () => {
  if (confirm('Close active tab?')) {
    sendToolCall('tabs_close_mcp');
  }
});

document.getElementById('clearBtn').addEventListener('click', () => {
  $messages.innerHTML = '';
  appendMessage('system', '🧹 Cleared. Status panel will refresh below.');
});

$input.addEventListener('keydown', (e) => {
  if (e.key === 'Enter' && $input.value.trim()) {
    const text = $input.value.trim();
    $input.value = '';
    appendMessage('user', text);
    // Free-text: try to parse as "navigate <url>" or "tool <name>"
    const navMatch = text.match(/^(?:navigate|go to|mở|đi tới)\s+(.+)$/i);
    if (navMatch) {
      sendToolCall('navigate', { url: navMatch[1].trim() });
    } else {
      appendMessage('assistant', '🤖 Free-text chat chưa wire tới Hermes CLI (Phase 4). Hiện tại dùng buttons.');
    }
  }
});

connect();
port?.postMessage({ type: 'GET_STATUS' });
