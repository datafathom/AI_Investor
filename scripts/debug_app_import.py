import sys
import os
sys.path.append(os.getcwd())

print("Attempting to import web.fastapi_gateway.app...")
try:
    from web.fastapi_gateway import app
    print("SUCCESS: App imported.")
except Exception as e:
    import traceback
    traceback.print_exc()
