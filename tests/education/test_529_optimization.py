import pytest
from services.education.plan_recommender import PlanRecommender529
from services.tax.state_conformity import StateConformityValidator

@pytest.fixture
def recommender():
    return PlanRecommender529()

@pytest.fixture
def validator():
    return StateConformityValidator()

def test_recommend_plan_in_state(recommender):
    # NY has tax and deduction
    result = recommender.recommend_plan("NY", True, True)
    assert result['recommended_plan'] == "NY_DEDUCTION_OPTIMIZED"

def test_recommend_plan_national(recommender):
    # FL has no income tax
    result = recommender.recommend_plan("FL", False, False)
    assert result['recommended_plan'] == "NATIONAL_FEES_OPTIMIZED"

def test_check_expense_conformity_ca(validator):
    # CA does NOT conform to K12 tuition deduction
    result = validator.check_expense_conformity("CA", "K12_TUITION")
    assert result['is_plan_conforming'] is False
    assert result['taxability'] == "STATE_TAXABLE_OR_PENALTY"

def test_check_expense_conformity_generic(validator):
    # Generic college expense always conforms
    result = validator.check_expense_conformity("TX", "COLLEGE")
    assert result['is_plan_conforming'] is True
