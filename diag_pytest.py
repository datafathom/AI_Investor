import pytest
from pathlib import Path
import os

PROJECT_ROOT = Path(os.getcwd())
TESTS_DIR = PROJECT_ROOT / "tests"
API_DIR = TESTS_DIR / "api"

print(f"Project Root: {PROJECT_ROOT}")
print(f"API Dir: {API_DIR}")
print(f"API Dir Exists: {API_DIR.exists()}")

print("\n--- Testing absolute path ---")
pytest.main(["-v", "--collect-only", str(API_DIR)])

print("\n--- Testing relative path ---")
pytest.main(["-v", "--collect-only", "tests/api"])
