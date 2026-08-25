// Hermes Browser Control — MV3 Service Worker
// Phase 3: Tool dispatch — extension SW does the actual chrome.* API calls,
// native host just relays JSON-RPC frames.
//
// Architecture reference: wiki/concepts/claude-chrome-extension-architecture-2026-08-13.md

const NATIVE_HOST_NAME = 'com.hermes.browser_extension';
const PANEL_PORT_NAME = 'hermes-panel';

// === TOOL DISPATCH (Phase 3 — 5 tools for v0.2.0) ===
// TIER 1 (read-only): tabs_context_mcp, read_page, get_page_text
// TIER 2 (medium): navigate, tabs_create_mcp, tabs_close_mcp
//
// Future: computer (click/type/drag), form_input, find, javascript_tool,
// upload_*, gif_creator — see references/22-tools-spec.md

const handlers = {
  // ============================================================
  // TIER 1: READ-ONLY
  // ============================================================

  tabs_context_mcp: async () => {
    const tabs = await chrome.tabs.query({});
    return {
      tabs: tabs.map((t) => ({
        id: t.id,
        windowId: t.windowId,
        title: t.title || '',
        url: t.url || '',
        active: t.active,
        index: t.index,
        favIconUrl: t.favIconUrl || null,
      })),
      currentWindowId: (await chrome.windows.getCurrent())?.id,
    };
  },

  read_page: async (params = {}) => {
    const tabId = await getActiveTabId();
    if (!tabId) throw new Error('No active tab');

    // Use chrome.scripting.executeScript to call content-script helpers
    try {
      const result = await chrome.scripting.executeScript({
        target: { tabId },
        func: () => {
          // Same logic as content-script READ_PAGE
          return {
            url: location.href,
            title: document.title,
            text: document.body ? document.body.innerText.slice(0, 5000) : '',
            headings: Array.from(document.querySelectorAll('h1,h2,h3'))
              .slice(0, 20)
              .map((h) => ({ tag: h.tagName, text: h.innerText.trim() })),
            links: Array.from(document.querySelectorAll('a[href]'))
              .slice(0, 30)
              .map((a) => ({ text: a.innerText.trim().slice(0, 100), href: a.href })),
            forms: Array.from(document.querySelectorAll('form')).length,
            inputs: Array.from(document.querySelectorAll('input,textarea,select')).length,
            buttons: Array.from(document.querySelectorAll('button')).length,
          };
        },
      });
      return result?.[0]?.result || { error: 'executeScript returned no result' };
    } catch (err) {
      // Chrome internal pages (chrome://, about:) can't be scripted
      return {
        url: null,
        error: 'Cannot read this page (chrome://, about:, or extension page): ' + err.message,
      };
    }
  },

  get_page_text: async () => {
    const tabId = await getActiveTabId();
    if (!tabId) throw new Error('No active tab');

    try {
      const result = await chrome.scripting.executeScript({
        target: { tabId },
        func: () => document.body ? document.body.innerText : '',
      });
      return { text: result?.[0]?.result || '' };
    } catch (err) {
      return { text: '', error: err.message };
    }
  },

  // ============================================================
  // TIER 2: WRITE / NAVIGATION
  // ============================================================

  navigate: async (params = {}) => {
    const { url, tabId } = params;
    if (!url) throw new Error('navigate: url is required');

    // Validate URL — block dangerous schemes
    const parsed = new URL(url);
    if (!['http:', 'https:'].includes(parsed.protocol)) {
      throw new Error(`Refusing to navigate to non-http(s) URL: ${parsed.protocol}`);
    }

    const targetTabId = tabId || await getActiveTabId();
    if (!targetTabId) throw new Error('No active tab to navigate');

    const tab = await chrome.tabs.update(targetTabId, { url });
    return {
      ok: true,
      tabId: tab.id,
      url: tab.url,
      pendingUrl: tab.pendingUrl,
    };
  },

  tabs_create_mcp: async (params = {}) => {
    const { url, active = true } = params;
    const tab = await chrome.tabs.create({ url: url || 'about:blank', active });
    return {
      id: tab.id,
      windowId: tab.windowId,
      url: tab.url || tab.pendingUrl,
      active: tab.active,
    };
  },

  tabs_close_mcp: async (params = {}) => {
    const { tabId } = params;
    const targetTabId = tabId || await getActiveTabId();
    if (!targetTabId) throw new Error('tabs_close_mcp: tabId required');
    await chrome.tabs.remove(targetTabId);
    return { ok: true, closedTabId: targetTabId };
  },
};

// === HELPERS ===

async function getActiveTabId() {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  return tab?.id;
}

// === NATIVE MESSAGING BRIDGE ===
async function callNativeHost(tool, params) {
  if (!chrome.runtime.connectNative) {
    throw new Error('chrome.runtime.connectNative not available');
  }

  return new Promise((resolve, reject) => {
    let port;
    try {
      port = chrome.runtime.connectNative(NATIVE_HOST_NAME);
    } catch (err) {
      reject(new Error(`Native host ${NATIVE_HOST_NAME} not installed. ` +
        `Run: bash ~/.hermes/skills/hermes-browser/native-host/install.sh`));
      return;
    }

    const message = {
      jsonrpc: '2.0',
      id: crypto.randomUUID(),
      method: 'tools/call',
      params: { name: tool, arguments: params || {} }
    };

    let timeout = setTimeout(() => {
      try { port.disconnect(); } catch {}
      reject(new Error('Native host timeout (30s)'));
    }, 30000);

    port.onMessage.addListener((response) => {
      clearTimeout(timeout);
      try { port.disconnect(); } catch {}
      if (response.error) {
        reject(new Error(response.error.message || 'Native host error'));
      } else {
        resolve(response.result || response);
      }
    });

    port.onDisconnect.addListener(() => {
      clearTimeout(timeout);
      if (chrome.runtime.lastError) {
        reject(new Error(`Native host disconnected: ${chrome.runtime.lastError.message}`));
      }
    });

    port.postMessage(message);
  });
}

// === MESSAGE ROUTING ===
// Two paths:
// 1. From side panel via port (long-lived): use chrome.* APIs DIRECTLY (no native host needed)
// 2. From native host (if it ever wants to call back): also handle
//
// This is the SIMPLER pattern vs Claude's:
//   side-panel → SW → native-host → CDP → browser
// Our pattern:
//   side-panel → SW → chrome.* APIs (DIRECT)
//   native-host is just a relay for now (Phase 3 doesn't need CDP)

chrome.runtime.onConnect.addListener((port) => {
  if (port.name !== PANEL_PORT_NAME) return;
  console.log('[Hermes Browser] Side panel connected');

  port.onMessage.addListener(async (msg) => {
    console.log('[Hermes Browser] ← panel:', msg);

    try {
      switch (msg.type) {
        case 'PING':
          port.postMessage({ type: 'PONG', ts: Date.now() });
          break;

        case 'GET_STATUS':
          const status = await getStatus();
          port.postMessage({ type: 'STATUS', ...status });
          break;

        case 'NATIVE_TOOL_CALL':
          // Phase 3: try native host FIRST, then fallback to direct chrome.* API
          try {
            const result = await callNativeHost(msg.tool, msg.params);
            port.postMessage({ type: 'TOOL_RESULT', id: msg.id, result });
          } catch (hostErr) {
            console.warn('[Hermes Browser] Native host failed, trying direct:', hostErr.message);
            // Fallback: call handler directly (works without native host)
            const handler = handlers[msg.tool];
            if (handler) {
              const result = await handler(msg.params || {});
              port.postMessage({
                type: 'TOOL_RESULT', id: msg.id,
                result,
                note: 'Executed by service worker (native host not connected)',
              });
            } else {
              throw new Error(`Tool ${msg.tool} not implemented and native host unreachable: ${hostErr.message}`);
            }
          }
          break;

        // Direct tool call (bypasses native host — useful when host is not installed)
        case 'DIRECT_TOOL_CALL':
          const handler = handlers[msg.tool];
          if (!handler) {
            throw new Error(`Tool ${msg.tool} not implemented`);
          }
          const result = await handler(msg.params || {});
          port.postMessage({ type: 'TOOL_RESULT', id: msg.id, result });
          break;

        default:
          port.postMessage({
            type: 'ERROR', id: msg.id,
            error: `Unknown message type: ${msg.type}`,
          });
      }
    } catch (err) {
      console.error('[Hermes Browser] Error:', err);
      port.postMessage({
        type: 'ERROR', id: msg.id,
        error: err.message || String(err),
      });
    }
  });

  port.onDisconnect.addListener(() => {
    console.log('[Hermes Browser] Side panel disconnected');
  });
});

// === STATUS ===
async function getStatus() {
  const result = {
    extensionVersion: chrome.runtime.getManifest().version,
    availableTools: Object.keys(handlers),
    nativeHostInstalled: false,
    activeTab: null,
  };

  // Check if native host responds (optional)
  try {
    const pong = await Promise.race([
      callNativeHost('ping', {}),
      new Promise((_, rej) => setTimeout(() => rej(new Error('timeout')), 1500))
    ]);
    result.nativeHostInstalled = true;
  } catch {
    result.nativeHostInstalled = false;
  }

  // Get active tab
  try {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    if (tab) {
      result.activeTab = { url: tab.url, title: tab.title, id: tab.id };
    }
  } catch {}

  return result;
}

// === LIFECYCLE ===
chrome.runtime.onInstalled.addListener(async (details) => {
  console.log('[Hermes Browser] onInstalled:', details.reason);
  if (chrome.sidePanel?.setPanelBehavior) {
    await chrome.sidePanel.setPanelBehavior({ openPanelOnActionClick: true });
  }
});

chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  if (msg.type === 'FROM_CONTENT_SCRIPT') {
    chrome.runtime.sendMessage({ type: 'CONTENT_DATA', data: msg.data }).catch(() => {});
  }
  return false;
});

console.log('[Hermes Browser] Service worker v0.2.0 loaded, tools:', Object.keys(handlers).join(', '));
