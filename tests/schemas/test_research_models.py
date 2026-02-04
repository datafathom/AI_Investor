"""
Tests for Research Pydantic Models
Phase 7: Model Validation Tests
"""

import pytest
from datetime import datetime
from pydantic import ValidationError
from schemas.research import (
    ReportType,
    ReportStatus,
    ResearchReport,
    ReportTemplate
)


class TestReportEnums:
    """Tests for report enums."""
    
    def test_report_type_enum(self):
        """Test report type enum values."""
        assert ReportType.PORTFOLIO_ANALYSIS == "portfolio_analysis"
        assert ReportType.COMPANY_RESEARCH == "company_research"
        assert ReportType.MARKET_OUTLOOK == "market_outlook"
        assert ReportType.TAX_REPORT == "tax_report"
    
    def test_report_status_enum(self):
        """Test report status enum values."""
        assert ReportStatus.PENDING == "pending"
        assert ReportStatus.GENERATING == "generating"
        assert ReportStatus.COMPLETED == "completed"
        assert ReportStatus.FAILED == "failed"


class TestResearchReport:
    """Tests for ResearchReport model."""
    
    def test_valid_research_report(self):
        """Test valid research report creation."""
        report = ResearchReport(
            report_id='report_1',
            user_id='user_1',
            report_type=ReportType.PORTFOLIO_ANALYSIS,
            title='Portfolio Analysis Report',
            content='Report content',
            sections=[],
            charts=[],
            data={},
            status=ReportStatus.COMPLETED,
            generated_date=datetime.now(),
            created_date=datetime.now(),
            updated_date=datetime.now()
        )
        assert report.report_id == 'report_1'
        assert report.report_type == ReportType.PORTFOLIO_ANALYSIS
        assert report.status == ReportStatus.COMPLETED
    
    def test_research_report_defaults(self):
        """Test research report with default values."""
        report = ResearchReport(
            report_id='report_1',
            user_id='user_1',
            report_type=ReportType.PORTFOLIO_ANALYSIS,
            title='Test Report',
            content='Test content',
            created_date=datetime.now(),
            updated_date=datetime.now()
        )
        assert report.status == ReportStatus.PENDING
        assert report.generated_date is None


class TestReportTemplate:
    """Tests for ReportTemplate model."""
    
    def test_valid_report_template(self):
        """Test valid report template creation."""
        template = ReportTemplate(
            template_id='template_1',
            template_name='Standard Portfolio Report',
            report_type=ReportType.PORTFOLIO_ANALYSIS,
            sections=[],
            default_settings={}
        )
        assert template.template_id == 'template_1'
        assert template.report_type == ReportType.PORTFOLIO_ANALYSIS
