import sys
import os
sys.path.append(os.getcwd())

print("Attempting to import web.fastapi_gateway...")
try:
    from web.fastapi_gateway import app
    print("Import successful")
except Exception as e:
    import traceback
    traceback.print_exc()
