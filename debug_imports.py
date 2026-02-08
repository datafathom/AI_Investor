import traceback
import sys
try:
    from web.fastapi_gateway import app
    print("SUCCESS: App loaded")
except Exception:
    traceback.print_exc()
    sys.exit(1)
