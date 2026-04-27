"""
Rotate CAPTCHA Solver — Miễn phí 100%
Dùng OpenCV HoughCircles + template matching để tìm góc xoay
"""

import cv2
import numpy as np
from typing import Tuple, Optional


class RotateSolver:
    """
    Tìm góc xoay để khớp inner circle với outer image.
    
    Cách hoạt động:
    1. Đọc inner circle và outer image (đã crop từ screenshot)
    2. HoughCircles tìm tâm vòng tròn inner
    3. Tìm feature points trên inner và outer
    4. Tính góc lệch giữa 2 ảnh
    5. Trả về khoảng cách pixel cần kéo
    """
    
    def __init__(self):
        self.pixel_per_degree = 0.65  # Thực nghiệm cho TikTok
        self.drag_multiplier = 2.1     # Thực nghiệm
    
    def solve(self, inner_path: str, outer_path: str, 
             slider_width: int = 348) -> Tuple[int, float]:
        """
        Tìm khoảng cách cần kéo để xoay ảnh.
        
        Args:
            inner_path: Đường dẫn ảnh inner circle
            outer_path: Đường dẫn ảnh outer (có lỗ tròn)
            slider_width: Chiều rộng thanh slider
            
        Returns:
            Tuple of (drag_distance_pixel, angle_degrees)
        """
        # Đọc ảnh
        inner = cv2.imread(inner_path)
        outer = cv2.imread(outer_path)
        
        if inner is None:
            raise ValueError(f"Không đọc được inner image: {inner_path}")
        if outer is None:
            raise ValueError(f"Không đọc được outer image: {outer_path}")
        
        return self.solve_from_arrays(inner, outer, slider_width)
    
    def solve_from_arrays(self, inner: np.ndarray, outer: np.ndarray,
                         slider_width: int = 348) -> Tuple[int, float]:
        """
        Tìm khoảng cách từ numpy arrays.
        
        Args:
            inner: Inner circle image array
            outer: Outer image array
            slider_width: Chiều rộng thanh slider
            
        Returns:
            Tuple of (drag_distance_pixel, angle_degrees)
        """
        # Tìm tâm vòng tròn
        center = self._find_circle_center(inner)
        
        # Tìm góc xoay bằng template matching
        angle = self._find_rotation_angle(inner, outer, center)
        
        # Chuyển góc sang pixel
        drag_distance = self._angle_to_drag(angle, slider_width)
        
        print(f"[RotateSolver] Angle: {angle:.2f}°, Drag: {drag_distance}px")
        
        return drag_distance, angle
    
    def _find_circle_center(self, img: np.ndarray) -> Tuple[int, int, int]:
        """
        Tìm tâm vòng tròn dùng HoughCircles.
        
        Returns:
            Tuple of (x, y, radius)
        """
        # Grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Apply slight blur
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # HoughCircles
        circles = cv2.HoughCircles(
            blurred,
            cv2.HOUGH_GRADIENT,
            dp=1,
            minDist=20,
            param1=50,
            param2=30,
            minRadius=0,
            maxRadius=0
        )
        
        if circles is None or len(circles) == 0:
            # Fallback: dùng tâm ảnh
            h, w = img.shape[:2]
            print("[RotateSolver] HoughCircles failed, using image center")
            return w // 2, h // 2, min(w, h) // 2
        
        # Lấy circle lớn nhất
        circle = circles[0][0]
        x, y, r = np.round(circle).astype(int)
        
        print(f"[RotateSolver] Found circle at ({x}, {y}) with radius {r}")
        
        return x, y, r
    
    def _find_rotation_angle(self, inner: np.ndarray, outer: np.ndarray,
                             center: Tuple[int, int, int]) -> float:
        """
        Tìm góc xoay bằng cách so sánh inner với outer.
        
        Thuật toán:
        1. Crop vùng inner từ outer (đã crop lỗ tròn)
        2. Tìm features (ORB/BRISK) trên cả 2 ảnh
        3. Match features
        4. Tính góc từ matches
        """
        x, y, r = center
        
        # Resize inner để match với kích thước crop từ outer
        inner_resized = cv2.resize(inner, (r * 2, r * 2), interpolation=cv2.INTER_AREA)
        
        # Grayscale
        inner_gray = cv2.cvtColor(inner_resized, cv2.COLOR_BGR2GRAY)
        outer_gray = cv2.cvtColor(outer, cv2.COLOR_BGR2GRAY)
        
        # Detect ORB features
        orb = cv2.ORB_create(nfeatures=100)
        kp1, des1 = orb.detectAndCompute(inner_gray, None)
        kp2, des2 = orb.detectAndCompute(outer_gray, None)
        
        if des1 is None or des2 is None or len(des1) < 3 or len(des2) < 3:
            # Fallback: dùng template matching đơn giản
            return self._angle_by_template_matching(inner_resized, outer)
        
        # Match features
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        matches = bf.match(des1, des2)
        
        if len(matches) < 3:
            return self._angle_by_template_matching(inner_resized, outer)
        
        # Sắp xếp matches theo khoảng cách
        matches = sorted(matches, key=lambda x: x.distance)[:10]
        
        # Tính góc trung bình từ các matches
        angles = []
        for match in matches:
            pt1 = kp1[match.queryIdx].pt
            pt2 = kp2[match.trainIdx].pt
            
            # Tính góc từ tâm
            angle = np.degrees(np.arctan2(pt2[1] - pt1[1], pt2[0] - pt1[0]))
            angles.append(angle)
        
        median_angle = np.median(angles)
        
        # Normalize angle
        if median_angle < 0:
            median_angle = abs(median_angle)
        
        return float(median_angle)
    
    def _angle_by_template_matching(self, inner: np.ndarray, outer: np.ndarray) -> float:
        """
        Fallback: Template matching để tìm góc.
        """
        inner_gray = cv2.cvtColor(inner, cv2.COLOR_BGR2GRAY)
        outer_gray = cv2.cvtColor(outer, cv2.COLOR_BGR2GRAY)
        
        # Try multiple rotations of inner and find best match
        best_angle = 0
        best_match = 0
        
        for angle in range(-180, 180, 5):
            # Rotate inner
            h, w = inner_gray.shape[:2]
            center_pt = (w // 2, h // 2)
            M = cv2.getRotationMatrix2D(center_pt, angle, 1.0)
            rotated = cv2.warpAffine(inner_gray, M, (w, h))
            
            # Template match
            result = cv2.matchTemplate(outer_gray, rotated, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, _ = cv2.minMaxLoc(result)
            
            if max_val > best_match:
                best_match = max_val
                best_angle = angle
        
        print(f"[RotateSolver] Template matching: angle={best_angle}, match={best_match:.3f}")
        
        return float(best_angle)
    
    def _angle_to_drag(self, angle: float, slider_width: int = 348) -> int:
        """
        Chuyển góc xoay sang khoảng cách pixel cần kéo.
        
        Args:
            angle: Góc xoay (degrees)
            slider_width: Chiều rộng thanh slider
            
        Returns:
            Khoảng cách pixel cần kéo
        """
        # TikTok slider: full rotation ~360° = ~slider_width pixels
        # Nhưng thực tế cần calibrate
        
        # Tính khoảng cách
        drag = abs(angle) * self.pixel_per_degree * self.drag_multiplier
        
        # Giới hạn trong slider width
        max_drag = slider_width - 55  # 55 = button width
        drag = min(drag, max_drag)
        
        return int(drag)


def solve_rotate_captcha(inner_path: str, outer_path: str,
                        slider_width: int = 348) -> Tuple[int, float]:
    """
    Hàm tiện ích: giải rotate CAPTCHA.
    
    Args:
        inner_path: Đường dẫn ảnh inner circle
        outer_path: Đường dẫn ảnh outer
        slider_width: Chiều rộng thanh slider
        
    Returns:
        Tuple of (drag_distance_pixel, angle_degrees)
    """
    solver = RotateSolver()
    return solver.solve(inner_path, outer_path, slider_width)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) == 3:
        inner_path, outer_path = sys.argv[1], sys.argv[2]
        solver = RotateSolver()
        drag, angle = solver.solve(inner_path, outer_path)
        print(f"Góc xoay: {angle:.2f}°, Khoảng cách kéo: {drag}px")
    else:
        print("Usage: python rotate_solver.py <inner.png> <outer.png>")
