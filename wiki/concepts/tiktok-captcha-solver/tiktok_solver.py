"""
TikTok CAPTCHA Solver — Orchestrator
Tự động nhận diện và giải tất cả các loại TikTok CAPTCHA
"""

import os
import time
import base64
from typing import Optional, Tuple
from pathlib import Path
from io import BytesIO

from puzzle_solver import PuzzleSolver
from rotate_solver import RotateSolver
from shapes_solver import ShapesSolver
from human_drag import HumanDrag, human_drag as perform_human_drag
from stealth_browser import StealthBrowser


class TikTokCaptchaSolver:
    """
    Orchestrator class giải tất cả TikTok CAPTCHA types.
    
    Supported types:
    - puzzle: Puzzle slider (OpenCV)
    - rotate: Rotate image (OpenCV)
    - shapes: 3D shapes (MiniMax Vision)
    - object: Object verification (MiniMax Vision)
    """
    
    # DOM selectors cho TikTok CAPTCHA elements
    CAPTCHA_SELECTORS = {
        "container": ".captcha-verify-container, .captcha_verify_container, #captcha_container",
        "puzzle_bg": "img.sc-fjd, img.captcha-bg",
        "puzzle_piece": "img.sc-cSHVUG, img.puzzle-piece",
        "rotate_inner": "img.sc-fjdhpX",  
        "rotate_outer": "img.sc-jTzLTM",
        "slider": "#secsdk-captcha-drag-wrapper > div",
        "slider_bar": ".secsdk-captcha-drag-slider",
    }
    
    def __init__(self, debug: bool = False):
        self.debug = debug
        self.puzzle_solver = PuzzleSolver()
        self.puzzle_solver.debug = debug
        self.rotate_solver = RotateSolver()
        self.shapes_solver = ShapesSolver()
        self.human_drag = HumanDrag()
        
        # Temp directory for screenshots
        self.temp_dir = Path("/tmp/tiktok_captcha")
        self.temp_dir.mkdir(exist_ok=True)
    
    def solve_and_drag(self, page, captcha_type: str = None, 
                      slider_element = None) -> bool:
        """
        Giải CAPTCHA và thực hiện drag.
        
        Args:
            page: Playwright page object
            captcha_type: Loại CAPTCHA ("puzzle", "rotate", "shapes", "object")
                       Nếu None, tự nhận diện
            slider_element: Slider element handle (nếu None, tự tìm)
            
        Returns:
            True nếu thành công
        """
        # Nhận diện CAPTCHA type
        if captcha_type is None:
            captcha_type = self._detect_captcha_type(page)
        
        print(f"[TikTokSolver] Detected CAPTCHA type: {captcha_type}")
        
        # Tìm slider element
        if slider_element is None:
            slider_element = self._find_slider(page)
        
        if slider_element is None:
            print("[TikTokSolver] ERROR: Cannot find slider element")
            return False
        
        # Giải theo loại
        if captcha_type == "puzzle":
            return self._solve_puzzle(page, slider_element)
        elif captcha_type == "rotate":
            return self._solve_rotate(page, slider_element)
        elif captcha_type in ("shapes", "object"):
            return self._solve_shapes(page, slider_element)
        else:
            print(f"[TikTokSolver] Unknown CAPTCHA type: {captcha_type}")
            return False
    
    def _detect_captcha_type(self, page) -> str:
        """Nhận diện loại CAPTCHA."""
        # Check URL patterns hoặc DOM elements
        try:
            # Thử kiểm tra các element đặc trưng
            puzzle_bg = page.query_selector("img.captcha-bg, img.sc-fjd")
            if puzzle_bg:
                return "puzzle"
            
            rotate_inner = page.query_selector("img.sc-fjdhpX")
            if rotate_inner:
                return "rotate"
            
            shapes = page.query_selector(".captcha-shapes, .shapes-container")
            if shapes:
                return "shapes"
            
            # Default
            return "puzzle"
            
        except Exception as e:
            print(f"[TikTokSolver] Detection error: {e}")
            return "puzzle"
    
    def _find_slider(self, page) -> Optional:
        """Tìm slider element."""
        selectors = [
            "#secsdk-captcha-drag-wrapper > div",
            ".secsdk-captcha-drag-slider",
            ".captcha-slider",
            '[class*="drag"]'
        ]
        
        for selector in selectors:
            try:
                element = page.query_selector(selector)
                if element:
                    return element
            except:
                pass
        
        return None
    
    def _solve_puzzle(self, page, slider_element) -> bool:
        """
        Giải puzzle slider CAPTCHA.
        """
        print("[TikTokSolver] Solving puzzle slider...")
        
        try:
            # 1. Extract images
            bg_path = self.temp_dir / "puzzle_bg.png"
            piece_path = self.temp_dir / "puzzle_piece.png"
            
            # Find background image
            bg_img = page.query_selector("img.captcha-bg, img.sc-fjd")
            if bg_img:
                bg_img.screenshot(str(bg_path))
            
            # Find piece image
            piece_img = page.query_selector("img.puzzle-piece, img.sc-cSHVUG")
            if piece_img:
                piece_img.screenshot(str(piece_path))
            
            # 2. Solve
            drag_distance, conf = self.puzzle_solver.solve(
                str(bg_path), str(piece_path)
            )
            
            print(f"[TikTokSolver] Puzzle solved: distance={drag_distance}, conf={conf:.2f}")
            
            # 3. Human-like drag
            self._perform_slider_drag(page, slider_element, drag_distance)
            
            # Wait for verification
            time.sleep(2)
            
            return True
            
        except Exception as e:
            print(f"[TikTokSolver] Puzzle solve error: {e}")
            return False
    
    def _solve_rotate(self, page, slider_element) -> bool:
        """
        Giải rotate CAPTCHA.
        """
        print("[TikTokSolver] Solving rotate CAPTCHA...")
        
        try:
            # 1. Extract images
            inner_path = self.temp_dir / "rotate_inner.png"
            outer_path = self.temp_dir / "rotate_outer.png"
            
            inner_img = page.query_selector("img.sc-fjdhpX")
            if inner_img:
                inner_img.screenshot(str(inner_path))
            
            outer_img = page.query_selector("img.sc-jTzLTM")
            if outer_img:
                outer_img.screenshot(str(outer_path))
            
            # 2. Solve
            drag_distance, angle = self.rotate_solver.solve(
                str(inner_path), str(outer_path)
            )
            
            print(f"[TikTokSolver] Rotate solved: angle={angle:.2f}, distance={drag_distance}")
            
            # 3. Human-like drag
            self._perform_slider_drag(page, slider_element, drag_distance)
            
            time.sleep(2)
            
            return True
            
        except Exception as e:
            print(f"[TikTokSolver] Rotate solve error: {e}")
            return False
    
    def _solve_shapes(self, page, slider_element) -> bool:
        """
        Giải 3D shapes CAPTCHA bằng Vision.
        
        NOTE: Cần hook vào MiniMax Vision API thực tế.
        """
        print("[TikTokSolver] Solving 3D shapes CAPTCHA...")
        
        try:
            # 1. Screenshot toàn bộ CAPTCHA container
            captcha_path = self.temp_dir / "shapes_captcha.png"
            
            container = page.query_selector(".captcha-verify-container")
            if container:
                container.screenshot(str(captcha_path))
            else:
                page.screenshot(path=str(captcha_path))
            
            # 2. Solve bằng Vision
            object_index, conf = self.shapes_solver.solve(str(captcha_path))
            
            print(f"[TikTokSolver] Shapes solved: index={object_index}, conf={conf:.2f}")
            
            # 3. Click vào object đúng
            shape_elements = page.query_selector_all(".shape-option, .captcha-shape")
            if object_index < len(shape_elements):
                shape_elements[object_index].click()
            
            time.sleep(1)
            
            # 4. Sau đó thực hiện slider verification (nếu cần)
            # TikTok thường yêu cầu thêm slider sau khi chọn shapes
            
            return True
            
        except Exception as e:
            print(f"[TikTokSolver] Shapes solve error: {e}")
            return False
    
    def _perform_slider_drag(self, page, slider_element, distance: int):
        """
        Thực hiện slider drag với human-like movement.
        """
        # Get slider bounding box
        bbox = slider_element.bounding_box()
        if not bbox:
            print("[TikTokSolver] Cannot get slider bounding box")
            return
        
        start_x = bbox["x"] + bbox["width"] / 2
        start_y = bbox["y"] + bbox["height"] / 2
        end_x = start_x + distance
        
        # Generate human-like path
        movements = self.human_drag.get_mouse_movements(
            start_x, start_y, end_x, start_y, distance,
            duration_ms=1000
        )
        
        # Execute
        page.mouse.move(start_x, start_y)
        page.mouse.down()
        
        for x, y, delay in movements[1:]:
            page.mouse.move(x, y)
            time.sleep(delay)
        
        page.mouse.up()
        
        print(f"[TikTokSolver] Dragged {distance}px with human-like movement")
    
    def wait_for_captcha(self, page, timeout: int = 30000) -> bool:
        """
        Chờ và tự động giải CAPTCHA khi xuất hiện.
        
        Args:
            page: Playwright page
            timeout: Timeout in milliseconds
            
        Returns:
            True if CAPTCHA was solved
        """
        from playwright.sync_api import TimeoutError as PlaywrightTimeout
        
        selectors = list(self.CAPTCHA_SELECTORS["container"].split(", "))
        
        try:
            # Wait for CAPTCHA to appear
            page.wait_for_selector(selectors[0], timeout=timeout)
            
            print("[TikTokSolver] CAPTCHA detected!")
            
            # Solve it
            return self.solve_and_drag(page)
            
        except PlaywrightTimeout:
            print("[TikTokSolver] No CAPTCHA appeared within timeout")
            return True  # No CAPTCHA = success
    
    def solve_with_stealth_browser(
        self,
        url: str,
        headless: bool = False,
        proxy: dict = None
    ) -> bool:
        """
        Mở TikTok với stealth browser và giải CAPTCHA.
        
        Args:
            url: TikTok URL
            headless: Run headless
            proxy: Proxy config
            
        Returns:
            True if successful
        """
        browser = StealthBrowser(headless=headless, proxy=proxy)
        
        try:
            browser.launch()
            page = browser.new_page()
            
            # Navigate
            page.goto(url)
            
            # Wait and solve CAPTCHA
            result = self.wait_for_captcha(page)
            
            return result
            
        finally:
            browser.close()


def demo():
    """Demo sử dụng."""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python tiktok_solver.py <tiktok_url>")
        print("   hoặc dùng class trực tiếp:")
        print("   from tiktok_solver import TikTokCaptchaSolver")
        return
    
    solver = TikTokCaptchaSolver(debug=True)
    solver.solve_with_stealth_browser(sys.argv[1])


if __name__ == "__main__":
    demo()
