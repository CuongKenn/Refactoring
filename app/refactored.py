"""
E-Commerce Order Management - AFTER REFACTORING
Clean code with DRY principle, extracted methods, and better structure
"""

from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional


class DiscountCode(Enum):
    """Enum for discount codes - eliminates magic strings"""

    SAVE10 = 0.1
    SAVE20 = 0.2
    SAVE30 = 0.3


class ShippingCalculator:
    """Extracted shipping logic into dedicated class"""

    @staticmethod
    def calculate(subtotal: float) -> float:
        """Single source of truth for shipping calculation"""
        if subtotal > 100:
            return 0.0
        elif subtotal > 50:
            return 5.0
        else:
            return 10.0


class PriceCalculator:
    """Centralized pricing calculations - DRY principle"""

    TAX_RATE = 0.1

    def __init__(self, items: List[Dict]):
        self.items = items
        self._subtotal_cache = None

    def get_subtotal(self) -> float:
        """Calculate subtotal once and cache it"""
        if self._subtotal_cache is None:
            self._subtotal_cache = sum(item["price"] * item["quantity"] for item in self.items)
        return self._subtotal_cache

    def get_tax(self) -> float:
        """Calculate tax based on subtotal"""
        return self.get_subtotal() * self.TAX_RATE

    def get_shipping(self) -> float:
        """Calculate shipping using dedicated calculator"""
        return ShippingCalculator.calculate(self.get_subtotal())

    def get_discount(self, code: Optional[str]) -> float:
        """Calculate discount using enum values"""
        if not code:
            return 0.0

        try:
            discount_rate = DiscountCode[code].value
            return self.get_subtotal() * discount_rate
        except KeyError:
            return 0.0

    def get_total(self, discount_code: Optional[str] = None) -> float:
        """Calculate final total with all components"""
        subtotal = self.get_subtotal()
        discount = self.get_discount(discount_code)
        discounted_subtotal = subtotal - discount
        tax = discounted_subtotal * self.TAX_RATE
        shipping = self.get_shipping()

        return discounted_subtotal + tax + shipping

    def invalidate_cache(self):
        """Clear cache when items change"""
        self._subtotal_cache = None


class OrderItem:
    """Extracted item validation and representation"""

    def __init__(self, product_name: str, price: float, quantity: int):
        self._validate(product_name, price, quantity)
        self.product_name = product_name
        self.price = price
        self.quantity = quantity

    @staticmethod
    def _validate(product_name: str, price: float, quantity: int):
        """Single validation method"""
        if not product_name or not product_name.strip():
            raise ValueError("Product name cannot be empty")
        if price <= 0:
            raise ValueError("Price must be positive")
        if quantity <= 0:
            raise ValueError("Quantity must be positive")

    def get_line_total(self) -> float:
        """Calculate item total"""
        return self.price * self.quantity

    def to_dict(self) -> Dict:
        """Convert to dictionary for compatibility"""
        return {"product": self.product_name, "price": self.price, "quantity": self.quantity}


class Order:
    """Refactored Order class - clean and focused"""

    def __init__(self, order_id: str, customer_name: str, customer_email: str):
        self.order_id = order_id
        self.customer_name = customer_name
        self.customer_email = customer_email
        self.items: List[OrderItem] = []
        self.created_at = datetime.now()
        self.status = "pending"
        self._calculator = None

    def add_item(self, product_name: str, price: float, quantity: int):
        """Add item using OrderItem class"""
        item = OrderItem(product_name, price, quantity)
        self.items.append(item)
        if self._calculator:
            self._calculator.invalidate_cache()

    def _get_calculator(self) -> PriceCalculator:
        """Lazy initialization of calculator"""
        if self._calculator is None:
            items_dict = [item.to_dict() for item in self.items]
            self._calculator = PriceCalculator(items_dict)
        return self._calculator

    def calculate_subtotal(self) -> float:
        """Delegate to calculator"""
        return self._get_calculator().get_subtotal()

    def calculate_tax(self) -> float:
        """Delegate to calculator"""
        return self._get_calculator().get_tax()

    def calculate_shipping(self) -> float:
        """Delegate to calculator"""
        return self._get_calculator().get_shipping()

    def calculate_total(self) -> float:
        """Delegate to calculator"""
        return self._get_calculator().get_total()

    def apply_discount_code(self, code: str) -> float:
        """Delegate to calculator"""
        return self._get_calculator().get_discount(code)

    def calculate_total_with_discount(self, discount_code: Optional[str] = None) -> float:
        """Delegate to calculator"""
        return self._get_calculator().get_total(discount_code)

    def get_order_summary(self) -> str:
        """Generate summary using helper method"""
        calculator = self._get_calculator()

        lines = [
            f"Order #{self.order_id}",
            f"Customer: {self.customer_name}",
            f"Email: {self.customer_email}",
            f"Status: {self.status}",
            "Items:",
        ]

        lines.extend(self._format_items())
        lines.extend(self._format_totals(calculator))

        return "\n".join(lines) + "\n"

    def _format_items(self) -> List[str]:
        """Extract item formatting logic"""
        return [f"  - {item.product_name}: ${item.price} x {item.quantity} = ${item.get_line_total()}" for item in self.items]

    def _format_totals(self, calculator: PriceCalculator) -> List[str]:
        """Extract totals formatting logic"""
        return [
            f"Subtotal: ${calculator.get_subtotal():.2f}",
            f"Tax (10%): ${calculator.get_tax():.2f}",
            f"Shipping: ${calculator.get_shipping():.2f}",
            f"Total: ${calculator.get_total():.2f}",
        ]


class Invoice:
    """Refactored Invoice class - reuses Order's calculator"""

    def __init__(self, invoice_id: str, order: Order):
        self.invoice_id = invoice_id
        self.order = order
        self.created_at = datetime.now()

    def calculate_invoice_subtotal(self) -> float:
        """Reuse order's calculation"""
        return self.order.calculate_subtotal()

    def calculate_invoice_tax(self) -> float:
        """Reuse order's calculation"""
        return self.order.calculate_tax()

    def calculate_invoice_total(self) -> float:
        """Reuse order's calculation"""
        return self.order.calculate_total()

    def generate_invoice(self) -> str:
        """Generate invoice by reusing order data"""
        calculator = self.order._get_calculator()

        lines = [
            f"INVOICE #{self.invoice_id}",
            f"Date: {self.created_at.strftime('%Y-%m-%d %H:%M')}",
            f"Order: {self.order.order_id}",
            f"Customer: {self.order.customer_name}",
            f"Email: {self.order.customer_email}",
            "",
            "Items:",
        ]

        for item in self.order.items:
            lines.append(f"  {item.product_name}: ${item.price} x {item.quantity} = ${item.get_line_total()}")

        lines.extend(
            [
                "",
                f"Subtotal: ${calculator.get_subtotal():.2f}",
                f"Tax: ${calculator.get_tax():.2f}",
                f"Shipping: ${calculator.get_shipping():.2f}",
                f"TOTAL: ${calculator.get_total():.2f}",
            ]
        )

        return "\n".join(lines) + "\n"
