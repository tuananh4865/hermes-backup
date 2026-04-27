"""
3D Shapes CAPTCHA Solver — Dùng MiniMax Vision API (Miễn phí vì đã có quyền truy cập)
Nhận diện object và hướng xoay bằng AI vision
"""

import base64
import json
from typing import Tuple, Optional


class ShapesSolver:
    """
    Giải 3D Shapes CAPTCHA dùng MiniMax Vision API.
    
    Cách hoạt động:
    1. Chụp ảnh CAPTCHA (gồm reference + các objects cần chọn)
    2. Gửi cho MiniMax Vision
    3. Nhận về object cần chọn và hướng xoay
    4. Trả về index của object đúng
    """
    
    def __init__(self, minimax_api_key: str = None):
        self.api_key = minimax_api_key or "YOUR_MINIMAX_API_KEY"
    
    def solve(self, image_path: str) -> Tuple[int, float]:
        """
        Giải 3D shapes CAPTCHA.
        
        Args:
            image_path: Đường dẫn ảnh CAPTCHA
            
        Returns:
            Tuple of (object_index, confidence)
            object_index: 0-based index của object cần chọn
        """
        with open(image_path, "rb") as f:
            image_bytes = f.read()
        
        return self.solve_from_bytes(image_bytes)
    
    def solve_from_bytes(self, image_bytes: bytes) -> Tuple[int, float]:
        """
        Giải từ bytes.
        
        Args:
            image_bytes: Ảnh CAPTCHA dạng bytes
            
        Returns:
            Tuple of (object_index, confidence)
        """
        b64_image = base64.b64encode(image_bytes).decode("utf-8")
        result = self._call_vision_api(b64_image)
        return self._parse_result(result)
    
    def _call_vision_api(self, b64_image: str) -> dict:
        """
        Gọi MiniMax Vision API.
        """
        import requests
        
        url = "https://api.minimax.chat/v1/vision"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "MiniMax-VL-01",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{b64_image}"}
                        },
                        {
                            "type": "text",
                            "text": "This is a TikTok 3D Shapes CAPTCHA. Identify which object matches the reference shape and what rotation direction is needed. Return JSON: {\"object_index\": 0-8, \"rotation\": \"CW\" or \"CCW\", \"confidence\": 0.0-1.0}"
                        }
                    ]
                }
            ],
            "temperature": 0.1
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        return response.json()
    
    def _parse_result(self, result: dict) -> Tuple[int, float]:
        """Parse kết quả từ Vision API."""
        try:
            content = result["choices"][0]["message"]["content"]
            data = json.loads(content)
            
            object_index = int(data.get("object_index", 0))
            confidence = float(data.get("confidence", 0.5))
            
            print(f"[ShapesSolver] Object: {object_index}, Confidence: {confidence:.2f}")
            return object_index, confidence
            
        except (KeyError, json.JSONDecodeError) as e:
            print(f"[ShapesSolver] Parse error: {e}")
            return 0, 0.3


def solve_shapes_captcha(image_path: str) -> Tuple[int, float]:
    """Hàm tiện ích: giải 3D shapes CAPTCHA."""
    solver = ShapesSolver()
    return solver.solve(image_path)


if __name__ == "__main__":
    import sys
    if len(sys.argv) == 2:
        index, conf = solve_shapes_captcha(sys.argv[1])
        print(f"Chọn object index: {index} (confidence: {conf:.2f})")
    else:
        print("Usage: python shapes_solver.py <captcha.png>")
