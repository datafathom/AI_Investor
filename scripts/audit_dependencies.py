
import sys
import os
# Add project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.system.supply_chain_service import get_supply_chain_service

if __name__ == "__main__":
    print("Running Dependency Audit (pip-audit)...")
    service = get_supply_chain_service()
    result = service.run_audit()
    print(f"Audit Complete. Status: {result.get('status')}")
    print(f"Vulnerabilities Found: {result.get('vulnerabilities')}")
