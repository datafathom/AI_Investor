import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from web.fastapi_gateway import app

print("Listing all registered routes:")
for route in app.routes:
    if hasattr(route, "path"):
        print(f"{route.path} - {route.methods if hasattr(route, 'methods') else 'N/A'}")
