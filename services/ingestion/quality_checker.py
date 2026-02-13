import logging
from typing import List, Dict
from pydantic import BaseModel
from datetime import datetime

logger = logging.getLogger(__name__)

class QualityIssue(BaseModel):
    id: str
    type: str  # "missing_data", "outlier", "schema_violation"
    source: str
    severity: str  # "low", "medium", "critical"
    detected_at: datetime
    description: str
    status: str = "open"  # "open", "resolved", "ignored"

class QualityChecker:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(QualityChecker, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self.issues: List[QualityIssue] = []
        self._seed_issues()
        self._initialized = True

    def _seed_issues(self):
        # Mock some issues for the dashboard
        self.issues.append(QualityIssue(
            id="issue_1",
            type="missing_data",
            source="alpha_vantage_daily",
            severity="medium",
            detected_at=datetime.now(),
            description="Missing OHLCV data for AAPL on 2023-10-25"
        ))
        self.issues.append(QualityIssue(
            id="issue_2",
            type="schema_violation",
            source="sec_13f",
            severity="critical",
            detected_at=datetime.now(),
            description="Unexpected column 'cusip_old' in filing 0001"
        ))

    def get_summary(self) -> Dict:
        total = len(self.issues)
        open_issues = len([i for i in self.issues if i.status == "open"])
        score = max(0, 100 - (open_issues * 5))  # Simple mock scoring
        return {
            "score": score,
            "completeness_pct": 98.5,
            "accuracy_pct": 99.2,
            "freshness_hours": 1.2,
            "total_issues": total,
            "open_issues": open_issues
        }

    def list_issues(self) -> List[QualityIssue]:
        return self.issues

    def resolve_issue(self, issue_id: str):
        for issue in self.issues:
            if issue.id == issue_id:
                issue.status = "resolved"
                return True
        return False
