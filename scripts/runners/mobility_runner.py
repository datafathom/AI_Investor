import logging
from services.legal.citizenship_service import CitizenshipService
from services.legal.passport_gate import PassportGate

logger = logging.getLogger(__name__)

def check_visa(country: str):
    """
    CLI Handler for Golden Visa program details.
    """
    svc = CitizenshipService()
    res = svc.get_program_details(country)
    
    if "error" in res:
        print(f"\n[ERROR] {res['error']}")
        return

    print("\n" + "="*50)
    print(f"        GOLDEN VISA PROGRAM: {country.upper()}")
    print("="*50)
    print(f"Cost:                ${res['cost']:,.2f}")
    print(f"Investment Type:     {res['type']}")
    print(f"EU Access:           {'[YES]' if res['eu_access'] else '[NO]'}")
    print(f"Tax Benefit:         {res['tax_benefit']}")
    print("="*50 + "\n")

def renunciation_risk(has_pass: str, stability: float):
    """
    CLI Handler for statelessness risk scoring.
    """
    svc = CitizenshipService()
    has_replacement = str(has_pass).lower() == "true"
    res = svc.calculate_stateless_risk(has_replacement, float(stability))
    
    print("\n" + "="*50)
    print("        STATELESSNESS RISK ASSESSMENT")
    print("="*50)
    print(f"Replacement Pass:    {'[YES]' if has_replacement else '[NO]'}")
    print(f"Home Stability:      {stability:.2%}")
    print("-" * 50)
    print(f"RISK SCORE:          {res['risk_score']:.2f} / 1.00")
    print(f"STATUS:              {res['status']}")
    print(f"RECOMMENDATION:      {res['recommendation']}")
    print("="*50 + "\n")
