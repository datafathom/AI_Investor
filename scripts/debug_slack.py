import sys
import os

print(f"Python Executable: {sys.executable}")
print(f"Python Version: {sys.version}")
print(f"Current Directory: {os.getcwd()}")
sys.path.append(os.getcwd())
print(f"Sys Path: {sys.path}")

try:
    import slack_bolt
    print(f"SUCCESS: slack_bolt imported from {slack_bolt.__file__}")
except ImportError as e:
    print(f"FAILURE: {e}")
except Exception as e:
    print(f"FAILURE (Other): {e}")

try:
    from services.notifications.slack_service import get_slack_service
    print("SUCCESS: services.notifications.slack_service imported")
except ImportError as e:
    print(f"FAILURE importing service: {e}")
except Exception as e:
    print(f"FAILURE importing service (Other): {e}")
