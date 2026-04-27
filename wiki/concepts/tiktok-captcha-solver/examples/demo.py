"""
Demo script — Cách sử dụng TikTok CAPTCHA Solver
"""

# ============================================================
# CÁCH 1: Dùng Orchestrator (ĐƠN GIẢN NHẤT)
# ============================================================
from tiktok_solver import TikTokCaptchaSolver

solver = TikTokCaptchaSolver(debug=True)

# Mở stealth browser và navigate đến TikTok
url = "https://www.tiktok.com/@someuser/video/1234567890"
result = solver.solve_with_stealth_browser(url, headless=False)

print(f"Result: {result}")


# ============================================================
# CÁCH 2: Dùng với Playwright đã có sẵn
# ============================================================
from playwright.sync_api import sync_playwright
from tiktok_solver import TikTokCaptchaSolver

solver = TikTokCaptchaSolver()

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    
    # Navigate đến TikTok
    page.goto("https://www.tiktok.com")
    
    # Làm gì đó trên page...
    page.wait_for_timeout(2000)
    
    # Kiểm tra và giải CAPTCHA nếu có
    # (hook vào request handler hoặc event listener)
    
    # Hoặc chủ động gọi:
    # solver.solve_and_drag(page, captcha_type="puzzle")
    
    browser.close()


# ============================================================
# CÁCH 3: Dùng riêng từng solver
# ============================================================

# Puzzle Solver
from puzzle_solver import PuzzleSolver

solver = PuzzleSolver()
distance, confidence = solver.solve("background.png", "piece.png")
print(f"Puzzle: kéo {distance}px, confidence {confidence}")

# Rotate Solver
from rotate_solver import RotateSolver

solver = RotateSolver()
distance, angle = solver.solve("inner.png", "outer.png")
print(f"Rotate: góc {angle}°, kéo {distance}px")

# Shapes Solver (cần MiniMax API key)
from shapes_solver import ShapesSolver

solver = ShapesSolver(api_key="YOUR_MINIMAX_KEY")
index, confidence = solver.solve("shapes.png")
print(f"Shapes: chọn object {index}, confidence {confidence}")

# Human Drag
from human_drag import HumanDrag

drag = HumanDrag()
movements = drag.get_mouse_movements(100, 200, 400, 200, 300, 1000)
print(f"Human drag: {len(movements)} steps")


# ============================================================
# CÁCH 4: Anti-CAPTCHA Prevention Setup
# ============================================================
from stealth_browser import StealthBrowser

browser = StealthBrowser(headless=False)
browser.launch()

# Proxy (tùy chọn)
proxy = {
    "server": "http://your-proxy:8080",
    "username": "user",
    "password": "pass"
}

context = browser.new_context()  # với proxy=proxy nếu cần
page = browser.new_page()

page.goto("https://www.tiktok.com")
# Bây giờ TikTok sẽ ít detect bạn hơn

browser.close()


# ============================================================
# CÁCH 5: Kết hợp với TikTokApi
# ============================================================
# Nếu dùng TikTokApi library, bạn có thể hook vào:
# 1. Custom verifyFp handler
# 2. Before/after request hooks

# def custom_captcha_handler(page):
#     solver = TikTokCaptchaSolver()
#     solver.solve_and_drag(page)

# # Hook vào TikTokApi
# api = TikTokApi()
# api._captcha_handler = custom_captcha_handler
