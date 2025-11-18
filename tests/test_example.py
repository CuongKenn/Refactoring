# tests/test_example.py
from app.example import (
    add_numbers,
    calculate,
    calculate_product,
    calculate_refactored,
    calculate_sum,
    multiply_numbers,
    subtract_numbers,
)


def test_add_numbers():
    """Test hàm add_numbers"""
    assert add_numbers(2, 3) == 5
    assert add_numbers(-1, 1) == 0
    assert add_numbers(0, 0) == 0
    assert add_numbers(-5, -3) == -8


def test_calculate():
    """Test hàm calculate gốc"""
    # Test trường hợp a > b (tính tổng)
    assert calculate(5, 3, 2) == 10  # 5 + 3 + 2
    assert calculate(10, 1, 5) == 16  # 10 + 1 + 5

    # Test trường hợp a <= b (tính tích)
    assert calculate(2, 3, 4) == 24  # 2 * 3 * 4
    assert calculate(1, 1, 5) == 5  # 1 * 1 * 5


def test_calculate_refactored():
    """Test hàm calculate đã refactor"""
    # Test trường hợp a > b (tính tổng)
    assert calculate_refactored(5, 3, 2) == 10  # 5 + 3 + 2
    assert calculate_refactored(10, 1, 5) == 16  # 10 + 1 + 5

    # Test trường hợp a <= b (tính tích)
    assert calculate_refactored(2, 3, 4) == 24  # 2 * 3 * 4
    assert calculate_refactored(1, 1, 5) == 5  # 1 * 1 * 5


def test_calculate_sum():
    """Test hàm calculate_sum"""
    assert calculate_sum(1, 2, 3) == 6
    assert calculate_sum(0, 0, 0) == 0
    assert calculate_sum(-1, -2, -3) == -6


def test_calculate_product():
    """Test hàm calculate_product"""
    assert calculate_product(2, 3, 4) == 24
    assert calculate_product(1, 1, 1) == 1
    assert calculate_product(0, 5, 10) == 0


def test_refactor_consistency():
    """Test để đảm bảo hàm gốc và hàm refactor cho kết quả giống nhau"""
    test_cases = [(5, 3, 2), (10, 1, 5), (2, 3, 4), (1, 1, 5), (0, 1, 2), (-1, 2, 3)]

    for a, b, c in test_cases:
        assert calculate(a, b, c) == calculate_refactored(a, b, c), f"Mismatch for inputs ({a}, {b}, {c})"


def test_subtract_numbers():
    """Test hàm subtract_numbers"""
    assert subtract_numbers(5, 3) == 2
    assert subtract_numbers(10, 7) == 3
    assert subtract_numbers(0, 0) == 0
    assert subtract_numbers(-5, -3) == -2


def test_multiply_numbers():
    """Test hàm multiply_numbers"""
    assert multiply_numbers(3, 4) == 12
    assert multiply_numbers(0, 5) == 0
    assert multiply_numbers(-2, 3) == -6
    assert multiply_numbers(-2, -3) == 6
