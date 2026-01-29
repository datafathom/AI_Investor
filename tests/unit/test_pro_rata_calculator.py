import pytest
from services.tax.pro_rata_calculator import ProRataCalculator

def test_pro_rata_partial_tax():
    calc = ProRataCalculator()
    # 7,000 conversion. 70,000 total balance. 7,000 basis (after-tax).
    # 7k / 70k = 10% tax free.
    # Tax free: 700. Taxable: 6,300.
    res = calc.calculate_taxable_portion(7000, 70000, 7000)
    assert res["tax_free_amount"] == 700.0
    assert res["taxable_amount"] == 6300.0
    assert res["ratio"] == 0.1

def test_pro_rata_clean_backdoor():
    calc = ProRataCalculator()
    # 7,000 conversion. 7,000 total. 7,000 basis.
    # 100% tax free.
    res = calc.calculate_taxable_portion(7000, 7000, 7000)
    assert res["taxable_amount"] == 0.0
    assert res["ratio"] == 1.0
