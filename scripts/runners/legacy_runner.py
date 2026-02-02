import logging
from decimal import Decimal
from services.treasury.cash_management_service import CashManagementService
from services.legal.philanthropy_service import PhilanthropyService

logger = logging.getLogger(__name__)

def cash_opt():
    """
    CLI Handler for cash yield optimization.
    """
    svc = CashManagementService()
    # Mock accounts
    accounts = {
        "CHECKING": Decimal("15000.00"),
        "MMA": Decimal("50000.00"),
        "HYSA": Decimal("25000.00")
    }
    res = svc.calculate_sweep_yield(accounts)
    
    print("\n" + "="*50)
    print("        TREASURY CASH OPTIMIZER")
    print("="*50)
    print(f"Annual Projected Return: ${res['total_annual_return']:,.2f}")
    print(f"Optimal Action:          {res['optimal_move']}")
    print("-" * 50)
    print("Account Breakdown:")
    for acc, details in res['account_breakdown'].items():
        print(f" - {acc:10}: ${details['amount']:,.0f} @ {details['yield_rate']:.1%}")
    print("="*50 + "\n")

def donate(amount: float):
    """
    CLI Handler for charitable donations.
    """
    svc = PhilanthropyService()
    res = svc.calculate_charitable_deduction(Decimal(str(amount)), Decimal("500000.00"), "CASH")
    
    print("\n" + "="*50)
    print(f"        CHARITABLE CONTRIBUTION: ${amount:,.2f}")
    print("="*50)
    print(f"Deductible (Current): ${res['deductible_this_year']:,.2f}")
    print(f"Carryover:            ${res['carryover_amount']:,.2f}")
    print(f"AGI Limit Reached:    {'[YES]' if res['limit_reached'] else '[NO]'}")
    print("="*50 + "\n")

def impact_report():
    """
    CLI Handler for social impact reporting.
    """
    svc = PhilanthropyService()
    # Mock history
    donations = [
        {"amount": 50000, "efficacy": 0.9},
        {"amount": 25000, "efficacy": 0.7}
    ]
    res = svc.score_social_impact(donations)
    
    print("\n" + "="*50)
    print("        SOCIAL IMPACT & LEGACY REPORT")
    print("="*50)
    print(f"Total Invested:      ${res['total_donated']:,.2f}")
    print(f"SOCIAL ID SCORE:     {res['social_id_score']:.2f} / 100")
    print(f"Impact Tier:         {res['tier']}")
    print("-" * 50)
    print("Legacy Nodes:        [ACTIVE]")
    print("="*50 + "\n")
