"""Pure CDP client using websockets - no Playwright needed.
Works on any Chrome with --remote-debugging-port.
"""
import asyncio, json, urllib.request, time
import websockets


class Chrome:
    """Minimal CDP client using pure websockets."""

    def __init__(self, ws_url=None, http_base="http://localhost:9222"):
        if ws_url is None:
            data = json.loads(urllib.request.urlopen(f"{http_base}/json/version").read())
            ws_url = data["webSocketDebuggerUrl"]
        self.ws_url = ws_url
        self.ws = None
        self._msg_id = 0
        self._sessions = {}

    async def connect(self):
        self.ws = await websockets.connect(self.ws_url, max_size=10_000_000)
        return self

    async def close(self):
        if self.ws:
            await self.ws.close()

    async def call(self, method, params=None, session_id=None):
        self._msg_id += 1
        msg = {"id": self._msg_id, "method": method, "params": params or {}}
        if session_id:
            msg["sessionId"] = session_id
        await self.ws.send(json.dumps(msg))
        while True:
            raw = await self.ws.recv()
            resp = json.loads(raw)
            if resp.get("id") == self._msg_id:
                if "error" in resp:
                    raise RuntimeError(f"CDP error: {resp['error']}")
                return resp["result"] if "result" in resp else {}

    # === High-level methods ===

    async def get_version(self):
        return await self.call("Browser.getVersion")

    async def get_targets(self):
        r = await self.call("Target.getTargets")
        return r["targetInfos"]

    async def create_target(self, url="about:blank", type_="page"):
        r = await self.call("Target.createTarget", {"url": url, "type": type_})
        return r["targetId"]

    async def attach_to_target(self, target_id, flatten=True):
        r = await self.call("Target.attachToTarget", {"targetId": target_id, "flatten": flatten})
        return r["sessionId"]

    async def new_page_session(self, url=None):
        """Create new page + attach session. Returns (targetId, sessionId)."""
        target_id = await self.create_target(url or "about:blank")
        session_id = await self.attach_to_target(target_id)
        # Enable Page + Network on session
        await self.call("Page.enable", session_id=session_id)
        await self.call("Network.enable", session_id=session_id)
        return target_id, session_id

    async def navigate(self, session_id, url, wait_load=True, timeout=30):
        """Navigate and wait for load."""
        # Set up load waiter
        load_future = asyncio.get_event_loop().create_future()

        def on_event(resp):
            if resp.get("method") == "Page.loadEventFired":
                if not load_future.done():
                    load_future.set_result(True)

        # Listen for events in background
        listener = asyncio.create_task(self._event_listener(on_event, session_id))

        await self.call("Page.navigate", {"url": url}, session_id=session_id)

        if wait_load:
            try:
                await asyncio.wait_for(load_future, timeout=timeout)
            except asyncio.TimeoutError:
                pass
        listener.cancel()

    async def _event_listener(self, callback, session_id):
        """Listen for events matching session_id."""
        try:
            async for raw in self.ws:
                resp = json.loads(raw)
                if resp.get("sessionId") == session_id:
                    callback(resp)
        except (asyncio.CancelledError, websockets.ConnectionClosed):
            pass

    async def get_cookies(self, session_id, urls=None):
        """Get cookies for URLs (or all if None)."""
        params = {}
        if urls:
            params["urls"] = urls if isinstance(urls, list) else [urls]
        r = await self.call("Network.getCookies", params, session_id=session_id)
        return r.get("cookies", [])

    async def evaluate(self, session_id, expression, await_promise=False):
        """Run JS in page context."""
        r = await self.call("Runtime.evaluate", {
            "expression": expression,
            "returnByValue": True,
            "awaitPromise": await_promise,
        }, session_id=session_id)
        if "exceptionDetails" in r:
            return {"error": r["exceptionDetails"], "result": None}
        return r.get("result", {}).get("value")

    async def wait_for_text(self, session_id, selector, timeout=30):
        """Wait for an element matching selector to appear."""
        deadline = time.time() + timeout
        while time.time() < deadline:
            present = await self.evaluate(session_id, f"!!document.querySelector({json.dumps(selector)})")
            if present:
                return True
            await asyncio.sleep(0.5)
        return False

    async def click(self, session_id, selector):
        """Click element matching selector."""
        return await self.evaluate(session_id, f"""
            (() => {{
                const el = document.querySelector({json.dumps(selector)});
                if (el) {{ el.click(); return true; }}
                return false;
            }})()
        """)

    async def type_text(self, session_id, selector, text):
        """Focus element and type text."""
        return await self.evaluate(session_id, f"""
            (() => {{
                const el = document.querySelector({json.dumps(selector)});
                if (el) {{
                    el.focus();
                    el.value = {json.dumps(text)};
                    el.dispatchEvent(new Event('input', {{bubbles: true}}));
                    el.dispatchEvent(new Event('change', {{bubbles: true}}));
                    return true;
                }}
                return false;
            }})()
        """)


# === Example usage ===
async def demo():
    chrome = await Chrome(http_base="http://localhost:9222").connect()

    print("=== Browser version ===")
    v = await chrome.get_version()
    print(f"  {v['product']}")

    print("\n=== Create new page session ===")
    target_id, session_id = await chrome.new_page_session("https://example.com")
    print(f"  Target: {target_id}")
    print(f"  Session: {session_id}")

    print("\n=== Get cookies ===")
    cookies = await chrome.get_cookies(session_id, urls=["https://example.com"])
    print(f"  {len(cookies)} cookies")

    print("\n=== Navigate ===")
    await chrome.navigate(session_id, "https://example.com")
    print("  Done")

    print("\n=== Evaluate JS ===")
    title = await chrome.evaluate(session_id, "document.title")
    print(f"  Title: {title}")

    await chrome.close()


if __name__ == "__main__":
    asyncio.run(demo())
