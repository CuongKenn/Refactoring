"""
E-Commerce Order Management - BEFORE REFACTORING
Demonstrates code with duplications, long methods, and poor structure
"""

from datetime import datetime
from typing import Dict, List, Optional


class Order:
    """Unrefactored Order class with duplicated logic"""

    def __init__(self, order_id: str, customer_name: str, customer_email: str):
        self.order_id = order_id
        self.customer_name = customer_name
        self.customer_email = customer_email
        self.items = []
        self.created_at = datetime.now()
        self.status = "pending"

    def add_item(self, product_name: str, price: float, quantity: int):
        """Add item with duplicated validation"""
        # Duplicated validation #1
        if price <= 0:
            raise ValueError("Price must be positive")
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        if not product_name or len(product_name.strip()) == 0:
            raise ValueError("Product name cannot be empty")

        self.items.append({"product": product_name, "price": price, "quantity": quantity})

    def calculate_subtotal(self) -> float:
        """Calculate subtotal - duplicated calculation logic"""
        total = 0
        for item in self.items:
            total += item["price"] * item["quantity"]
        return total

    def calculate_tax(self) -> float:
        """Calculate tax - duplicated calculation logic"""
        subtotal = 0
        for item in self.items:
            subtotal += item["price"] * item["quantity"]
        tax_rate = 0.1
        return subtotal * tax_rate

    def calculate_shipping(self) -> float:
        """Calculate shipping - duplicated calculation logic"""
        subtotal = 0
        for item in self.items:
            subtotal += item["price"] * item["quantity"]

        # Duplicated shipping logic
        if subtotal > 100:
            return 0  # Free shipping
        elif subtotal > 50:
            return 5
        else:
            return 10

    def calculate_total(self) -> float:
        """Calculate total - duplicated calculation logic"""
        subtotal = 0
        for item in self.items:
            subtotal += item["price"] * item["quantity"]

        tax_rate = 0.1
        tax = subtotal * tax_rate

        # Duplicated shipping logic again
        if subtotal > 100:
            shipping = 0
        elif subtotal > 50:
            shipping = 5
        else:
            shipping = 10

        return subtotal + tax + shipping

    def get_order_summary(self) -> str:
        """Get order summary - long method with duplications"""
        # Duplicated calculation
        subtotal = 0
        for item in self.items:
            subtotal += item["price"] * item["quantity"]

        tax_rate = 0.1
        tax = subtotal * tax_rate

        # Duplicated shipping logic
        if subtotal > 100:
            shipping = 0
        elif subtotal > 50:
            shipping = 5
        else:
            shipping = 10

        total = subtotal + tax + shipping

        # Build summary
        summary = f"Order #{self.order_id}\n"
        summary += f"Customer: {self.customer_name}\n"
        summary += f"Email: {self.customer_email}\n"
        summary += f"Status: {self.status}\n"
        summary += f"Items:\n"
        for item in self.items:
            summary += f"  - {item['product']}: ${item['price']} x {item['quantity']} = ${item['price'] * item['quantity']}\n"
        summary += f"Subtotal: ${subtotal:.2f}\n"
        summary += f"Tax (10%): ${tax:.2f}\n"
        summary += f"Shipping: ${shipping:.2f}\n"
        summary += f"Total: ${total:.2f}\n"

        return summary

    def apply_discount_code(self, code: str) -> float:
        """Apply discount - duplicated validation and calculation"""
        # Duplicated calculation
        subtotal = 0
        for item in self.items:
            subtotal += item["price"] * item["quantity"]

        # Duplicated discount logic
        if code == "SAVE10":
            discount = subtotal * 0.1
        elif code == "SAVE20":
            discount = subtotal * 0.2
        elif code == "SAVE30":
            discount = subtotal * 0.3
        else:
            discount = 0

        return discount

    def calculate_total_with_discount(self, discount_code: str = None) -> float:
        """Calculate total with discount - massive duplication"""
        # Duplicated calculation
        subtotal = 0
        for item in self.items:
            subtotal += item["price"] * item["quantity"]

        # Duplicated discount logic
        discount = 0
        if discount_code:
            if discount_code == "SAVE10":
                discount = subtotal * 0.1
            elif discount_code == "SAVE20":
                discount = subtotal * 0.2
            elif discount_code == "SAVE30":
                discount = subtotal * 0.3

        discounted_subtotal = subtotal - discount

        tax_rate = 0.1
        tax = discounted_subtotal * tax_rate

        # Duplicated shipping logic
        if subtotal > 100:
            shipping = 0
        elif subtotal > 50:
            shipping = 5
        else:
            shipping = 10

        return discounted_subtotal + tax + shipping


class Invoice:
    """Unrefactored Invoice class with similar duplications"""

    def __init__(self, invoice_id: str, order: Order):
        self.invoice_id = invoice_id
        self.order = order
        self.created_at = datetime.now()

    def calculate_invoice_subtotal(self) -> float:
        """Duplicated from Order.calculate_subtotal"""
        total = 0
        for item in self.order.items:
            total += item["price"] * item["quantity"]
        return total

    def calculate_invoice_tax(self) -> float:
        """Duplicated from Order.calculate_tax"""
        subtotal = 0
        for item in self.order.items:
            subtotal += item["price"] * item["quantity"]
        tax_rate = 0.1
        return subtotal * tax_rate

    def calculate_invoice_total(self) -> float:
        """Duplicated from Order.calculate_total"""
        subtotal = 0
        for item in self.order.items:
            subtotal += item["price"] * item["quantity"]

        tax_rate = 0.1
        tax = subtotal * tax_rate

        if subtotal > 100:
            shipping = 0
        elif subtotal > 50:
            shipping = 5
        else:
            shipping = 10

        return subtotal + tax + shipping

    def generate_invoice(self) -> str:
        """Generate invoice - duplicated summary logic"""
        # Duplicated calculation
        subtotal = 0
        for item in self.order.items:
            subtotal += item["price"] * item["quantity"]

        tax_rate = 0.1
        tax = subtotal * tax_rate

        if subtotal > 100:
            shipping = 0
        elif subtotal > 50:
            shipping = 5
        else:
            shipping = 10

        total = subtotal + tax + shipping

        invoice_text = f"INVOICE #{self.invoice_id}\n"
        invoice_text += f"Date: {self.created_at.strftime('%Y-%m-%d %H:%M')}\n"
        invoice_text += f"Order: {self.order.order_id}\n"
        invoice_text += f"Customer: {self.order.customer_name}\n"
        invoice_text += f"Email: {self.order.customer_email}\n"
        invoice_text += f"\nItems:\n"
        for item in self.order.items:
            invoice_text += (
                f"  {item['product']}: ${item['price']} x {item['quantity']} = ${item['price'] * item['quantity']}\n"
            )
        invoice_text += f"\nSubtotal: ${subtotal:.2f}\n"
        invoice_text += f"Tax: ${tax:.2f}\n"
        invoice_text += f"Shipping: ${shipping:.2f}\n"
        invoice_text += f"TOTAL: ${total:.2f}\n"

        return invoice_text
