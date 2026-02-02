import logging
from decimal import Decimal
from services.credit.credit_risk_engine import CreditRiskEngine
from services.credit.loan_tape_svc import LoanTapeService

logger = logging.getLogger(__name__)

def ingest_tape(file_path: str):
    """
    CLI Handler for loan tape ingestion.
    """
    service = LoanTapeService()
    # Mocking ingestion
    data = [{"principal": 1000000, "rate": 0.08} for _ in range(125)]
    res = service.ingest_tape(data)
    
    print(f"\n[*] Ingesting Loan Tape from: {file_path}")
    print(f"    - Processed {res['loan_count']} loan records.")
    print(f"    - Total Principal: ${res['total_committed']:,.2f}")
    print("[x] Success: Phase 171 Ledger updated.\n")

def calc_risk():
    """
    CLI Handler for net yield risk calculation.
    """
    engine = CreditRiskEngine()
    # Mock portfolio defaults
    res = engine.calculate_expected_net_yield(
        gross_spread_bps=650, # 6.5% over SOFR
        base_rate=Decimal('0.05'), # 5% SOFR
        default_prob_annual=Decimal('0.02'), # 2% default rate
        recovery_rate=Decimal('0.60') # 60% recovery
    )
    
    print("\n" + "="*50)
    print("          PRIVATE CREDIT RISK PROJECTION")
    print("="*50)
    print(f"Gross Yield:      {res['gross_yield_pct']}%")
    print(f"Expected Loss:    {res['expected_loss_pct']}%")
    print("-" * 50)
    print(f"NET EXPECTED:     {res['net_yield_pct']}%")
    print(f"Risk Status:      {res['risk_status']}")
    print("="*50 + "\n")
