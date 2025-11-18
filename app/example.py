# app/example.py


def add_numbers(a, b):
    """
    Hàm cộng hai số
    """
    return a + b


def calculate(a, b, c):
    """
    Hàm tính toán phức tạp - cần refactor
    """
    if a > b:
        result = a + b + c
    else:
        result = a * b * c
    return result


def calculate_sum(a, b, c):
    """
    Hàm tính tổng ba số
    """
    return a + b + c


def calculate_product(a, b, c):
    """
    Hàm tính tích ba số
    """
    return a * b * c


def calculate_refactored(a, b, c):
    """
    Hàm tính toán đã được refactor - dễ đọc hơn
    """
    if a > b:
        return calculate_sum(a, b, c)
    else:
        return calculate_product(a, b, c)


def subtract_numbers(a, b):
    """
    Hàm trừ hai số - thêm để demo CI/CD
    """
    return a - b


def multiply_numbers(a, b):
    """
    Hàm nhân hai số - thêm để demo CI/CD
    """
    return a * b
