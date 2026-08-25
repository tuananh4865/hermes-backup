// Hermes Browser — Popup logic (Phase 1 stub)
document.addEventListener('DOMContentLoaded', async () => {
  const $version = document.getElementById('version');
  const $status = document.getElementById('status');
  const $statusText = document.getElementById('statusText');

  // Get extension version
  const manifest = chrome.runtime.getManifest();
  $version.textContent = `v${manifest.version}`;

  // Check native host status
  try {
    chrome.runtime.sendNativeMessage('com.hermes.browser_extension', { method: 'ping' },
      (response) => {
        if (chrome.runtime.lastError) {
          $status.className = 'status no';
          $statusText.textContent = 'native host missing';
        } else if (response && response.ok) {
          $status.className = 'status ok';
          $statusText.textContent = 'connected';
        }
      });
  } catch (err) {
    $status.className = 'status no';
    $statusText.textContent = 'check failed';
  }

  document.getElementById('installBtn').addEventListener('click', () => {
    alert('Phase 2 — install script not yet implemented.\nSee: ~/.hermes/skills/hermes-browser/native-host/install.sh');
  });

  document.getElementById('openSideBtn').addEventListener('click', async () => {
    try {
      const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
      if (tab && tab.windowId) {
        await chrome.sidePanel.open({ windowId: tab.windowId });
        window.close();
      }
    } catch (err) {
      alert('Side panel failed: ' + err.message);
    }
  });

  document.getElementById('uninstallBtn').addEventListener('click', () => {
    alert('Phase 2 — uninstall script not yet implemented.');
  });
});
