import sys
import os
import logging
from decimal import Decimal

# Add project root to path and remove scripts to avoid neo4j shadowing
if os.path.dirname(__file__) in sys.path:
    sys.path.remove(os.path.dirname(__file__))
sys.path.append(os.getcwd())

from services.compliance.fatca_compliance_svc import FATCAComplianceService
from services.neo4j.residency_graph import ResidencyGraph
from services.kafka.crs_consumer import CRSConsumer
from services.risk.country_risk import CountryRiskService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("VERIFY_PHASE_183")

def verify_183():
    print("\n" + "="*60)
    print("       PHASE 183: FATCA & FBAR COMPLIANCE VERIFICATION")
    print("="*60 + "\n")

    # 1. FATCA Thresholds
    print("[*] Testing FATCAComplianceService Thresholds...")
    svc = FATCAComplianceService()
    res = svc.check_reporting_thresholds(Decimal('75000.00'))
    print(f"    Value: $75,000 -> FBAR: {res['requires_fbar_filing']}, FATCA: {res['requires_8938_filing']}")

    # 2. Secrecy Compromise Detector
    print("\n[*] Testing Secrecy Compromise Detector...")
    comp = svc.detect_secrecy_compromise("Switzerland", "Please provide a W-9 form for tax residency.")
    print(f"    Compromised: {comp['is_secrecy_compromised']} (triggers: {comp['compromise_triggers']})")

    # 3. Residency Graph (Neo4j)
    print("\n[*] Testing ResidencyGraph (Neo4j)...")
    rg = ResidencyGraph()
    map_res = rg.map_foreign_account("user_1", "acc_99", "CH")
    print(f"    Graph Status: {map_res['status']} for {map_res['account_id']}")

    # 4. CRS Consumer (Kafka)
    print("\n[*] Testing CRSConsumer (Kafka Simulator)...")
    crs = CRSConsumer()
    event = crs.simulate_stream()
    print(f"    Processed CRS: {event['country']} (Balance: {event['balance']}, Audit: {event['requires_audit']})")

    # 5. Jurisdiction Risk
    print("\n[*] Testing CountryRiskService (Secrecy Risk)...")
    crs_risk = CountryRiskService()
    risk = crs_risk.evaluate_country("KY")
    print(f"    Cayman Islands Risk: {risk['secrecy_risk']} secrecy")

    print("\n" + "="*60)
    print("               PHASE 183 VERIFICATION COMPLETE")
    print("="*60 + "\n")

if __name__ == "__main__":
    verify_183()
