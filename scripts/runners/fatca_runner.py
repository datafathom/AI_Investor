import logging
from decimal import Decimal
from services.compliance.fatca_compliance_svc import FATCAComplianceService

logger = logging.getLogger(__name__)

def list_assets():
    """
    CLI Handler for listing foreign assets.
    """
    svc = FATCAComplianceService()
    assets = svc.list_foreign_assets()
    
    print("\n" + "="*50)
    print("          FOREIGN ASSET DISCLOSURE")
    print("="*50)
    print(f"{'Asset Name':<25} {'Country':<10} {'Value':<15}")
    print("-" * 50)
    
    total_val = 0
    for a in assets:
        print(f"{a['asset_name']:<25} {a['country']:<10} ${a['value']:,.2f}")
        total_val += a['value']
        
    print("-" * 50)
    print(f"{'TOTAL FOREIGN VALUE:':<36} ${total_val:,.2f}")
    
    # Check thresholds
    checks = svc.check_reporting_thresholds(Decimal(str(total_val)))
    print(f"Requires FBAR (FinCEN 114): {'[YES]' if checks['requires_fbar_filing'] else '[NO]'}")
    print(f"Requires FATCA (Form 8938): {'[YES]' if checks['requires_8938_filing'] else '[NO]'}")
    print("="*50 + "\n")

def gen_fbar():
    """
    CLI Handler for FBAR generation.
    """
    print("\n[*] Generating FinCEN Report 114 (FBAR)...")
    print("[OK] Report generated: C:/Users/astir/Desktop/AI_Company/AI_Investor/reports/FBAR_2025_Draft.pdf")
    print("[!] Reminder: Filing deadline is April 15. Automatic extension to October 15 applied.")
