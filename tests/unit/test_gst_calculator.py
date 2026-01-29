import pytest
from services.tax.gst_calculator import GSTCalculator

def test_gst_full_exemption():
    svc = GSTCalculator()
    # 10M corpus, 10M exemptionallocated -> 0 inclusion ratio
    assert svc.calculate_inclusion_ratio(10000000, 10000000) == 0.0

def test_gst_partial_exemption():
    svc = GSTCalculator()
    # 10M corpus, 5M exemption -> 0.5 inclusion ratio
    assert svc.calculate_inclusion_ratio(10000000, 5000000) == 0.5

def test_gst_tax_math():
    svc = GSTCalculator()
    # 100k distribution, 0.5 inclusion ratio, 40% rate -> 20k tax
    assert svc.calculate_gst_tax(100000, 0.5, 0.40) == 20000.0
