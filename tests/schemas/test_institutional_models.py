"""
Tests for Institutional Pydantic Models
Phase 7: Model Validation Tests
"""

import pytest
from datetime import datetime
from pydantic import ValidationError
from schemas.institutional import (
    Client,
    WhiteLabelConfig,
    ProfessionalReport
)


class TestClient:
    """Tests for Client model."""
    
    def test_valid_client(self):
        """Test valid client creation."""
        client = Client(
            client_id='client_1',
            advisor_id='advisor_1',
            client_name='John Doe',
            portfolio_ids=['portfolio_1', 'portfolio_2'],
            created_date=datetime.now(),
            updated_date=datetime.now()
        )
        assert client.client_id == 'client_1'
        assert client.advisor_id == 'advisor_1'
        assert len(client.portfolio_ids) == 2
    
    def test_client_defaults(self):
        """Test client with default values."""
        client = Client(
            client_id='client_1',
            advisor_id='advisor_1',
            client_name='Jane Smith',
            created_date=datetime.now(),
            updated_date=datetime.now()
        )
        assert len(client.portfolio_ids) == 0


class TestWhiteLabelConfig:
    """Tests for WhiteLabelConfig model."""
    
    def test_valid_white_label_config(self):
        """Test valid white label config creation."""
        config = WhiteLabelConfig(
            config_id='config_1',
            organization_id='org_1',
            logo_url='https://example.com/logo.png',
            primary_color='#000000',
            secondary_color='#FFFFFF',
            custom_domain='app.example.com',
            branding_name='Custom Brand',
            created_date=datetime.now(),
            updated_date=datetime.now()
        )
        assert config.config_id == 'config_1'
        assert config.logo_url == 'https://example.com/logo.png'
        assert config.primary_color == '#000000'
    
    def test_white_label_config_optional_fields(self):
        """Test white label config with optional fields."""
        config = WhiteLabelConfig(
            config_id='config_1',
            organization_id='org_1',
            created_date=datetime.now(),
            updated_date=datetime.now()
        )
        assert config.logo_url is None
        assert config.primary_color is None
        assert config.custom_domain is None


class TestProfessionalReport:
    """Tests for ProfessionalReport model."""
    
    def test_valid_professional_report(self):
        """Test valid professional report creation."""
        report = ProfessionalReport(
            report_id='report_1',
            advisor_id='advisor_1',
            client_id='client_1',
            report_type='performance',
            content={
                'total_return': 0.15,
                'sharpe_ratio': 1.5,
                'max_drawdown': 0.05
            },
            generated_date=datetime.now()
        )
        assert report.report_id == 'report_1'
        assert report.report_type == 'performance'
        assert 'total_return' in report.content
    
    def test_professional_report_defaults(self):
        """Test professional report with default values."""
        report = ProfessionalReport(
            report_id='report_1',
            advisor_id='advisor_1',
            client_id='client_1',
            report_type='custom',
            generated_date=datetime.now()
        )
        assert report.content == {}
