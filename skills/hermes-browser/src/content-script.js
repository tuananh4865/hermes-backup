// Hermes Browser — Content Script
// Phase 1: Foundation — DOM/ARIA extraction helpers, runs on every page

(function() {
  'use strict';

  // Avoid double-injection
  if (window.__hermes_browser_injected__) return;
  window.__hermes_browser_injected__ = true;

  console.log('[Hermes content] Loaded on', location.hostname);

  // Listen for requests from service worker
  chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
    if (msg.action === 'READ_PAGE') {
      try {
        const result = readPageSummary();
        sendResponse({ ok: true, data: result });
      } catch (err) {
        sendResponse({ ok: false, error: err.message });
      }
      return true; // async
    }

    if (msg.action === 'GET_ARIA_TREE') {
      try {
        const tree = getARIATree();
        sendResponse({ ok: true, data: tree });
      } catch (err) {
        sendResponse({ ok: false, error: err.message });
      }
      return true;
    }

    if (msg.action === 'EXECUTE_JS') {
      try {
        const result = eval(msg.code);
        sendResponse({ ok: true, data: result });
      } catch (err) {
        sendResponse({ ok: false, error: err.message });
      }
      return true;
    }

    return false;
  });

  function readPageSummary() {
    return {
      url: location.href,
      title: document.title,
      text: document.body ? document.body.innerText.slice(0, 5000) : '',
      headings: Array.from(document.querySelectorAll('h1,h2,h3'))
        .slice(0, 20)
        .map(h => ({ tag: h.tagName, text: h.innerText.trim() })),
      links: Array.from(document.querySelectorAll('a[href]'))
        .slice(0, 30)
        .map(a => ({ text: a.innerText.trim().slice(0, 100), href: a.href })),
      forms: Array.from(document.querySelectorAll('form')).length,
      inputs: Array.from(document.querySelectorAll('input,textarea,select')).length,
      buttons: Array.from(document.querySelectorAll('button')).length,
    };
  }

  function getARIATree(maxDepth = 6) {
    function walk(el, depth) {
      if (depth > maxDepth) return null;
      const role = el.getAttribute('role') || el.tagName.toLowerCase();
      const name = el.getAttribute('aria-label') ||
                   el.getAttribute('title') ||
                   (el.innerText || '').trim().slice(0, 80);
      const node = { role, name, tag: el.tagName.toLowerCase() };
      const children = Array.from(el.children).map(c => walk(c, depth + 1)).filter(Boolean);
      if (children.length) node.children = children;
      return node;
    }
    return walk(document.body, 0);
  }

})();
