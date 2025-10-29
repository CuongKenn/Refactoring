# Python Refactor CI/CD Demo

🚀 **CI/CD Status:** [![Python CI/CD Pipeline](https://github.com/CuongKenn/Refactoring/actions/workflows/python-ci.yml/badge.svg)](https://github.com/CuongKenn/Refactoring/actions/workflows/python-ci.yml)

## Mô tả

Đây là một dự án demo về việc tích hợp CI/CD với Python, bao gồm:
- Unit testing với pytest
- Code linting với flake8
- Automated testing với GitHub Actions
- Code refactoring examples

## Cấu trúc dự án

```
python-refactor-ci/
│
├── app/
│   ├── __init__.py
│   └── example.py          # Code ví dụ với các hàm cần refactor
├── tests/
│   ├── __init__.py
│   └── test_example.py     # Unit tests
├── .github/
│   └── workflows/
│       └── python-ci.yml  # GitHub Actions workflow
├── requirements.txt        # Dependencies
├── venv/                   # Virtual environment
└── README.md              # Documentation

```

## Cài đặt

### 1. Clone repository và tạo virtual environment

```bash
git clone <repository-url>
cd python-refactor-ci
python -m venv venv

# Kích hoạt virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

### 2. Cài đặt dependencies

```bash
pip install -r requirements.txt
```

## Sử dụng

### Chạy tests

```bash
pytest
```

### Chạy tests với coverage

```bash
pytest --cov=app
```

### Chạy linting

```bash
flake8 app/ tests/
```

### Chạy tất cả checks

```bash
# Linting
flake8 app/ tests/

# Testing
pytest -v

# Coverage
pytest --cov=app --cov-report=html
```

## Ví dụ về Refactoring

### Code trước khi refactor:

```python
def calculate(a, b, c):
    if a > b:
        result = a + b + c
    else:
        result = a * b * c
    return result
```

### Code sau khi refactor:

```python
def calculate_sum(a, b, c):
    return a + b + c

def calculate_product(a, b, c):
    return a * b * c

def calculate_refactored(a, b, c):
    if a > b:
        return calculate_sum(a, b, c)
    else:
        return calculate_product(a, b, c)
```

### Lợi ích của refactoring:

1. **Tách biệt logic**: Mỗi hàm có một trách nhiệm duy nhất
2. **Dễ test**: Có thể test từng hàm riêng biệt
3. **Dễ đọc**: Code rõ ràng và dễ hiểu hơn
4. **Tái sử dụng**: Các hàm helper có thể dùng ở nơi khác

## CI/CD Pipeline

GitHub Actions workflow sẽ tự động chạy khi:
- Push code lên branch `main` hoặc `develop`
- Tạo Pull Request về branch `main`

### Pipeline bao gồm:

1. **Testing**:
   - Chạy trên nhiều phiên bản Python (3.8, 3.9, 3.10, 3.11)
   - Chạy unit tests với pytest
   - Tạo coverage report

2. **Linting & Formatting**:
   - Kiểm tra code style với flake8
   - Kiểm tra formatting với Black
   - Kiểm tra import order với isort
   - Type checking với mypy

3. **Security**:
   - Security scanning với bandit
   - Vulnerability checking với safety

## Development Workflow

1. **Trước khi commit**:
   ```bash
   # Chạy tests
   pytest
   
   # Kiểm tra linting
   flake8 app/ tests/
   
   # Format code (optional)
   black .
   isort .
   ```

2. **Commit và push**:
   ```bash
   git add .
   git commit -m "Your commit message"
   git push origin main
   ```

3. **Theo dõi pipeline**:
   - Vào tab "Actions" trong GitHub repository
   - Kiểm tra kết quả của từng step

## Best Practices

### 1. Testing
- Viết tests trước khi refactor
- Đảm bảo coverage >= 80%
- Test cả happy path và edge cases

### 2. Refactoring
- Refactor từng bước nhỏ
- Chạy tests sau mỗi bước refactor
- Giữ nguyên behavior của code

### 3. CI/CD
- Không merge code khi tests fail
- Kiểm tra kết quả pipeline trước khi merge
- Fix linting errors ngay lập tức

## Tools sử dụng

- **pytest**: Unit testing framework
- **flake8**: Code linting
- **black**: Code formatting
- **isort**: Import sorting
- **mypy**: Static type checking
- **bandit**: Security linting
- **safety**: Dependency vulnerability scanner
- **GitHub Actions**: CI/CD platform

## Troubleshooting

### Lỗi thường gặp:

1. **ImportError**: Đảm bảo virtual environment đã được kích hoạt
2. **Test failures**: Kiểm tra logic và test cases
3. **Linting errors**: Chạy `flake8` và fix theo suggestions
4. **Coverage thấp**: Thêm tests cho các cases chưa được cover

## Contributing

1. Fork repository
2. Tạo feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Tạo Pull Request

## License

Dự án này được tạo cho mục đích học tập và demo.