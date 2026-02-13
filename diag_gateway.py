import sys
import os
sys.path.append(os.getcwd())

print("Attempting to import web.fastapi_gateway...")
try:
    import web.fastapi_gateway
    print("Success!")
except Exception as e:
    import traceback
    traceback.print_exc()
