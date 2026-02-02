import logging
import datetime
from services.compliance.selling_plan_service import SellingPlanService
from services.compliance.fiduciary_execution_layer import FiduciaryExecutionLayer

logger = logging.getLogger(__name__)

def create_plan():
    """
    CLI Handler for creating an executive 10b5-1 plan.
    """
    # Mock data for demonstration
    user_id = "u_exec_123"
    ticker = "NVDA"
    total_shares = 10000
    shares_per_date = 2500
    
    # Next 4 quarters
    today = datetime.date.today()
    sale_dates = [
        today + datetime.timedelta(days=90),
        today + datetime.timedelta(days=180),
        today + datetime.timedelta(days=270),
        today + datetime.timedelta(days=360)
    ]
    
    svc = SellingPlanService()
    plan = svc.create_selling_plan(user_id, ticker, total_shares, sale_dates, shares_per_date)
    
    print("\n" + "="*50)
    print("        10b5-1 SELLING PLAN CREATED")
    print("="*50)
    print(f"Plan ID:        {plan['plan_id']}")
    print(f"Ticker:         {plan['ticker']}")
    print(f"Total Shares:   {plan['total_shares']:,}")
    print("-" * 50)
    print("Execution Schedule:")
    for s in plan['schedule']:
        print(f" - {s['date']}: {s['shares']:,} shares")
    print("="*50 + "\n")

def check_status():
    """
    CLI Handler for checking plan and fiduciary status.
    """
    print("\n[*] Checking active 10b5-1 plans for compliance...")
    # Mock lookup
    print("[OK] NVDA plan for u_exec_123: Next sale in 89 days.")
    print("[OK] Fiduciary Attestation: No executive overrides detected.")

def execute_plan():
    """
    CLI Handler for manual trigger of scheduled execution (Sim).
    """
    fid = FiduciaryExecutionLayer()
    res = fid.execute_scheduled_sale("PLAN_u_exec_123_NVDA", "NVDA", 2500)
    
    print("\n" + "="*50)
    print("        10b5-1 FIDUCIARY EXECUTION")
    print("="*50)
    print(f"Execution ID:   {res['execution_id']}")
    print(f"Ticker:         {res['ticker']}")
    print(f"Shares:         {res['shares_executed']:,}")
    print("-" * 50)
    print(f"ATTESTATION: {res['fiduciary_attestation']}")
    print("="*50 + "\n")
