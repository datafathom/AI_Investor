import logging
import json
import os
import base64
from datetime import datetime, timezone
from typing import Dict, List, Any
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

logger = logging.getLogger(__name__)

class AlphaReportingService:
    """
    Generates End-of-Day (EOD) reports on agent performance.
    Identifies Alpha (Excess Return) and Attribution.
    Reports are PGP-encrypted (simulated via Fernet + Fixed Key).
    """
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AlphaReportingService, cls).__new__(cls)
            cls._instance._init_encryption()
        return cls._instance

    def _init_encryption(self):
        """Initialize encryption key for secure reporting."""
        # In a real app, this would be a PGP key from a Vault.
        # For prototype, we derive a key from a 'Sovereign' secret.
        password = b"sovereign_os_master_pass"
        salt = b"missions_salt"
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password))
        self.fernet = Fernet(key)
        logger.info("AlphaReportingService encryption layer initialized.")

    def generate_eod_report(self, encrypt: bool = True) -> Dict[str, Any]:
        """
        Synthesizes performance data and secures it.
        """
        logger.info("Generating EOD Alpha Report...")
        
        # 1. Fetch performance data (Enhanced Mock)
        agent_performance = self._fetch_agent_performance()
        
        # 2. Calculate Sector ROI
        sector_roi = self._calculate_sector_roi(agent_performance)
        
        # 3. Identify Top/Bottom Performers
        ranking = sorted(agent_performance, key=lambda x: x['roi'], reverse=True)
        top_agent = ranking[0] if ranking else None
        bottom_agent = ranking[-1] if ranking else None
        
        raw_report = {
            "version": "1.1",
            "date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
            "total_pnl": sum(a['pnl'] for a in agent_performance),
            "sector_performance": sector_roi,
            "mvp_agent": top_agent,
            "laggard_agent": bottom_agent,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "status": "FINAL"
        }
        
        if encrypt:
            report_str = json.dumps(raw_report)
            encrypted_data = self.fernet.encrypt(report_str.encode())
            
            final_report = {
                "header": "SOVEREIGN_OS_SECURE_REPORT",
                "mode": "PGP_ENC_SIM",
                "payload": encrypted_data.decode(),
                "checksum": hashes.Hash(hashes.SHA256()).update(encrypted_data).finalize().hex()
            }
            logger.info(f"Secure Report Generated. Checksum: {final_report['checksum'][:8]}")
            return final_report
            
        return raw_report

    def _fetch_agent_performance(self) -> List[Dict[str, Any]]:
        # Mocking real-time feed integration
        return [
            {"agent_id": "crypto_01", "sector": "Crypto", "pnl": 1500.0, "roi": 0.15},
            {"agent_id": "macro_01", "sector": "Macro", "pnl": -200.0, "roi": -0.02},
            {"agent_id": "tech_01", "sector": "Equities", "pnl": 800.0, "roi": 0.08},
            {"agent_id": "fixed_01", "sector": "Bonds", "pnl": 50.0, "roi": 0.005},
            {"agent_id": "intelligence_03", "sector": "Intelligence", "pnl": 120.0, "roi": 0.012}
        ]

    def _calculate_sector_roi(self, performance: List[Dict[str, Any]]) -> Dict[str, float]:
        sectors = {}
        for p in performance:
            sec = p['sector']
            if sec not in sectors: sectors[sec] = []
            sectors[sec].append(p['roi'])
            
        return {k: sum(v)/len(v) for k, v in sectors.items()}

# Singleton
alpha_reporting_service = AlphaReportingService()
def get_alpha_reporting_service() -> AlphaReportingService:
    return alpha_reporting_service
