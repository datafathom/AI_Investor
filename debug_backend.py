import sys
import os

print("--- DEBUG START ---")
print(f"CWD: {os.getcwd()}")
try:
    print(sys.path)
    # import web
    # print(f"Web path: {web.__path__}")
    from web import auth_utils
    print("✅ SUCCESS: Imported web.auth_utils")
    from web import fastapi_gateway
    print("✅ SUCCESS: Imported web.fastapi_gateway")
except SyntaxError as e:
    print(f"❌ SyntaxError: {e}")
    print(f"File: {e.filename}, Line: {e.lineno}")
    print(f"Text: {e.text}")
except Exception as e:
    print(f"❌ Error: {e}")
