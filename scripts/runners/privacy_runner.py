--import logging
from services.security.privacy_blocker import PrivacyBlockerService
from services.analysis.privacy_score import PrivacyScorer

logger = logging.getLogger(__name__)

def enable_lockdown(office_id: str):
    """
    CLI Handler for enabling full privacy mode.
    """
    service = PrivacyBlockerService()
    res = service.enforce_lockdown(office_id, mode='BLACK_HOLE')
    
    print("\n" + "!"*50)
    print("          SFO PRIVACY LOCKDOWN ACTIVATED")
    print("!"*50)
    print(f"Office ID:      {office_id}")
    print(f"Mode:           {res['privacy_mode']}")
    print(f"Audit Status:   {res['audit_sharing_status']}")
    print("-" * 50)
    print("WARNING: External data sync (Plaid/Yodlee) DISCONNECTED.")
    print("!"*50 + "\n")

def check_privacy_status():
    """
    CLI Handler for privacy advantage scoring.
    """
    scorer = PrivacyScorer()
    # Comparison
    sfo_res = scorer.calculate_privacy_score("SFO", uses_third_party_custodian=False, public_filings_required=False)
    mfo_res = scorer.calculate_privacy_score("MFO", uses_third_party_custodian=True, public_filings_required=True)
    
    print("\n" + "="*50)
    print("          PRIVACY ADVANTAGE AUDIT")
    print("="*50)
    print(f"SFO Score:    {sfo_res['privacy_score']}/100 ({sfo_res['rating']})")
    print(f"MFO Score:    {mfo_res['privacy_score']}/100 ({mfo_res['rating']})")
    print("-" * 50)
    print(f"Net Advantage: +{sfo_res['privacy_score'] - mfo_res['privacy_score']} points for SFO.")
    print("="*50 + "\n")
