import pytest
from services.planning.plan_generator import PlanGenerator
from services.planning.complexity_analyzer import ComplexityAnalyzer
from uuid import uuid4

def test_plan_generation_auto():
    analyzer = ComplexityAnalyzer()
    generator = PlanGenerator(analyzer)
    plan = generator.generate_plan(uuid4(), {"net_worth": 1000000})
    assert plan.status == "COMPLETED"
    assert plan.requires_human_review == False

def test_plan_generation_review():
    analyzer = ComplexityAnalyzer()
    generator = PlanGenerator(analyzer)
    # 50M + Business -> Score 0.7 -> High complexity
    plan = generator.generate_plan(uuid4(), {"net_worth": 50000000, "has_business": True})
    assert plan.status == "REVIEW_REQUIRED"
    assert plan.requires_human_review == True
