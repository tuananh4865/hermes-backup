"""
Human-like Drag Movement — Di chuyển slider như người thật
Dùng bezier curve + random variation để tránh bị phát hiện
"""

import math
import random
import time
from typing import List, Tuple, Generator


class HumanDrag:
    """
    Tạo human-like drag movement để bypass bot detection.
    
    Key techniques:
    1. Bezier curve thay vì đường thẳng
    2. Random pause và speed variation
    3. Micro-corrections nhỏ trên đường đi
    4. Initial delay trước khi bắt đầu kéo
    """
    
    def __init__(self, seed: int = None):
        """Seed cho random để reproduce được nếu cần."""
        if seed is not None:
            random.seed(seed)
        self.last_y_offset = 0
    
    def generate_path(
        self,
        start_x: float,
        start_y: float,
        end_x: float,
        end_y: float,
        duration_ms: float = 1000,
        steps: int = None
    ) -> List[Tuple[float, float, float]]:
        """
        Generate path với human-like movement.
        
        Args:
            start_x, start_y: Vị trí bắt đầu
            end_x, end_y: Vị trí kết thúc
            duration_ms: Thời gian kéo (ms)
            steps: Số bước (auto calculate nếu None)
            
        Returns:
            List of (x, y, delay_ms) tuples
        """
        if steps is None:
            steps = random.randint(40, 80)
        
        path = []
        
        # Initial pause (200-500ms) - người thật hay pause trước khi kéo
        initial_pause = random.uniform(0.2, 0.5)
        path.append((start_x, start_y, initial_pause))
        
        # Generate bezier control points
        cp1_x = start_x + random.uniform(-30, 30)
        cp1_y = start_y + random.uniform(-15, 15)
        cp2_x = end_x + random.uniform(-30, 30)
        cp2_y = end_y + random.uniform(-15, 15)
        
        # Khoảng thời gian mỗi step
        step_duration = duration_ms / steps
        
        for i in range(1, steps + 1):
            t = i / steps
            
            # Cubic bezier
            x = (1-t)**3 * start_x + 3*(1-t)**2*t * cp1_x + 3*(1-t)*t**2 * cp2_x + t**3 * end_x
            
            # Y có sinusoidal variation (người không đi thẳng hoàn hảo)
            y_offset = math.sin(t * math.pi) * random.uniform(-8, 8)
            y = start_y + y_offset
            
            # Random delay per step (tạo speed variation)
            delay = step_duration * random.uniform(0.5, 1.5)
            
            path.append((x, y, delay))
        
        return path
    
    def generate_with_micro_corrections(
        self,
        start_x: float,
        start_y: float,
        end_x: float,
        end_y: float,
        target_distance: float,
        duration_ms: float = 1000
    ) -> List[Tuple[float, float, float]]:
        """
        Generate path với micro-corrections (người hay sửa lại khi gần đích).
        
        Args:
            start_x, start_y: Vị trí bắt đầu
            end_x, end_y: Vị trí kết thúc  
            target_distance: Khoảng cách cần kéo (pixel)
            duration_ms: Thời gian kéo (ms)
        """
        # Thường overshoot rồi correct
        overshoot_chance = random.random()
        
        if overshoot_chance > 0.6:
            # Overshoot
            overshoot_pct = random.uniform(1.1, 1.3)
            mid_end_x = start_x + target_distance * overshoot_pct
        else:
            mid_end_x = end_x
        
        # Generate main path
        path1 = self.generate_path(start_x, start_y, mid_end_x, start_y, 
                                   duration_ms * 0.7)
        
        # Micro-correction path
        if mid_end_x != end_x:
            path2 = self.generate_path(mid_end_x, start_y, end_x, start_y,
                                      duration_ms * 0.3)
            path = path1 + path2[1:]  # Skip duplicate point
        else:
            path = path1
        
        return path
    
    def get_mouse_movements(
        self,
        start_x: float,
        start_y: float,
        end_x: float,
        end_y: float,
        target_distance: float = None,
        duration_ms: float = 1000
    ) -> List[Tuple[float, float, float]]:
        """
        Main interface: lấy list các mouse movements.
        
        Args:
            start_x, start_y: Vị trí bắt đầu
            end_x, end_y: Vị trí kết thúc
            target_distance: Khoảng cách cần kéo (pixel)
            duration_ms: Thời gian kéo (ms)
            
        Returns:
            List of (x, y, delay_seconds) tuples
        """
        if target_distance is None:
            target_distance = abs(end_x - start_x)
        
        # Random chọn strategy
        strategy = random.random()
        
        if strategy > 0.5:
            return self.generate_with_micro_corrections(
                start_x, start_y, end_x, end_y, target_distance, duration_ms
            )
        else:
            return self.generate_path(
                start_x, start_y, end_x, end_y, duration_ms
            )


def human_drag(page, slider_element, target_distance: int, duration_ms: int = 1000):
    """
    Thực hiện human-like drag trên Playwright page.
    
    Args:
        page: Playwright page object
        slider_element: Slider element handle
        target_distance: Khoảng cách cần kéo (pixel)
        duration_ms: Thời gian kéo (ms)
    """
    # Get bounding box
    bbox = slider_element.bounding_box()
    start_x = bbox["x"] + bbox["width"] / 2
    start_y = bbox["y"] + bbox["height"] / 2
    
    end_x = start_x + target_distance
    
    # Generate path
    drag = HumanDrag()
    movements = drag.get_mouse_movements(
        start_x, start_y, end_x, start_y, target_distance, duration_ms
    )
    
    # Execute movements
    page.mouse.move(start_x, start_y)
    page.mouse.down()
    
    for x, y, delay in movements[1:]:  # Skip first (already at start)
        page.mouse.move(x, y)
        time.sleep(delay / 1000)  # Convert ms to seconds
    
    page.mouse.up()


def human_swipe(start_x: int, start_y: int, end_x: int, end_y: int,
               steps: int = None) -> List[Tuple[int, int]]:
    """
    Tạo swipe path cho mobile (Appium-style).
    
    Args:
        start_x, start_y: Vị trí bắt đầu
        end_x, end_y: Vị trí kết thúc
        steps: Số bước
        
    Returns:
        List of (x, y) tuples
    """
    if steps is None:
        steps = random.randint(30, 60)
    
    path = []
    
    for i in range(steps + 1):
        t = i / steps
        
        # Ease-in-out
        if t < 0.5:
            ease = 2 * t * t
        else:
            ease = 1 - pow(-2 * t + 2, 2) / 2
        
        x = int(start_x + (end_x - start_x) * ease)
        y = int(start_y + (end_y - start_y) * ease + random.uniform(-3, 3))
        
        path.append((x, y))
    
    return path


if __name__ == "__main__":
    # Test đơn giản
    drag = HumanDrag()
    movements = drag.get_mouse_movements(100, 200, 300, 200, 200, 1000)
    
    print(f"Generated {len(movements)} movement steps:")
    for i, (x, y, delay) in enumerate(movements[:5]):
        print(f"  Step {i}: ({x:.1f}, {y:.1f}), delay: {delay*1000:.1f}ms")
    print("  ...")
