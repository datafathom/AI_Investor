"""
Tests for Compliance Pydantic Models
Phase 7: Model Validation Tests
"""

import pytest
from datetime import datetime
from pydantic import ValidationError
from schemas.compliance import (
    ViolationSeverity,
    ComplianceRule,
    ComplianceViolation,
    ComplianceReport
)


class TestViolationSeverityEnum:
    """Tests for ViolationSeverity enum."""
    
    def test_violation_severity_enum(self):
        """Test violation severity enum values."""
        assert ViolationSeverity.LOW == "low"
        assert ViolationSeverity.MEDIUM == "medium"
        assert ViolationSeverity.HIGH == "high"
        assert ViolationSeverity.CRITICAL == "critical"


class TestComplianceRule:
    """Tests for ComplianceRule model."""
    
    def test_valid_compliance_rule(self):
        """Test valid compliance rule creation."""
        rule = ComplianceRule(
            rule_id='rule_1',
            regulation='SEC',
            rule_name='Pattern Day Trader Rule',
            description='PDT rule enforcement',
            rule_logic={'min_account_value': 25000}
        )
        assert rule.rule_id == 'rule_1'
        assert rule.regulation == 'SEC'
        assert 'min_account_value' in rule.rule_logic


class TestComplianceViolation:
    """Tests for ComplianceViolation model."""
    
    def test_valid_compliance_violation(self):
        """Test valid compliance violation creation."""
        violation = ComplianceViolation(
            violation_id='viol_1',
            rule_id='rule_1',
            user_id='user_1',
            severity=ViolationSeverity.HIGH,
            description='Account value below minimum',
            detected_date=datetime.now(),
            resolved_date=None,
            status='open'
        )
        assert violation.violation_id == 'viol_1'
        assert violation.severity == ViolationSeverity.HIGH
        assert violation.status == 'open'
    
    def test_compliance_violation_defaults(self):
        """Test compliance violation with default values."""
        violation = ComplianceViolation(
            violation_id='viol_1',
            rule_id='rule_1',
            user_id='user_1',
            severity=ViolationSeverity.LOW,
            description='Test violation',
            detected_date=datetime.now()
        )
        assert violation.status == 'open'
        assert violation.resolved_date is None


class TestComplianceReport:
    """Tests for ComplianceReport model."""
    
    def test_valid_compliance_report(self):
        """Test valid compliance report creation."""
        report = ComplianceReport(
            report_id='report_1',
            user_id='user_1',
            report_type='regulatory',
            period_start=datetime(2024, 1, 1),
            period_end=datetime(2024, 12, 31),
            violations=['viol_1', 'viol_2'],
            generated_date=datetime.now()
        )
        assert report.report_id == 'report_1'
        assert report.report_type == 'regulatory'
        assert len(report.violations) == 2
    
    def test_compliance_report_defaults(self):
        """Test compliance report with default values."""
        report = ComplianceReport(
            report_id='report_1',
            user_id='user_1',
            report_type='custom',
            period_start=datetime(2024, 1, 1),
            period_end=datetime(2024, 12, 31),
            generated_date=datetime.now()
        )
        assert len(report.violations) == 0
