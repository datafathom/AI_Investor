import sys
import os

# Add project root to sys.path
PROJECT_ROOT = os.path.abspath(os.curdir)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

print(f"Testing imports from web.api.dev_api in {PROJECT_ROOT}...")

try:
    from web.api import dev_api
    print("✅ SUCCESS: web.api.dev_api imported successfully.")
except ImportError as e:
    print(f"❌ FAILED: Import Error: {e}")
    import traceback
    traceback.print_exc()
except Exception as e:
    print(f"❌ FAILED: Unexpected Error: {e}")
    import traceback
    traceback.print_exc()
