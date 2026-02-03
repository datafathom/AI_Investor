"""
Compliance Service - Audit Logging & SAR Workflow
Phase 59: Manages audit trails, suspicious activity reporting (SAR),
and regulatory compliance monitoring.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional
import uuid
import logging

logger = logging.getLogger(__name__)

import hashlib
import json

@dataclass
class AuditLog:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    user_id: str = "demo-user"
    action: str = ""
    resource: str = ""
    status: str = "success"
    severity: str = "info"  # info, warning, critical
    details: Dict = field(default_factory=dict)
    prev_hash: str = ""
    hash: str = ""

    def calculate_hash(self) -> str:
        content = {
            "id": self.id,
            "timestamp": self.timestamp,
            "user_id": self.user_id,
            "action": self.action,
            "resource": self.resource,
            "status": self.status,
            "severity": self.severity,
            "details": self.details,
            "prev_hash": self.prev_hash
        }
        encoded = json.dumps(content, sort_keys=True).encode()
        return hashlib.sha256(encoded).hexdigest()

@dataclass
class SARAlert:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    type: str = "aml"  # aml, insider_trading, structuring, spoofing, layering
    status: str = "pending"  # pending, reviewed, filed
    severity: str = "medium"
    description: str = ""
    evidence_score: float = 0.0
    agent_id: Optional[str] = None

class ComplianceService:
    def __init__(self) -> None:
        self._audit_logs: List[AuditLog] = []
        self._sar_alerts: List[SARAlert] = []
        self._initialize_mock_data()
        logger.info("ComplianceService initialized")

    def _initialize_mock_data(self) -> None:
        """Add some sample data for the demo with a valid hash chain."""
        actions = [
            ("LOGIN", "AUTH_SERVICE", "info", {}),
            ("KYC_UPLOAD", "KYC_SERVICE", "info", {"doc_type": "passport"}),
            ("ORDER_EXECUTION", "TRADING_SERVICE", "warning", {"amount": 500000}),
            ("VAULT_ACCESS", "DOCUMENT_VAULT", "info", {}),
            ("SYSTEM_CONFIG_CHANGE", "ADMIN_PORTAL", "critical", {}),
        ]
        
        prev_hash = "0" * 64
        for action, resource, severity, details in actions:
            log = AuditLog(
                action=action, 
                resource=resource, 
                severity=severity, 
                details=details,
                prev_hash=prev_hash
            )
            log.hash = log.calculate_hash()
            self._audit_logs.append(log)
            prev_hash = log.hash
        
        import random
        alert_types = ["structuring", "insider_trading", "spoofing", "layering", "aml"]
        tickers = ["AAPL", "TSLA", "GME", "NVDA", "BTC"]
        
        for i in range(3):
            self._sar_alerts.append(SARAlert(
                type=random.choice(alert_types),
                description=f"Automated detection: {random.choice(['Abnormal volume', 'Pre-news spike', 'Rapid cancellation'])} in {random.choice(tickers)}",
                evidence_score=round(random.uniform(0.65, 0.98), 2),
                agent_id=f"Watcher-{i+1}"
            ))

    def get_audit_logs(self, limit: int = 100) -> List[AuditLog]:
        return self._audit_logs[-limit:]

    def add_audit_log(self, log_data: Dict) -> AuditLog:
        prev_hash = self._audit_logs[-1].hash if self._audit_logs else "0" * 64
        log = AuditLog(
            action=log_data.get("action", ""),
            resource=log_data.get("resource", ""),
            severity=log_data.get("severity", "info"),
            details=log_data.get("details", {}),
            prev_hash=prev_hash
        )
        log.hash = log.calculate_hash()
        self._audit_logs.append(log)
        
        if log.severity == "critical":
            logger.critical(f"CRITICAL AUDIT EVENT: {log.action} on {log.resource}")
        
        # Simple real-time abuse detection trigger
        if "order" in log.action.lower() and log.details.get("latency_ms", 100) < 10:
            self._trigger_abuse_alert(log)
            
        return log

    def _trigger_abuse_alert(self, log: AuditLog) -> None:
        alert = SARAlert(
            type="spoofing",
            description=f"Potential spoofing detected: {log.action} with {log.details.get('latency_ms')}ms latency",
            severity="high",
            evidence_score=0.9,
            agent_id=log.details.get("agent_id")
        )
        self._sar_alerts.append(alert)
        logger.warning(f"Abuse alert triggered: {alert.description}")

    def verify_log_integrity(self) -> Dict:
        """Validates the entire hash chain."""
        valid = True
        errors = []
        prev_hash = "0" * 64
        
        for i, log in enumerate(self._audit_logs):
            if log.prev_hash != prev_hash:
                valid = False
                errors.append(f"Chain broken at index {i}: expected prev_hash {prev_hash}, got {log.prev_hash}")
            
            actual_hash = log.calculate_hash()
            if log.hash != actual_hash:
                valid = False
                errors.append(f"Data tampered at index {i}: expected hash {actual_hash}, got {log.hash}")
            
            prev_hash = log.hash
            
        return {
            "is_valid": valid,
            "errors": errors,
            "log_count": len(self._audit_logs),
            "timestamp": datetime.now().isoformat()
        }

    def get_sar_alerts(self) -> List[SARAlert]:
        return self._sar_alerts

    def update_sar_status(self, sar_id: str, status: str) -> bool:
        for alert in self._sar_alerts:
            if alert.id == sar_id:
                alert.status = status
                logger.info(f"SAR {sar_id} status updated to {status}")
                return True
        return False

    def get_compliance_score(self) -> int:
        """Calculate a mock compliance score (0-100)."""
        pending = len([a for a in self._sar_alerts if a.status == "pending"])
        score = 100 - (pending * 5)
        return max(0, score)

# Singleton
_compliance_service: Optional[ComplianceService] = None

def get_compliance_service() -> ComplianceService:
    global _compliance_service
    if _compliance_service is None:
        _compliance_service = ComplianceService()
    return _compliance_service
