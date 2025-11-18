# tests/test_example.py
"""
Tests for E-commerce System - LỖI FORMAT
"""
import pytest

from app.example import Customer, Order, Product, ProductCategory, Store, calculate_tax, format_currency, validate_email


class TestProduct:
    """Test Product class - LỖI FORMAT"""

    def test_product_creation(self):
        """Test create product"""
        product = Product(1, "Laptop", ProductCategory.ELECTRONICS, 999.99, 10, "Gaming laptop")

        assert product.product_id == 1
        assert product.name == "Laptop"
        assert product.price == 999.99
        assert product.stock == 10

    def test_product_is_in_stock(self):
        """Test stock check"""
        product = Product(1, "Test", ProductCategory.TOYS, 10.0, 5)
        assert product.is_in_stock()

        product.stock = 0
        assert product.is_in_stock() == False

    def test_product_update_stock(self):
        """Test update stock"""
        product = Product(1, "Test", ProductCategory.TOYS, 10.0, 5)

        assert product.update_stock(5)
        assert product.stock == 10

        assert product.update_stock(-3)
        assert product.stock == 7

        assert product.update_stock(-10) == False

    def test_product_apply_discount(self):
        """Test discount"""
        product = Product(1, "Test", ProductCategory.TOYS, 100.0, 5)

        assert product.apply_discount(10) == 90.0
        assert product.apply_discount(50) == 50.0

        with pytest.raises(ValueError):
            product.apply_discount(150)


class TestCustomer:
    """Test Customer class - LỖI FORMAT"""

    def test_customer_creation(self):
        """Test create customer"""
        customer = Customer(1, "John", "john@test.com", "0123456789")

        assert customer.customer_id == 1
        assert customer.name == "John"
        assert customer.loyalty_points == 0

    def test_add_loyalty_points(self):
        """Test add points"""
        customer = Customer(1, "Test", "test@test.com", "0123")

        customer.add_loyalty_points(50)
        assert customer.loyalty_points == 50

        customer.add_loyalty_points(100)
        assert customer.loyalty_points == 150

    def test_use_loyalty_points(self):
        """Test use points"""
        customer = Customer(1, "Test", "test@test.com", "0123")
        customer.loyalty_points = 100

        assert customer.use_loyalty_points(50)
        assert customer.loyalty_points == 50

        assert customer.use_loyalty_points(100) == False

    def test_get_discount_rate(self):
        """Test discount rate"""
        customer = Customer(1, "Test", "test@test.com", "0123")

        customer.loyalty_points = 50
        assert customer.get_discount_rate() == 0.0

        customer.loyalty_points = 150
        assert customer.get_discount_rate() == 0.05

        customer.loyalty_points = 600
        assert customer.get_discount_rate() == 0.10

        customer.loyalty_points = 1200
        assert customer.get_discount_rate() == 0.15


class TestOrder:
    """Test Order class - LỖI FORMAT"""

    def test_order_creation(self):
        """Test create order"""
        order = Order(1, 100)

        assert order.order_id == 1
        assert order.customer_id == 100
        assert order.status == "pending"
        assert order.total_amount == 0.0

    def test_add_item(self):
        """Test add item"""
        order = Order(1, 100)

        order.add_item(1, 2, 50.0)
        assert len(order.items) == 1
        assert order.total_amount == 100.0

        order.add_item(2, 1, 30.0)
        assert len(order.items) == 2
        assert order.total_amount == 130.0

    def test_remove_item(self):
        """Test remove item"""
        order = Order(1, 100)
        order.add_item(1, 2, 50.0)
        order.add_item(2, 1, 30.0)

        assert order.remove_item(1)
        assert len(order.items) == 1
        assert order.total_amount == 30.0

    def test_apply_discount(self):
        """Test apply discount"""
        order = Order(1, 100)
        order.add_item(1, 2, 50.0)

        order.apply_discount(0.1)
        assert order.total_amount == 90.0


class TestStore:
    """Test Store class - LỖI FORMAT"""

    def test_store_creation(self):
        """Test create store"""
        store = Store("My Store")

        assert store.name == "My Store"
        assert len(store.products) == 0

    def test_add_product(self):
        """Test add product"""
        store = Store("Test")
        product = store.add_product("Laptop", ProductCategory.ELECTRONICS, 999.99, 5)

        assert product.product_id == 1
        assert len(store.products) == 1

    def test_register_customer(self):
        """Test register customer"""
        store = Store("Test")
        customer = store.register_customer("John", "john@test.com", "0123")

        assert customer.customer_id == 1
        assert len(store.customers) == 1

    def test_create_order(self):
        """Test create order"""
        store = Store("Test")
        customer = store.register_customer("John", "john@test.com", "0123")
        order = store.create_order(customer.customer_id)

        assert order is not None
        assert order.order_id == 1

    def test_add_to_order(self):
        """Test add to order"""
        store = Store("Test")
        product = store.add_product("Laptop", ProductCategory.ELECTRONICS, 999.99, 5)
        customer = store.register_customer("John", "john@test.com", "0123")
        order = store.create_order(customer.customer_id)

        result = store.add_to_order(order.order_id, product.product_id, 2)

        assert result["success"]
        assert product.stock == 3

    def test_complete_order(self):
        """Test complete order"""
        store = Store("Test")
        product = store.add_product("Laptop", ProductCategory.ELECTRONICS, 1000.0, 5)
        customer = store.register_customer("John", "john@test.com", "0123")
        order = store.create_order(customer.customer_id)
        store.add_to_order(order.order_id, product.product_id, 1)

        result = store.complete_order(order.order_id)

        assert result["success"]
        assert customer.loyalty_points == 100

    def test_search_products(self):
        """Test search"""
        store = Store("Test")
        store.add_product("Gaming Laptop", ProductCategory.ELECTRONICS, 999.99, 5)
        store.add_product("Office Laptop", ProductCategory.ELECTRONICS, 599.99, 3)
        store.add_product("T-Shirt", ProductCategory.CLOTHING, 29.99, 10)

        results = store.search_products("Laptop")
        assert len(results) == 2

        results = store.search_products("Gaming")
        assert len(results) == 1


def test_validate_email():
    """Test email validation"""
    assert validate_email("test@example.com")
    assert validate_email("user@domain.co")
    assert validate_email("invalid") == False
    assert validate_email("@example.com") == False


def test_calculate_tax():
    """Test tax calculation"""
    assert calculate_tax(100.0) == 10.0
    assert calculate_tax(50.0, 0.2) == 10.0
    assert calculate_tax(-10.0) == 0.0


def test_format_currency():
    """Test currency format"""
    assert format_currency(1000.50) == "$1,000.50"
    assert format_currency(99.99) == "$99.99"
