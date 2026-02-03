
import sys
import os

# Add project root to path
sys.path.append(os.getcwd())

try:
    print("Attempting to import homeostasis_service...")
    from services.portfolio.homeostasis_service import homeostasis_service
    print("SUCCESS: homeostasis_service imported.")
    
    print("Attempting to import philanthropy_service...")
    from services.execution.philanthropy_service import philanthropy_service
    print("SUCCESS: philanthropy_service imported.")
    
except Exception as e:
    print(f"FAILED: {e}")
    import traceback
    traceback.print_exc()
