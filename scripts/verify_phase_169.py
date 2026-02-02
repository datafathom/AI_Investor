import sys
import os
import logging
from decimal import Decimal

# Add project root to path
sys.path.append(os.getcwd())

# Remove script's directory from path to avoid shadowing the 'neo4j' library
script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir in sys.path:
    sys.path.remove(script_dir)

from services.security.privacy_blocker import PrivacyBlockerService
from services.sfo.dark_asset_service import DarkAssetService
from services.analysis.privacy_score import PrivacyScorer
from services.system.vault_secret_manager import VaultSecretManager
from services.neo4j.independence_check import IndependenceCheck

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("VERIFY_PHASE_169")

def verify_169():
    print("\n" + "="*60)
    print("       PHASE 169: SFO PRIVACY OBFUSCATION VERIFICATION")
    print("="*60 + "\n")

    # 1. Privacy Blocker (Black Hole Mode)
    print("[*] Testing PrivacyBlockerService...")
    blocker = PrivacyBlockerService()
    res = blocker.enforce_lockdown("SECURE-FO", "BLACK_HOLE")
    print(f"    Mode: {res['privacy_mode']} (Expected: BLACK_HOLE)")
    
    # 2. Dark Asset Service
    print("\n[*] Testing DarkAssetService...")
    dark = DarkAssetService()
    dark.register_dark_asset("Gold Bars", Decimal('500000'), "Safe-Z")
    print(f"    Dark Wealth: ${dark.get_total_dark_wealth():,.2f}")

    # 3. Privacy Scorer
    print("\n[*] Testing PrivacyScorer...")
    scorer = PrivacyScorer()
    score = scorer.calculate_privacy_score("SFO", False, False)
    print(f"    SFO Privacy Score: {score['privacy_score']} (Expected: 100.0)")

    # 4. Vault Manager
    print("\n[*] Testing VaultSecretManager...")
    vault = VaultSecretManager()
    print("    Vault initialized.")

    # 5. Independence Check (Neo4j)
    print("\n[*] Testing IndependenceCheck...")
    # Mocking driver for check
    graph = IndependenceCheck(None) 
    print("    Service initialized.")

    print("\n" + "="*60)
    print("               PHASE 169 VERIFICATION COMPLETE")
    print("="*60 + "\n")

if __name__ == "__main__":
    verify_169()
