from decimal import Decimal
from services.compliance.ppli_gate import PPLIEligibilityGate
from services.insurance.ppli_withdrawal import PPLIWithdrawalEngine
from services.insurance.efficiency_ranker import TaxEfficiencyRanker
from services.insurance.premium_opt import PremiumCadenceOptimizer

logger = logging.getLogger(__name__)

def optimize_premium(total: float, years: int, rate: float):
    """
    CLI Handler for premium cadence optimization.
    """
    opt = PremiumCadenceOptimizer()
    res = opt.compare_cadence(Decimal(str(total)), years, Decimal(str(rate / 100)))
    
    print("\n" + "="*50)
    print("          PPLI PREMIUM OPTIMIZER")
    print("="*50)
    print(f"Total Premium:   ${total:,.2f}")
    print(f"Spread Years:    {years}")
    print(f"Projected ROI:   {rate}%")
    print("-" * 50)
    print(f"Dump-In FV:      ${res['dump_in_fv']:,.2f}")
    print(f"Level Pay FV:    ${res['level_pay_fv']:,.2f}")
    print(f"TIMING ALPHA:    ${res['timing_alpha']:,.2f}")
    print(f"Recommendation:  {res['recommendation']}")
    print("="*50 + "\n")

def rank_assets():
    """
    CLI Handler for PPLI asset selection.
    """
    # Mock portfolio for ranking
    portfolio = [
        {"ticker": "CRED-ETF", "type": "DEBT", "yield": 0.08, "turnover": 0.20},
        {"ticker": "HEDGE-X", "type": "ALTS", "yield": 0.02, "turnover": 1.50},
        {"ticker": "SPY", "type": "EQUITY", "yield": 0.015, "turnover": 0.05}
    ]
    
    ranker = TaxEfficiencyRanker()
    ranked = ranker.rank_assets(portfolio, Decimal('0.37'), Decimal('0.35'))
    
    print("\n" + "="*50)
    print("          PPLI ASSET SELECTION (TAX DRAG)")
    print("="*50)
    print(f"{'Ticker':<10} | {'Type':<8} | {'Tax Drag (BPS)':<15} | {'Priority'}")
    print("-" * 50)
    for asset in ranked:
        print(f"{asset['ticker']:<10} | {asset['type']:<8} | {asset['tax_drag_bps']:<15} | {asset['ppli_priority']}")
    print("="*50 + "\n")

def check_mec(premium: float, limit: float):
    """
    CLI Handler for MEC (Modified Endowment Contract) testing.
    """
    gate = PPLIEligibilityGate()
    res = gate.check_mec_status(premium, limit)
    
    print("\n" + "="*50)
    print("          PPLI MEC (7-PAY) TEST")
    print("="*50)
    print(f"Premium Paid:     ${premium:,.2f}")
    print(f"7-Pay Limit:      ${limit:,.2f}")
    print("-" * 50)
    print(f"Status:           {res['status']}")
    print(f"Tax Advantaged:   {res['loan_tax_advantage']}")
    print(f"Premium Headroom: ${res['headroom']:,.2f}")
    print("="*50 + "\n")

def get_ppli_value(account_id: str):
    """
    CLI Handler for fetching PPLI cash value (Mock).
    """
    # Mock data
    cash_value = 12500000.0
    coi = 45000.0
    
    engine = PPLIWithdrawalEngine()
    res = engine.calculate_max_loan(cash_value, coi)
    
    print("\n" + "="*50)
    print(f"          PPLI ACCOUNT VALUE: {account_id}")
    print("="*50)
    print(f"Cash Value:       ${cash_value:,.2f}")
    print(f"Annual COI:       ${coi:,.2f}")
    print("-" * 50)
    print(f"Max Safe Loan:    ${res['max_safe_loan']:,.2f}")
    print(f"Buffer Retained:  ${res['lapse_buffer_retained']:,.2f}")
    print(f"LTV Ratio:        {res['loan_to_value_pct']:.2%}")
    print("="*50 + "\n")
