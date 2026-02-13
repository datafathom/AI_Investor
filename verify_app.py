import sys
import os
from pathlib import Path

# Add project root to sys.path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

print(f"Current Working Directory: {os.getcwd()}")
print(f"Python Executable: {sys.executable}")

try:
    print("Attempting to import app from web.fastapi_gateway...")
    from web.fastapi_gateway import app
    print("✅ App imported successfully!")
    
    # Check total routers
    print(f"Total routes registered: {len(app.routes)}")
except Exception as e:
    import traceback
    print("❌ Failed to import app!")
    traceback.print_exc()
    sys.exit(1)
