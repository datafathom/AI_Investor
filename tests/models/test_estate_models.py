"""
Tests for Estate Pydantic Models
Phase 7: Model Validation Tests
"""

import pytest
from datetime import datetime
from pydantic import ValidationError
from schemas.estate import (
    BeneficiaryType,
    Beneficiary,
    EstatePlan,
    InheritanceProjection,
    EstateScenario
)


class TestBeneficiaryTypeEnum:
    """Tests for BeneficiaryType enum."""
    
    def test_beneficiary_type_enum(self):
        """Test beneficiary type enum values."""
        assert BeneficiaryType.SPOUSE == "spouse"
        assert BeneficiaryType.CHILD == "child"
        assert BeneficiaryType.TRUST == "trust"
        assert BeneficiaryType.CHARITY == "charity"


class TestBeneficiary:
    """Tests for Beneficiary model."""
    
    def test_valid_beneficiary(self):
        """Test valid beneficiary creation."""
        beneficiary = Beneficiary(
            beneficiary_id='ben_1',
            user_id='user_1',
            name='John Doe',
            relationship=BeneficiaryType.CHILD,
            allocation_percentage=50.0,
            allocation_amount=500000.0,
            tax_implications=None,
            created_date=datetime.now(),
            updated_date=datetime.now()
        )
        assert beneficiary.beneficiary_id == 'ben_1'
        assert beneficiary.allocation_percentage == 50.0
        assert beneficiary.relationship == BeneficiaryType.CHILD
    
    def test_beneficiary_allocation_percentage_validation(self):
        """Test beneficiary allocation percentage validation."""
        # Should fail if percentage > 100
        with pytest.raises(ValidationError):
            Beneficiary(
                beneficiary_id='ben_1',
                user_id='user_1',
                name='John Doe',
                relationship=BeneficiaryType.CHILD,
                allocation_percentage=150.0,
                created_date=datetime.now(),
                updated_date=datetime.now()
            )


class TestEstatePlan:
    """Tests for EstatePlan model."""
    
    def test_valid_estate_plan(self):
        """Test valid estate plan creation."""
        plan = EstatePlan(
            plan_id='plan_1',
            user_id='user_1',
            total_estate_value=1000000.0,
            beneficiaries=[],
            trust_accounts=[],
            tax_exempt_amount=12000000.0,
            estimated_estate_tax=0.0,
            created_date=datetime.now(),
            updated_date=datetime.now()
        )
        assert plan.plan_id == 'plan_1'
        assert plan.total_estate_value == 1000000.0
        assert plan.tax_exempt_amount == 12000000.0


class TestInheritanceProjection:
    """Tests for InheritanceProjection model."""
    
    def test_valid_inheritance_projection(self):
        """Test valid inheritance projection creation."""
        projection = InheritanceProjection(
            projection_id='proj_1',
            beneficiary_id='ben_1',
            projected_inheritance=500000.0,
            projected_tax_liability=0.0,
            after_tax_inheritance=500000.0,
            projected_date=datetime(2050, 1, 1),
            assumptions={}
        )
        assert projection.projection_id == 'proj_1'
        assert projection.projected_inheritance == 500000.0
        assert projection.after_tax_inheritance == 500000.0


class TestEstateScenario:
    """Tests for EstateScenario model."""
    
    def test_valid_estate_scenario(self):
        """Test valid estate scenario creation."""
        scenario = EstateScenario(
            scenario_name='Standard Estate',
            estate_value=1000000.0,
            beneficiaries=[],
            tax_strategies=['gifting', 'trust'],
            projection_years=10
        )
        assert scenario.scenario_name == 'Standard Estate'
        assert scenario.estate_value == 1000000.0
        assert len(scenario.tax_strategies) == 2
