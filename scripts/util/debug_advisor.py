import sys
import os
sys.path.append(os.getcwd())

try:
    from schemas.advisor import Advisor
    data = {
        "name": "Jane Fiduciary",
        "email": "jane@fiduciary.test",
        "fiduciary_status": True,
        "fiduciary_type": "RIA",
        "registration_type": "SEC",
        "firm_name": "Fiduciary Wealth",
        "fee_structure": "FEE_ONLY"
    }
    advisor = Advisor(**data)
    print(f"Success: {advisor.name}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
