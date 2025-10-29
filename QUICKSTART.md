# Hướng dẫn khởi động nhanh

## Các lệnh cơ bản để sử dụng dự án

### 1. Kích hoạt virtual environment
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 2. Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### 3. Chạy tests
```bash
pytest -v
```

### 4. Chạy linting
```bash
flake8 app/ tests/
```

### 5. Chạy tests với coverage
```bash
pip install pytest-cov
pytest --cov=app
```

### 6. Để đẩy lên GitHub và kích hoạt CI/CD:
```bash
git init
git add .
git commit -m "Initial commit: Python refactor CI/CD demo"
git branch -M main
git remote add origin <your-github-repo-url>
git push -u origin main
```

## Cấu trúc dự án hoàn chỉnh:
```
python-refactor-ci/
├── .github/
│   └── workflows/
│       └── python-ci.yml    # GitHub Actions CI/CD
├── app/
│   ├── __init__.py
│   └── example.py           # Code với ví dụ refactoring
├── tests/
│   ├── __init__.py
│   └── test_example.py      # Unit tests
├── venv/                    # Virtual environment
├── .flake8                  # Flake8 config
├── .gitignore              # Git ignore rules
├── requirements.txt        # Dependencies
├── README.md              # Documentation
└── QUICKSTART.md          # File này
```

## Lưu ý quan trọng:
- Luôn kích hoạt virtual environment trước khi làm việc
- Chạy tests trước khi commit code
- GitHub Actions sẽ tự động chạy khi push lên GitHub
- Pipeline sẽ fail nếu tests fail hoặc có lỗi linting