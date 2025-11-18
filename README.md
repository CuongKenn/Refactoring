# 🚀 Python Refactoring với CI/CD Auto-Fix

[![Python CI/CD](https://github.com/CuongKenn/Refactoring/actions/workflows/python-ci.yml/badge.svg)](https://github.com/CuongKenn/Refactoring/actions)

Dự án Python Refactoring tích hợp GitHub Actions để **tự động format code**, chạy tests và đảm bảo chất lượng code.

## 📋 Mục lục

- [Tính năng](#-tính-năng)
- [Yêu cầu hệ thống](#-yêu-cầu-hệ-thống)
- [Cài đặt](#-cài-đặt)
- [Cấu trúc dự án](#-cấu-trúc-dự-án)
- [Sử dụng](#-sử-dụng)
- [CI/CD Pipeline](#-cicd-pipeline)
- [Demo Application](#-demo-application)
- [Troubleshooting](#-troubleshooting)

---

## ✨ Tính năng

- ✅ **Auto-fix Formatting**: Tự động sửa lỗi format với Black, isort, autopep8
- ✅ **Multi-version Testing**: Test trên Python 3.8, 3.9, 3.10, 3.11
- ✅ **GitHub Actions**: CI/CD pipeline tự động
- ✅ **Code Quality**: Linting với flake8
- ✅ **Test Coverage**: Pytest với coverage reporting
- ✅ **Auto-commit**: Bot tự động commit code đã được fix

---

## 💻 Yêu cầu hệ thống

- **Python**: 3.8 trở lên
- **Git**: 2.0 trở lên
- **GitHub Account**: Để sử dụng GitHub Actions
- **Operating System**: Windows, macOS, hoặc Linux

---

## 🔧 Cài đặt

### Bước 1: Clone repository

```bash
git clone https://github.com/CuongKenn/Refactoring.git
cd Refactoring
```

### Bước 2: Tạo môi trường ảo (Virtual Environment)

**Windows:**
```cmd
python -m venv .venv
.venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Bước 3: Cài đặt dependencies

```bash
pip install -r requirements.txt
```

**Dependencies bao gồm:**
- `pytest>=7.0.0` - Testing framework
- `pytest-cov>=4.0.0` - Coverage reporting
- `flake8>=6.0.0` - Code linting
- `black>=23.0.0` - Code formatting
- `isort>=5.12.0` - Import sorting
- `autopep8>=2.0.0` - Auto PEP8 formatting

### Bước 4: Xác minh cài đặt

```bash
python -m pytest --version
python -m black --version
python -m flake8 --version
```

---

## 📁 Cấu trúc dự án

```
Refactoring/
│
├── .github/
│   └── workflows/
│       └── python-ci.yml          # GitHub Actions workflow
│
├── app/
│   ├── __init__.py
│   └── example.py                 # Demo application code
│
├── tests/
│   ├── __init__.py
│   └── test_example.py            # Test suite
│
├── .flake8                        # Flake8 configuration
├── requirements.txt               # Python dependencies
├── README.md                      # Documentation (file này)
├── QUICKSTART.md                  # Quick start guide
└── .gitignore                     # Git ignore rules
```

---

## 🎯 Sử dụng

### 1. Chạy Tests

**Chạy tất cả tests:**
```bash
pytest
```

**Chạy tests với output chi tiết:**
```bash
pytest -v
```

**Chạy tests với coverage:**
```bash
pytest --cov=app --cov-report=html
```

**Chạy một test file cụ thể:**
```bash
pytest tests/test_example.py
```

**Chạy một test function cụ thể:**
```bash
pytest tests/test_example.py::TestProduct::test_product_creation
```

### 2. Kiểm tra Code Quality

**Chạy flake8 để tìm lỗi:**
```bash
flake8 app tests
```

**Đếm số lỗi:**
```bash
flake8 app tests --count
```

**Xem lỗi chi tiết với line numbers:**
```bash
flake8 app tests --show-source
```

### 3. Format Code (Local)

**Format với Black:**
```bash
black app tests
```

**Sort imports với isort:**
```bash
isort app tests
```

**Auto-fix với autopep8:**
```bash
autopep8 --in-place --aggressive --aggressive -r app tests
```

**Format tất cả cùng lúc:**
```bash
black app tests && isort app tests && autopep8 --in-place --aggressive --aggressive -r app tests
```

### 4. Workflow Development

**Quy trình làm việc chuẩn:**

```bash
# 1. Tạo branch mới
git checkout -b feature/ten-tinh-nang

# 2. Viết code
# ... code trong app/example.py ...

# 3. Viết tests
# ... tests trong tests/test_example.py ...

# 4. Chạy tests local
pytest -v

# 5. Commit và push (không cần format trước)
git add .
git commit -m "feat: thêm tính năng mới"
git push origin feature/ten-tinh-nang

# 6. GitHub Actions sẽ tự động:
#    - Chạy tests
#    - Auto-fix formatting
#    - Commit code đã được fix
#    - Run linting

# 7. Pull code đã được fix về
git pull origin feature/ten-tinh-nang

# 8. Tạo Pull Request trên GitHub
```

---

## 🤖 CI/CD Pipeline

### GitHub Actions Workflow

Pipeline tự động chạy khi:
- Push code lên branch `main`
- Tạo Pull Request

### Các bước trong Pipeline:

#### **Job 1: Test**
Chạy trên matrix Python 3.8, 3.9, 3.10, 3.11

```yaml
1. Checkout code
2. Setup Python
3. Install dependencies
4. Run pytest
```

#### **Job 2: Lint and Format**
Chỉ chạy trên Python 3.11

```yaml
1. Checkout code
2. Setup Python
3. Install dependencies
4. Run Black formatter
5. Run isort
6. Run autopep8
7. Commit changes (nếu có)
8. Push fixed code
9. Run flake8 linting
```

### Xem kết quả Pipeline

1. Truy cập: https://github.com/CuongKenn/Refactoring/actions
2. Click vào workflow run mới nhất
3. Xem chi tiết từng job:
   - ✅ **test (3.8)** - Test trên Python 3.8
   - ✅ **test (3.9)** - Test trên Python 3.9
   - ✅ **test (3.10)** - Test trên Python 3.10
   - ✅ **test (3.11)** - Test trên Python 3.11
   - ✅ **lint-and-format** - Auto-fix và linting

### Cách hoạt động của Auto-fix

**Trước khi push:**
```python
# Code với lỗi formatting
def calculate(a,b):
    return a+b
```

**Sau khi GitHub Actions chạy:**
```python
# Code đã được auto-fix
def calculate(a, b):
    return a + b
```

**Commits:**
```
abc1234 - Your commit message (bạn)
def5678 - 🤖 Auto-fix: Format code with Black, isort, and autopep8 (github-actions[bot])
```

---

## 🛍️ Demo Application

Dự án bao gồm một **E-commerce Product Management System** hoàn chỉnh.

### Tính năng Demo:

#### 1. **Product Management**
- Tạo sản phẩm với giá, stock, category
- Kiểm tra tồn kho
- Cập nhật stock
- Áp dụng discount

#### 2. **Customer Management**
- Đăng ký khách hàng
- Hệ thống điểm loyalty
- Tính discount theo tier (Bronze/Silver/Gold)
- Validate email

#### 3. **Order Management**
- Tạo đơn hàng
- Thêm/xóa sản phẩm
- Áp dụng discount
- Tính thuế
- Xử lý thanh toán

#### 4. **Store Operations**
- Quản lý inventory
- Tìm kiếm sản phẩm
- Xử lý đơn hàng end-to-end

### Chạy Demo:

```bash
# Import và sử dụng
python -c "
from app.example import Store, Product, Customer, ProductCategory

# Tạo store
store = Store('TechMart')

# Thêm sản phẩm
laptop = Product('LAP001', 'Gaming Laptop', 1200.0, 10, ProductCategory.ELECTRONICS)
store.add_product(laptop)

# Đăng ký khách hàng
customer = Customer('C001', 'John Doe', 'john@example.com')
store.register_customer(customer)

# Tạo và xử lý đơn hàng
order = store.create_order('C001')
store.add_to_order(order.order_id, 'LAP001', 1)
result = store.complete_order(order.order_id)

print(f'Tổng tiền: \${result[\"total\"]:.2f}')
"
```

### Chạy Tests cho Demo:

```bash
# Chạy tất cả 22 tests
pytest tests/test_example.py -v

# Output:
# test_product_creation PASSED
# test_product_is_in_stock PASSED
# test_customer_creation PASSED
# test_add_loyalty_points PASSED
# test_order_creation PASSED
# test_store_creation PASSED
# ... (22 tests total)
```

---

## 🔍 Troubleshooting

### Lỗi: "No module named 'pytest'"

**Nguyên nhân:** Chưa cài dependencies

**Giải pháp:**
```bash
pip install -r requirements.txt
```

### Lỗi: "GitHub Actions workflow not found"

**Nguyên nhân:** File workflow chưa được push

**Giải pháp:**
```bash
git add .github/workflows/python-ci.yml
git commit -m "Add CI/CD workflow"
git push origin main
```

### Lỗi: "Permission denied (github-actions[bot])"

**Nguyên nhân:** Workflow không có quyền write

**Giải pháp:**
1. Vào GitHub repository → Settings
2. Actions → General
3. Workflow permissions → Check "Read and write permissions"
4. Save

### Auto-fix không commit changes

**Nguyên nhân:** Không có thay đổi hoặc permissions không đủ

**Kiểm tra:**
```bash
# Xem git log
git log --oneline -5

# Nếu không thấy commit từ github-actions[bot]:
# 1. Check workflow permissions (như trên)
# 2. Verify có lỗi format không:
flake8 app tests --count
```

### Tests failed trên GitHub nhưng pass ở local

**Nguyên nhân:** Khác biệt môi trường Python version

**Giải pháp:**
```bash
# Test trên nhiều Python versions local
tox  # nếu có tox configured

# Hoặc test cụ thể version
python3.8 -m pytest
python3.9 -m pytest
python3.10 -m pytest
python3.11 -m pytest
```

### Code bị format khác giữa local và GitHub

**Nguyên nhân:** Version tools khác nhau

**Giải pháp:**
```bash
# Cập nhật tools lên version mới nhất
pip install --upgrade black isort autopep8 flake8

# Hoặc dùng chính xác version trong requirements.txt
pip install -r requirements.txt --force-reinstall
```

### Flake8 báo lỗi sau khi auto-fix

**Nguyên nhân:** Một số lỗi không thể auto-fix (logic issues, unused imports)

**Giải pháp:**
```bash
# Xem lỗi còn lại
flake8 app tests --show-source

# Fix thủ công:
# - F401: Remove unused imports
# - E712: Change == True to is True
# - Complexity: Refactor code
```

### Virtual environment không activate

**Windows CMD:**
```cmd
.venv\Scripts\activate.bat
```

**Windows PowerShell:**
```powershell
.venv\Scripts\Activate.ps1

# Nếu lỗi execution policy:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**macOS/Linux:**
```bash
source .venv/bin/activate
```

---

## 📚 Commands Cheat Sheet

### Setup & Installation
```bash
# Clone repository
git clone https://github.com/CuongKenn/Refactoring.git
cd Refactoring

# Create virtual environment
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate

# Activate (Linux/Mac)
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Testing
```bash
# Run all tests
pytest

# Verbose output
pytest -v

# With coverage
pytest --cov=app

# HTML coverage report
pytest --cov=app --cov-report=html

# Specific test file
pytest tests/test_example.py

# Specific test
pytest tests/test_example.py::TestProduct::test_product_creation
```

### Code Quality
```bash
# Flake8 linting
flake8 app tests

# Count errors
flake8 app tests --count

# Show source
flake8 app tests --show-source

# Check specific file
flake8 app/example.py
```

### Formatting
```bash
# Black
black app tests

# Check only (no changes)
black --check app tests

# isort
isort app tests

# Check only
isort --check-only app tests

# autopep8
autopep8 --in-place --aggressive --aggressive -r app tests

# All formatters
black app tests && isort app tests && autopep8 --in-place --aggressive --aggressive -r app tests
```

### Git Operations
```bash
# Check status
git status

# View recent commits
git log --oneline -5

# View changes
git diff

# Add all changes
git add .

# Commit
git commit -m "your message"

# Push
git push origin main

# Pull latest
git pull origin main

# Create branch
git checkout -b feature/new-feature

# Switch branch
git checkout main
```

### GitHub Actions
```bash
# View workflows
# Go to: https://github.com/CuongKenn/Refactoring/actions

# Check workflow status
git log --oneline -5
# Look for commits from github-actions[bot]

# Pull auto-fixed code
git pull origin main
```

---

## 📊 Thống kê dự án

- **Languages**: Python
- **Lines of Code**: ~500+
- **Test Coverage**: 100%
- **Tests**: 22 unit tests
- **CI/CD**: GitHub Actions
- **Auto-fix Rate**: 99% (619 errors → 6 errors)

---

## 🎓 Best Practices

### 1. Commit Messages

```bash
# ✅ Good
git commit -m "feat: add customer loyalty system"
git commit -m "fix: resolve inventory stock issue"
git commit -m "test: add unit tests for Order class"
git commit -m "docs: update README with new examples"

# ❌ Bad
git commit -m "update"
git commit -m "fix bug"
git commit -m "changes"
```

### 2. Code Organization

- ✅ Một class một file (khi project lớn)
- ✅ Tách logic business ra khỏi tests
- ✅ Sử dụng type hints
- ✅ Viết docstrings cho functions/classes

### 3. Testing

- ✅ Test coverage ≥ 80%
- ✅ Test cả happy path và edge cases
- ✅ Sử dụng fixtures cho setup
- ✅ Mỗi test chỉ test một behavior

### 4. Git Workflow

```bash
# 1. Luôn pull trước khi làm việc
git pull origin main

# 2. Tạo branch cho feature mới
git checkout -b feature/new-feature

# 3. Commit thường xuyên
git add .
git commit -m "feat: implement X"

# 4. Push và để CI/CD xử lý
git push origin feature/new-feature

# 5. Pull code đã được auto-fix
git pull origin feature/new-feature

# 6. Merge vào main qua Pull Request
```

---

## 📚 Tài liệu tham khảo

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Pytest Documentation](https://docs.pytest.org/)
- [Black Documentation](https://black.readthedocs.io/)
- [Flake8 Rules](https://www.flake8rules.com/)
- [PEP 8 Style Guide](https://peps.python.org/pep-0008/)
- [isort Documentation](https://pycqa.github.io/isort/)

---

## 📝 License

MIT License - Xem file LICENSE để biết thêm chi tiết.

---

## 👥 Contributing

Contributions are welcome! Please follow these steps:

1. Fork repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'feat: Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

## 📞 Contact

- **Author**: CuongKenn
- **GitHub**: [@CuongKenn](https://github.com/CuongKenn)
- **Repository**: [Refactoring](https://github.com/CuongKenn/Refactoring)

---

## 🎉 Acknowledgments

- GitHub Actions team for the awesome CI/CD platform
- Python Software Foundation for the amazing language
- All contributors to Black, pytest, flake8, and other tools

---

**Made with ❤️ by CuongKenn**
