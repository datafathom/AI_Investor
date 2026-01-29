import pytest
from services.quantitative.sharpe_grader import SharpeGrader

def test_sharpe_grading():
    svc = SharpeGrader()
    assert svc.grade_performance(3.5) == "EXCEPTIONAL"
    assert svc.grade_performance(1.5) == "GOOD"
    assert svc.grade_performance(-0.5) == "POOR"

def test_grading_colors():
    svc = SharpeGrader()
    assert svc.get_color_code("EXCEPTIONAL") == "#0000FF"
    assert svc.get_color_code("POOR") == "#FF0000"
