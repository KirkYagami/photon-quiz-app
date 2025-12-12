"""
Setup verification script
Run: python setup_verify.py
"""

import os
import sys

def check_file(path, file_type="file"):
    """Check if file or directory exists"""
    exists = os.path.exists(path)
    icon = "✓" if exists else "✗"
    print(f"  {icon} {path}")
    return exists

def check_module(module_name):
    """Check if Python module is installed"""
    try:
        __import__(module_name)
        print(f"  ✓ {module_name}")
        return True
    except ImportError:
        print(f"  ✗ {module_name} (NOT INSTALLED)")
        return False

print("=" * 60)
print("QUIZ APP SETUP VERIFICATION")
print("=" * 60)

# Check directory structure
print("\n📁 Directory Structure:")
all_good = True
required_dirs = [
    "models",
    "routes",
    "utils",
    "templates",
    "templates/admin",
    "templates/quiz",
    "static",
    "static/css",
    "static/js"
]
for directory in required_dirs:
    all_good &= check_file(directory, "dir")

# Check required files
print("\n📄 Required Files:")
required_files = [
    "app.py",
    "config.py",
    "requirements.txt",
    "models/__init__.py",
    "models/database.py",
    "routes/__init__.py",
    "routes/main.py",
    "routes/admin.py",
    "routes/quiz.py",
    "utils/__init__.py",
    "utils/parsers.py",
    "utils/helpers.py",
    "templates/base.html",
    "templates/home.html",
    "templates/admin/login.html",
    "templates/admin/dashboard.html",
    "templates/quiz/take.html",
    "templates/quiz/result.html",
    "templates/quiz/review.html",
    "static/css/style.css",
    "static/js/timer.js"
]
for file in required_files:
    all_good &= check_file(file)

# Check Python modules
print("\n📦 Python Modules:")
required_modules = ["flask", "yaml", "markdown"]
for module in required_modules:
    all_good &= check_module(module)

# Summary
print("\n" + "=" * 60)
if all_good:
    print("✓ ALL CHECKS PASSED!")
    print("\nYou can now run the application:")
    print("  python app.py")
else:
    print("✗ SOME CHECKS FAILED!")
    print("\nPlease fix the issues above before running the app.")
    print("\nTo install missing modules:")
    print("  pip install -r requirements.txt")

print("=" * 60)