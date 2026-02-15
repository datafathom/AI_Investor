import sys
import os

# Add project root to sys.path
PROJECT_ROOT = os.path.abspath(os.curdir)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

print(f"Testing full import of web.fastapi_gateway in {PROJECT_ROOT}...")

try:
    # Set dummy env vars to avoid some init errors if any
    os.environ["SECRET_KEY"] = "test"
    
    from web import fastapi_gateway
    print("✅ SUCCESS: web.fastapi_gateway imported successfully.")
except ImportError as e:
    print(f"❌ FAILED: Import Error: {e}")
    import traceback
    traceback.print_exc()
except Exception as e:
    # We might expect some connection errors if it tries to init services, 
    # but we want to know about IMPORT errors specifically.
    print(f"⚠️  Import reached but failed on INIT: {e}")
    import traceback
    traceback.print_exc()
