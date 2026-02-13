import sys
import os
import time

sys.path.append(os.getcwd())

routers = [
    "health_api", "auth_api", "system_api", "agents_api", "dev_api",
    "debate_api", "departments_api", "master_orchestrator_api", "onboarding_api",
    "tasks_api", "dashboard_api", "brokerage_api", "strategy_api", "risk_api",
    "market_data_api", "news_api", "watchlist_api", "scanner_api", "homeostasis_api",
    "evolution_api", "identity_api", "compliance_api", "estate_api", "tax_api",
    "macro_api", "corporate_api", "margin_api", "mobile_api", "integrations_api",
    "admin", "deployments_api", "ops_api", "workspaces_api", "advanced_risk_api"
]

print("Starting Selective Import Trace...")

for r in routers:
    print(f"Importing web.api.{r}...")
    start = time.time()
    try:
        module_path = f"web.api.{r}"
        __import__(module_path)
        print(f"  - SUCCESS ({time.time() - start:.4f}s)")
    except Exception as e:
        print(f"\n!!! FAILED: {r} !!!")
        import traceback
        traceback.print_exc()
        # sys.exit(1)

print("\nSelective imports completed!")
