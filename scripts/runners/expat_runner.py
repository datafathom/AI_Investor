import logging
from decimal import Decimal
from services.tax.exit_tax_service import ExitTaxService
from services.legal.residency_timer import ResidencyTimer

logger = logging.getLogger(__name__)

def check_status():
    """
    CLI Handler for covered expatriate status check.
    """
    # Mock data for demonstration
    net_worth = Decimal("2500000.00")
    avg_tax = Decimal("210000.00")
    compliant = True
    history = list(range(2010, 2025)) # 15 years of residency
    
    svc = ExitTaxService()
    status = svc.check_covered_status(net_worth, avg_tax, compliant)
    
    timer = ResidencyTimer()
    residency = timer.validate_expatriation_eligibility(history)
    
    print("\n" + "="*50)
    print("          EXPATRIATION STATUS AUDIT")
    print("="*50)
    print(f"Net Worth:           ${net_worth:,.2f}")
    print(f"Avg Tax Liability:   ${avg_tax:,.2f}")
    print(f"Residency History:   {residency['residency_years_count']} / 15 years")
    print("-" * 50)
    
    is_covered = status['is_covered_expatriate'] or residency['is_long_term_resident']
    print(f"COVERED EXPATRIATE:  {'[YES]' if is_covered else '[NO]'}")
    
    if is_covered:
        print("Reasons:")
        for r in status['reasons']:
            print(f" - {r}")
        if residency['is_long_term_resident']:
            print(" - Long-Term Resident (8 of 15 rule)")
    print("="*50 + "\n")

def calc_bill():
    """
    CLI Handler for exit tax estimation.
    """
    unrealized_gains = Decimal("3500000.00")
    
    # Assume covered for calc demonstration
    svc = ExitTaxService()
    mock_status = {"is_covered_expatriate": True}
    
    bill = svc.calculate_exit_tax(unrealized_gains, mock_status)
    
    print("\n" + "="*50)
    print("          EXIT TAX BILL ESTIMATION")
    print("="*50)
    print(f"Unrealized Gains:     ${bill['total_unrealized_gains']:,.2f}")
    print(f"IRS Exclusion (2024): -${bill['exclusion_applied']:,.2f}")
    print(f"Taxable Gain:         ${bill['taxable_gain']:,.2f}")
    print("-" * 50)
    print(f"ESTIMATED TAX DUE:    ${bill['estimated_tax_bill']:,.2f}")
    print("="*50 + "\n")
