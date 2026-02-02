from services.sfo.sfo_justification import SFOJustificationEngine
from services.planning.spending_rule import SpendingRule
from services.sfo.governance import GovernanceService

logger = logging.getLogger(__name__)

def calc_spending(aum: float, returns: float, inflation: float):
    """
    CLI Handler for safe spending calculation.
    """
    rule = SpendingRule()
    res = rule.calculate_safe_spend(
        Decimal(str(aum)),
        Decimal(str(returns / 100)),
        Decimal(str(inflation / 100))
    )
    
    print("\n" + "="*50)
    print("          SFO SUSTAINABLE SPENDING REPORT")
    print("="*50)
    print(f"Portfolio Value:  ${aum:,.2f}")
    print(f"Safe Spend Rate:  {res['safe_spend_rate_pct']}%")
    print("-" * 50)
    print(f"MAX ANNUAL SPEND: ${res['max_spend_usd']:,.2f}")
    print(f"Strategy:         {res['status']}")
    print("="*50 + "\n")

def audit_governance(family_id: str):
    """
    CLI Handler for governance audit.
    """
    import uuid
    gov = GovernanceService()
    # Mock constitution creation and ratification for CLI demo
    c = gov.create_constitution(uuid.UUID(family_id), "Preserve wealth for 100 years.", ["Integrity", "Impact"])
    res = gov.ratify_constitution(c['id'], [uuid.uuid4()])
    
    print("\n" + "="*50)
    print("          SFO GOVERNANCE AUDIT")
    print("="*50)
    print(f"Constitution ID:  {res['id']}")
    print(f"Status:           {res['status']}")
    print(f"Ratified On:      {res['date']}")
    print(f"Signatories:      {res['signers']}")
    print("="*50 + "\n")

def analyze_sfo(aum: str, external_bps: int = 100):
    """
    CLI Handler for SFO Economics Analysis.
    """
    try:
        aum_val = Decimal(aum.replace(',', ''))
        engine = SFOJustificationEngine()
        result = engine.run_breakeven_analysis(aum_val, external_bps)
        
        print("\n" + "="*50)
        print("          SFO ECONOMIC VIABILITY REPORT")
        print("="*50)
        print(f"Target AUM:         ${aum_val:,.2f}")
        print(f"External Fees:      ${result['external_annual_fees']:,.2f} ({external_bps} bps)")
        print(f"Internal OpEx Est:  ${result['internal_operating_est']:,.2f}")
        print(f"Estimated Savings:  ${result['annual_savings']:,.2f}")
        print("-" * 50)
        status = "VIABLE ✅" if result['is_sfo_economically_viable'] else "NOT VIABLE ❌"
        print(f"DECISION:           {status}")
        print("="*50 + "\n")
        
    except Exception as e:
        logger.error(f"SFO Analysis Failed: {e}")
        print(f"Error: {e}")

def budget_template():
    """
    CLI Handler for SFO Budget Template.
    """
    engine = SFOJustificationEngine()
    template = engine.get_standard_budget()
    
    print("\n" + "="*50)
    print("          STANDARD SFO BUDGET TEMPLATE")
    print("="*50)
    print(json.dumps(template, indent=4))
    print("="*50 + "\n")

def calc_clew():
    """
    CLI Handler for CLEW (Cost of Living Extremely Well) Index.
    """
    from services.economics.clew_index_svc import ClewIndexService
    
    svc = ClewIndexService()
    idx = svc.calculate_current_index()
    inflation = svc.get_uhnwi_inflation_rate()
    
    print("\n" + "="*50)
    print("      CLEW INDEX (UHNWI INFLATION TRACKER)")
    print("="*50)
    print(f"Current Index Level:  {idx:,.2f}")
    print(f"UHNWI Inflation:      {inflation:.2f}% (Annual)")
    print(f"CPI Reference:        3.10% (Official)")
    print("-" * 50)
    print(f"Luxury Premium:       +{inflation - 3.1:.2f}%")
    print("="*50 + "\n")

def check_dilution():
    """
    CLI Handler for Inter-Generational Dilution Tracking.
    """
    from services.estate.dilution_tracker import DilutionTracker
    
    svc = DilutionTracker()
    # Mock projection for CLI
    res = svc.project_wealth_per_capita(years=30, generations=2)
    
    print("\n" + "="*50)
    print("      DYNASTIC WEALTH DILUTION REPORT")
    print("="*50)
    print(f"Current G1 Wealth:    ${res['current_wealth']:,.2f}")
    print(f"Projected G3 Members: {res['future_members']}")
    print("-" * 50)
    print(f"Wealth Per Capita (Now):  ${res['wpc_now']:,.2f}")
    print(f"Wealth Per Capita (30y):  ${res['wpc_future']:,.2f}")
    print(f"Dilution Impact:          {res['dilution_pct']:.1f}%")
    print("="*50 + "\n")
