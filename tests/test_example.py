"""Tests demonstrating the refactoring improvements"""

import pytest
from app.example import Order as OldOrder, Invoice as OldInvoice
from app.refactored import (
    Order as NewOrder, 
    Invoice as NewInvoice,
    OrderItem,
    PriceCalculator,
    ShippingCalculator,
    DiscountCode
)


class TestOldImplementation:
    """Test the old, unrefactored code"""
    
    def test_old_order_basic_calculation(self):
        order = OldOrder("ORD001", "John Doe", "john@example.com")
        order.add_item("Laptop", 1000, 1)
        order.add_item("Mouse", 25, 2)
        
        assert order.calculate_subtotal() == 1050
        assert order.calculate_tax() == 105
        assert order.calculate_shipping() == 0  # Free shipping
        assert order.calculate_total() == 1155
    
    def test_old_order_with_discount(self):
        order = OldOrder("ORD002", "Jane Smith", "jane@example.com")
        order.add_item("Phone", 500, 1)
        
        discount = order.apply_discount_code("SAVE20")
        assert discount == 100
        
        total_with_discount = order.calculate_total_with_discount("SAVE20")
        assert total_with_discount == 440  # (500-100) + 40 tax + 0 shipping (>100)
    
    def test_old_invoice_generation(self):
        order = OldOrder("ORD003", "Bob Johnson", "bob@example.com")
        order.add_item("Keyboard", 75, 1)
        
        invoice = OldInvoice("INV003", order)
        invoice_text = invoice.generate_invoice()
        
        assert "INVOICE #INV003" in invoice_text
        assert "Bob Johnson" in invoice_text
        assert "Keyboard" in invoice_text


class TestNewImplementation:
    """Test the refactored, clean code"""
    
    def test_new_order_basic_calculation(self):
        order = NewOrder("ORD001", "John Doe", "john@example.com")
        order.add_item("Laptop", 1000, 1)
        order.add_item("Mouse", 25, 2)
        
        assert order.calculate_subtotal() == 1050
        assert order.calculate_tax() == 105
        assert order.calculate_shipping() == 0
        assert order.calculate_total() == 1155
    
    def test_new_order_with_discount(self):
        order = NewOrder("ORD002", "Jane Smith", "jane@example.com")
        order.add_item("Phone", 500, 1)
        
        discount = order.apply_discount_code("SAVE20")
        assert discount == 100
        
        total_with_discount = order.calculate_total_with_discount("SAVE20")
        assert total_with_discount == 440  # (500-100) + 40 tax + 0 shipping
    
    def test_new_invoice_generation(self):
        order = NewOrder("ORD003", "Bob Johnson", "bob@example.com")
        order.add_item("Keyboard", 75, 1)
        
        invoice = NewInvoice("INV003", order)
        invoice_text = invoice.generate_invoice()
        
        assert "INVOICE #INV003" in invoice_text
        assert "Bob Johnson" in invoice_text
        assert "Keyboard" in invoice_text


class TestRefactoringImprovements:
    """Test the specific improvements from refactoring"""
    
    def test_order_item_validation(self):
        """OrderItem class provides centralized validation"""
        with pytest.raises(ValueError, match="Price must be positive"):
            OrderItem("Product", -10, 1)
        
        with pytest.raises(ValueError, match="Quantity must be positive"):
            OrderItem("Product", 10, 0)
        
        with pytest.raises(ValueError, match="Product name cannot be empty"):
            OrderItem("", 10, 1)
    
    def test_shipping_calculator_reusability(self):
        """ShippingCalculator can be used independently"""
        assert ShippingCalculator.calculate(150) == 0
        assert ShippingCalculator.calculate(75) == 5
        assert ShippingCalculator.calculate(25) == 10
    
    def test_discount_code_enum(self):
        """Discount codes use enum instead of magic strings"""
        assert DiscountCode.SAVE10.value == 0.1
        assert DiscountCode.SAVE20.value == 0.2
        assert DiscountCode.SAVE30.value == 0.3
    
    def test_price_calculator_caching(self):
        """PriceCalculator caches subtotal for efficiency"""
        items = [
            {"product": "Item1", "price": 100, "quantity": 2},
            {"product": "Item2", "price": 50, "quantity": 3}
        ]
        calculator = PriceCalculator(items)
        
        # First call calculates
        subtotal1 = calculator.get_subtotal()
        assert subtotal1 == 350
        
        # Second call uses cache (same result, no recalculation)
        subtotal2 = calculator.get_subtotal()
        assert subtotal2 == 350
        assert subtotal1 is subtotal2  # Same object reference


class TestCodeComparison:
    """Compare old vs new implementation results"""
    
    def test_both_implementations_produce_same_results(self):
        """Verify refactoring preserves functionality"""
        # Old implementation
        old_order = OldOrder("ORD100", "Test User", "test@example.com")
        old_order.add_item("Product A", 100, 2)
        old_order.add_item("Product B", 50, 1)
        
        # New implementation
        new_order = NewOrder("ORD100", "Test User", "test@example.com")
        new_order.add_item("Product A", 100, 2)
        new_order.add_item("Product B", 50, 1)
        
        # Same results
        assert old_order.calculate_subtotal() == new_order.calculate_subtotal()
        assert old_order.calculate_tax() == new_order.calculate_tax()
        assert old_order.calculate_shipping() == new_order.calculate_shipping()
        assert old_order.calculate_total() == new_order.calculate_total()
    
    def test_discount_calculations_match(self):
        """Both implementations calculate discounts identically"""
        old_order = OldOrder("ORD200", "User", "user@test.com")
        old_order.add_item("Item", 200, 1)
        
        new_order = NewOrder("ORD200", "User", "user@test.com")
        new_order.add_item("Item", 200, 1)
        
        for code in ["SAVE10", "SAVE20", "SAVE30"]:
            old_discount = old_order.apply_discount_code(code)
            new_discount = new_order.apply_discount_code(code)
            assert old_discount == new_discount
            
            old_total = old_order.calculate_total_with_discount(code)
            new_total = new_order.calculate_total_with_discount(code)
            assert old_total == new_total


class TestRefactoringBenefits:
    """Demonstrate benefits of refactored code"""
    
    def test_reduced_code_duplication(self):
        """New code eliminates subtotal calculation duplication"""
        order = NewOrder("ORD300", "Customer", "customer@email.com")
        order.add_item("Product", 100, 3)
        
        # All methods use same calculator instance
        calculator = order._get_calculator()
        
        # Calling multiple times doesn't recalculate (uses cache)
        subtotal1 = calculator.get_subtotal()
        subtotal2 = calculator.get_subtotal()
        tax = calculator.get_tax()
        shipping = calculator.get_shipping()
        
        assert subtotal1 == subtotal2 == 300
        assert tax == 30
        assert shipping == 0
    
    def test_easier_to_extend(self):
        """New structure makes it easy to add features"""
        # Can easily create custom calculators
        items = [{"product": "Item", "price": 50, "quantity": 4}]
        calculator = PriceCalculator(items)
        
        # Easy to add new discount codes via enum
        assert "SAVE10" in DiscountCode.__members__
        assert "SAVE20" in DiscountCode.__members__
        assert "SAVE30" in DiscountCode.__members__
    
    def test_better_separation_of_concerns(self):
        """Each class has single responsibility"""
        # OrderItem handles validation
        item = OrderItem("Product", 50, 2)
        assert item.get_line_total() == 100
        
        # ShippingCalculator handles shipping
        assert ShippingCalculator.calculate(60) == 5
        
        # PriceCalculator handles all calculations
        calculator = PriceCalculator([item.to_dict()])
        assert calculator.get_subtotal() == 100
        assert calculator.get_tax() == 10
