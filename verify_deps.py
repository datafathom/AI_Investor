
import importlib
import sys

dependencies = [
    'flask',
    'flask_socketio',
    'flask_compress',
    'flask_cors',
    'sentry_sdk',
    'flasgger',
    'psutil',
    'kafka',
    'psycopg2',
    'neo4j',
    'redis',
    'pydantic',
    'dotenv',
    'requests'
]

print("--- Dependency Verification ---")
for dep in dependencies:
    try:
        importlib.import_module(dep)
        print(f"[OK] {dep}")
    except ImportError as e:
        print(f"[MISSING] {dep}: {e}")

print("\nPython executable:", sys.executable)
print("Python path:", sys.path)
