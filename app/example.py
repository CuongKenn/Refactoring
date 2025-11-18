# app/example.py
"""
Module demo phức tạp với NHIỀU LỖI FORMATTING để test auto-fix
"""
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union


class DataValidator:
    """Validator cho dữ liệu - CÓ LỖI FORMATTING"""

    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email - LỖI SPACING"""
        if not email or "@" not in email:
            return False
        parts = email.split("@")
        if len(parts) != 2:
            return False
        return len(parts[0]) > 0 and len(parts[1]) > 0

    @staticmethod
    def validate_age(age: int) -> bool:
        """Validate tuổi"""
        return 0 <= age <= 150

    @staticmethod
    def validate_phone(phone: str) -> bool:
        """Validate SĐT VN"""
        phone = phone.replace(" ", "").replace("-", "")
        if not phone.startswith("0"):
            return False
        return len(phone) == 10 and phone.isdigit()


class UserManager:
    """Manager users - LỖI FORMATTING"""

    def __init__(self):
        self.users: List[Dict] = []
        self.validator = DataValidator()

    def add_user(self, name: str, email: str, age: int, phone: str) -> Dict:
        """Thêm user"""
        errors = []

        if not name or len(name.strip()) < 2:
            errors.append("Tên phải >=2 ký tự")

        if not self.validator.validate_email(email):
            errors.append("Email invalid")

        if not self.validator.validate_age(age):
            errors.append("Tuổi 0-150")

        if not self.validator.validate_phone(phone):
            errors.append("SĐT invalid")

        if errors:
            return {"success": False, "errors": errors}

        user = {
            "id": len(self.users) + 1,
            "name": name.strip(),
            "email": email.lower(),
            "age": age,
            "phone": phone,
            "created_at": datetime.now().isoformat(),
        }
        self.users.append(user)
        return {"success": True, "user": user}

    def get_user_by_id(self, user_id: int) -> Optional[Dict]:
        """Lấy user by ID"""
        for user in self.users:
            if user["id"] == user_id:
                return user
        return None

    def get_users_by_age_range(self, min_age: int, max_age: int) -> List[Dict]:
        """Lấy users trong khoảng tuổi"""
        return [u for u in self.users if min_age <= u["age"] <= max_age]

    def update_user(self, user_id: int, **kwargs) -> Dict:
        """Update user"""
        user = self.get_user_by_id(user_id)
        if not user:
            return {"success": False, "error": "User not found"}

        for key, value in kwargs.items():
            if key in user and key != "id":
                user[key] = value

        return {"success": True, "user": user}

    def delete_user(self, user_id: int) -> bool:
        """Xóa user"""
        user = self.get_user_by_id(user_id)
        if user:
            self.users.remove(user)
            return True
        return False


class DataProcessor:
    """Xử lý data - LỖI FORMATTING"""

    @staticmethod
    def calculate_statistics(numbers: List[Union[int, float]]) -> Dict:
        """Tính stats"""
        if not numbers:
            return {"error": "Empty list"}

        total = sum(numbers)
        count = len(numbers)
        average = total / count
        sorted_nums = sorted(numbers)

        if count % 2 == 0:
            median = (sorted_nums[count // 2 - 1] + sorted_nums[count // 2]) / 2
        else:
            median = sorted_nums[count // 2]

        return {"count": count, "sum": total, "average": average, "median": median, "min": min(numbers), "max": max(numbers)}

    @staticmethod
    def filter_outliers(numbers: List[float], threshold: float = 2.0) -> List[float]:
        """Loại outliers"""
        if len(numbers) < 3:
            return numbers

        mean = sum(numbers) / len(numbers)
        variance = sum((x - mean) ** 2 for x in numbers) / len(numbers)
        std_dev = variance**0.5

        return [x for x in numbers if abs(x - mean) <= threshold * std_dev]

    @staticmethod
    def group_by_range(numbers: List[int], range_size: int = 10) -> Dict[str, List[int]]:
        """Nhóm số theo range"""
        if not numbers or range_size <= 0:
            return {}

        groups = {}
        for num in numbers:
            range_key = f"{(num//range_size)*range_size}-{(num//range_size)*range_size+range_size-1}"
            if range_key not in groups:
                groups[range_key] = []
            groups[range_key].append(num)

        return groups


def process_json_data(json_string: str) -> Dict:
    """Process JSON - LỖI FORMATTING"""
    try:
        data = json.loads(json_string)
        return {"success": True, "data": data}
    except json.JSONDecodeError as e:
        return {"success": False, "error": str(e)}


def calculate_discount(price: float, discount_percent: float, is_member: bool = False) -> float:
    """Tính giảm giá - LỖI FORMATTING"""
    if price < 0 or discount_percent < 0 or discount_percent > 100:
        raise ValueError("Invalid values")

    discount = price * discount_percent / 100
    final_price = price - discount

    if is_member:
        final_price *= 0.95

    return round(final_price, 2)
