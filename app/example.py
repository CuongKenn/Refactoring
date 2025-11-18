# app/example.py
"""
E-commerce Product Management System - CÓ TÌNH NHIỀU LỖI FORMAT
"""
import json
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional


class ProductCategory(Enum):
    """Product categories - LỖI FORMAT"""

    ELECTRONICS = "electronics"
    CLOTHING = "clothing"
    FOOD = "food"
    BOOKS = "books"
    TOYS = "toys"


class Product:
    """Product class - LỖI FORMAT"""

    def __init__(self, product_id: int, name: str, category: ProductCategory, price: float, stock: int, description: str = ""):
        self.product_id = product_id
        self.name = name
        self.category = category
        self.price = price
        self.stock = stock
        self.description = description
        self.created_at = datetime.now()

    def to_dict(self) -> Dict:
        """Convert to dict"""
        return {
            "product_id": self.product_id,
            "name": self.name,
            "category": self.category.value,
            "price": self.price,
            "stock": self.stock,
            "description": self.description,
            "created_at": self.created_at.isoformat(),
        }

    def is_in_stock(self) -> bool:
        """Check if in stock"""
        return self.stock > 0

    def update_stock(self, quantity: int) -> bool:
        """Update stock"""
        new_stock = self.stock + quantity
        if new_stock < 0:
            return False
        self.stock = new_stock
        return True

    def apply_discount(self, discount_percent: float) -> float:
        """Calculate discounted price"""
        if discount_percent < 0 or discount_percent > 100:
            raise ValueError("Discount must be 0-100")
        discount_amount = self.price * discount_percent / 100
        return round(self.price - discount_amount, 2)


class Customer:
    """Customer class - LỖI FORMAT"""

    def __init__(self, customer_id: int, name: str, email: str, phone: str):
        self.customer_id = customer_id
        self.name = name
        self.email = email
        self.phone = phone
        self.orders: List[int] = []
        self.loyalty_points = 0

    def to_dict(self) -> Dict:
        """Convert to dict"""
        return {
            "customer_id": self.customer_id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "orders": self.orders,
            "loyalty_points": self.loyalty_points,
        }

    def add_loyalty_points(self, points: int) -> None:
        """Add loyalty points"""
        if points > 0:
            self.loyalty_points += points

    def use_loyalty_points(self, points: int) -> bool:
        """Use loyalty points"""
        if points > self.loyalty_points or points < 0:
            return False
        self.loyalty_points -= points
        return True

    def get_discount_rate(self) -> float:
        """Get discount based on loyalty"""
        if self.loyalty_points >= 1000:
            return 0.15
        elif self.loyalty_points >= 500:
            return 0.10
        elif self.loyalty_points >= 100:
            return 0.05
        return 0.0


class Order:
    """Order class - LỖI FORMAT"""

    def __init__(self, order_id: int, customer_id: int):
        self.order_id = order_id
        self.customer_id = customer_id
        self.items: List[Dict] = []
        self.status = "pending"
        self.created_at = datetime.now()
        self.total_amount = 0.0

    def add_item(self, product_id: int, quantity: int, price: float) -> None:
        """Add item to order"""
        item = {"product_id": product_id, "quantity": quantity, "price": price, "subtotal": quantity * price}
        self.items.append(item)
        self.calculate_total()

    def remove_item(self, product_id: int) -> bool:
        """Remove item from order"""
        for item in self.items:
            if item["product_id"] == product_id:
                self.items.remove(item)
                self.calculate_total()
                return True
        return False

    def calculate_total(self) -> float:
        """Calculate total amount"""
        self.total_amount = sum(item["subtotal"] for item in self.items)
        return self.total_amount

    def apply_discount(self, discount_percent: float) -> None:
        """Apply discount to order"""
        if discount_percent > 0:
            discount = self.total_amount * discount_percent
            self.total_amount -= discount

    def update_status(self, new_status: str) -> None:
        """Update order status"""
        valid_statuses = ["pending", "processing", "shipped", "delivered", "cancelled"]
        if new_status in valid_statuses:
            self.status = new_status

    def to_dict(self) -> Dict:
        """Convert to dict"""
        return {
            "order_id": self.order_id,
            "customer_id": self.customer_id,
            "items": self.items,
            "status": self.status,
            "total_amount": self.total_amount,
            "created_at": self.created_at.isoformat(),
        }


class Store:
    """Store management - LỖI FORMAT"""

    def __init__(self, name: str):
        self.name = name
        self.products: Dict[int, Product] = {}
        self.customers: Dict[int, Customer] = {}
        self.orders: Dict[int, Order] = {}
        self.next_product_id = 1
        self.next_customer_id = 1
        self.next_order_id = 1

    def add_product(self, name: str, category: ProductCategory, price: float, stock: int, description: str = "") -> Product:
        """Add new product"""
        product = Product(self.next_product_id, name, category, price, stock, description)
        self.products[self.next_product_id] = product
        self.next_product_id += 1
        return product

    def register_customer(self, name: str, email: str, phone: str) -> Customer:
        """Register new customer"""
        customer = Customer(self.next_customer_id, name, email, phone)
        self.customers[self.next_customer_id] = customer
        self.next_customer_id += 1
        return customer

    def create_order(self, customer_id: int) -> Optional[Order]:
        """Create new order"""
        if customer_id not in self.customers:
            return None
        order = Order(self.next_order_id, customer_id)
        self.orders[self.next_order_id] = order
        self.next_order_id += 1
        return order

    def add_to_order(self, order_id: int, product_id: int, quantity: int) -> Dict:
        """Add product to order"""
        if order_id not in self.orders:
            return {"success": False, "error": "Order not found"}

        if product_id not in self.products:
            return {"success": False, "error": "Product not found"}

        order = self.orders[order_id]
        product = self.products[product_id]

        if not product.is_in_stock():
            return {"success": False, "error": "Out of stock"}

        if product.stock < quantity:
            return {"success": False, "error": f"Only {product.stock} available"}

        if product.update_stock(-quantity):
            order.add_item(product_id, quantity, product.price)
            return {"success": True, "order": order.to_dict()}

        return {"success": False, "error": "Failed to update stock"}

    def complete_order(self, order_id: int, apply_loyalty_discount: bool = False) -> Dict:
        """Complete order"""
        if order_id not in self.orders:
            return {"success": False, "error": "Order not found"}

        order = self.orders[order_id]
        customer = self.customers.get(order.customer_id)

        if not customer:
            return {"success": False, "error": "Customer not found"}

        if apply_loyalty_discount:
            discount_rate = customer.get_discount_rate()
            order.apply_discount(discount_rate)

        order.update_status("processing")
        customer.orders.append(order_id)

        points = int(order.total_amount / 10)
        customer.add_loyalty_points(points)

        return {"success": True, "order": order.to_dict(), "loyalty_points_earned": points}

    def search_products(self, query: str, category: Optional[ProductCategory] = None) -> List[Product]:
        """Search products"""
        query_lower = query.lower()
        results = []

        for product in self.products.values():
            if category and product.category != category:
                continue

            if query_lower in product.name.lower() or query_lower in product.description.lower():
                results.append(product)

        return results

    def get_low_stock_products(self, threshold: int = 10) -> List[Product]:
        """Get products with low stock"""
        return [p for p in self.products.values() if p.stock <= threshold]

    def get_revenue_report(self) -> Dict:
        """Generate revenue report"""
        completed_orders = [o for o in self.orders.values() if o.status in ["delivered", "processing"]]
        total_revenue = sum(o.total_amount for o in completed_orders)
        total_orders = len(completed_orders)
        avg_order_value = total_revenue / total_orders if total_orders > 0 else 0

        return {"total_revenue": total_revenue, "total_orders": total_orders, "average_order_value": round(avg_order_value, 2)}


def validate_email(email: str) -> bool:
    """Validate email format - LỖI FORMAT"""
    if not email or "@" not in email:
        return False
    parts = email.split("@")
    return len(parts) == 2 and len(parts[0]) > 0 and len(parts[1]) > 0


def calculate_tax(amount: float, tax_rate: float = 0.1) -> float:
    """Calculate tax - LỖI FORMAT"""
    if amount < 0:
        return 0.0
    return round(amount * tax_rate, 2)


def format_currency(amount: float) -> str:
    """Format currency - LỖI FORMAT"""
    return f"${amount:,.2f}"
