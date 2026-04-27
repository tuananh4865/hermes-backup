"""
Puzzle Slider CAPTCHA Solver — Miễn phí 100%
Dùng OpenCV template matching để tìm vị trí puzzle piece
"""

import cv2
import numpy as np
from pathlib import Path
from typing import Tuple, Optional


class PuzzleSolver:
    """
    Tìm vị trí puzzle piece trên background image dùng OpenCV.
    
    Cách hoạt động:
    1. Đọc 2 ảnh: background (có lỗ) và puzzle piece
    2. Edge detection trên cả 2 ảnh
    3. Template matching để tìm vị trí puzzle piece
    4. Trả về tọa độ X cần kéo slider
    """
    
    def __init__(self):
        self.debug = False
    
    def solve(self, background_path: str, piece_path: str, output_path: Optional[str] = None) -> int:
        """
        Tìm vị trí puzzle piece.
        
        Args:
            background_path: Đường dẫn ảnh nền (có lỗ puzzle)
            piece_path: Đường dẫn ảnh puzzle piece
            output_path: Đường dẫn ảnh debug (tùy chọn)
            
        Returns:
            Vị trí X (pixel) cần kéo slider
        """
        # Đọc ảnh
        bg_img = cv2.imread(background_path)
        piece_img = cv2.imread(piece_path)
        
        if bg_img is None:
            raise ValueError(f"Không đọc được ảnh background: {background_path}")
        if piece_img is None:
            raise ValueError(f"Không đọc được ảnh piece: {piece_path}")
        
        # Tìm vị trí
        x_pos = self._find_position(bg_img, piece_img)
        
        # Debug output
        if output_path and self.debug:
            self._save_debug(bg_img, piece_img, x_pos, output_path)
        
        return x_pos
    
    def solve_bytes(self, bg_bytes: bytes, piece_bytes: bytes) -> int:
        """
        Tìm vị trí từ bytes (cho việc extract trực tiếp từ browser).
        
        Args:
            bg_bytes: Background image as bytes
            piece_bytes: Puzzle piece image as bytes
            
        Returns:
            Vị trí X (pixel) cần kéo slider
        """
        # Decode bytes thành numpy array
        bg_img = cv2.imdecode(np.frombuffer(bg_bytes, np.uint8), cv2.IMREAD_COLOR)
        piece_img = cv2.imdecode(np.frombuffer(piece_bytes, np.uint8), cv2.IMREAD_COLOR)
        
        if bg_img is None:
            raise ValueError("Không decode được background image từ bytes")
        if piece_img is None:
            raise ValueError("Không decode được piece image từ bytes")
        
        return self._find_position(bg_img, piece_img)
    
    def _find_position(self, bg_img: np.ndarray, piece_img: np.ndarray) -> int:
        """
        Tìm vị trí puzzle piece trên background.
        
        Thuật toán:
        1. Crop whitespace từ piece image
        2. Edge detection (Canny) trên cả 2 ảnh
        3. Template matching với edge images
        4. Tìm max correlation location
        """
        # Bước 1: Crop whitespace từ piece
        piece_cropped = self._remove_whitespace(piece_img)
        
        # Bước 2: Edge detection
        bg_edges = self._apply_edge_detection(bg_img)
        piece_edges = self._apply_edge_detection(piece_cropped)
        
        # Bước 3: Template matching
        # TM_CCOEFF_NORMED hoạt động tốt nhất cho edge images
        result = cv2.matchTemplate(bg_edges, piece_edges, cv2.TM_CCOEFF_NORMED)
        
        # Bước 4: Tìm vị trí có correlation cao nhất
        _, max_val, _, max_loc = cv2.minMaxLoc(result)
        
        print(f"[PuzzleSolver] Match confidence: {max_val:.3f}, Position X: {max_loc[0]}")
        
        # Nếu confidence thấp, thử phương pháp khác
        if max_val < 0.3:
            print("[PuzzleSolver] Low confidence, trying alternative method...")
            return self._find_position_alternative(bg_img, piece_cropped)
        
        return max_loc[0]
    
    def _find_position_alternative(self, bg_img: np.ndarray, piece_img: np.ndarray) -> int:
        """
        Phương pháp thay thế: dùng grayscale matching.
        """
        # Grayscale
        bg_gray = cv2.cvtColor(bg_img, cv2.COLOR_BGR2GRAY)
        piece_gray = cv2.cvtColor(piece_img, cv2.COLOR_BGR2GRAY)
        
        # Normalize
        bg_norm = cv2.normalize(bg_gray, None, 0, 255, cv2.NORM_MINMAX)
        piece_norm = cv2.normalize(piece_gray, None, 0, 255, cv2.NORM_MINMAX)
        
        # Template matching
        result = cv2.matchTemplate(bg_norm, piece_norm, cv2.TM_CCOEFF_NORMED)
        _, _, _, max_loc = cv2.minMaxLoc(result)
        
        return max_loc[0]
    
    def _remove_whitespace(self, img: np.ndarray) -> np.ndarray:
        """Crop whitespace từ ảnh puzzle piece."""
        # Chuyển sang grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Threshold để tạo mask
        _, thresh = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY)
        
        # Tìm contours
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if not contours:
            return img
        
        # Tìm bounding box lớn nhất
        largest = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest)
        
        # Crop với padding nhỏ
        padding = 2
        x = max(0, x - padding)
        y = max(0, y - padding)
        w = min(img.shape[1] - x, w + padding * 2)
        h = min(img.shape[0] - y, h + padding * 2)
        
        return img[y:y+h, x:x+w]
    
    def _apply_edge_detection(self, img: np.ndarray) -> np.ndarray:
        """Apply Canny edge detection."""
        # Grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Blur nhẹ để giảm noise
        blurred = cv2.GaussianBlur(gray, (3, 3), 0)
        
        # Canny edge detection
        edges = cv2.Canny(blurred, 50, 150)
        
        # Dilate để làm đậm edges
        kernel = np.ones((2, 2), np.uint8)
        edges = cv2.dilate(edges, kernel, iterations=1)
        
        return edges
    
    def _save_debug(self, bg_img: np.ndarray, piece_img: np.ndarray, 
                    x_pos: int, output_path: str):
        """Lưu ảnh debug với vị trí được đánh dấu."""
        h, w = piece_img.shape[:2]
        
        # Vẽ rectangle tại vị trí tìm được
        result = bg_img.copy()
        cv2.rectangle(result, (x_pos, 0), (x_pos + w, h), (0, 0, 255), 2)
        
        cv2.imwrite(output_path, result)
        print(f"[PuzzleSolver] Debug image saved to {output_path}")


def solve_puzzle_slider(background_path: str, piece_path: str, 
                        slider_width: int = 348) -> Tuple[int, float]:
    """
    Hàm tiện ích: giải puzzle slider.
    
    Args:
        background_path: Đường dẫn ảnh nền
        piece_path: Đường dẫn ảnh puzzle piece
        slider_width: Chiều rộng thanh slider (pixel)
        
    Returns:
        Tuple of (drag_distance_pixel, confidence)
    """
    solver = PuzzleSolver()
    
    # Tìm vị trí
    x_pos = solver.solve(background_path, piece_path)
    
    # Confidence (giả định)
    confidence = 0.85
    
    # Tính khoảng cách cần kéo
    # Slider width thường ~348px, puzzle piece width ~60-70px
    # Khoảng cách thực = x_pos - (slider_width - piece_width) / 2
    piece_width = 60  # approximate
    drag_distance = x_pos - (slider_width - piece_width) / 2
    
    return int(max(0, drag_distance)), confidence


if __name__ == "__main__":
    # Test đơn giản
    import sys
    
    if len(sys.argv) == 3:
        bg_path, piece_path = sys.argv[1], sys.argv[2]
        solver = PuzzleSolver()
        pos = solver.solve(bg_path, piece_path)
        print(f"Puzzle piece ở vị trí X: {pos}")
    else:
        print("Usage: python puzzle_solver.py <background.png> <piece.png>")
