import pytest
from services.planning.expense_calculator import ExpenseCalculator

def test_expense_burn_calculation():
    calc = ExpenseCalculator()
    # 10 days of transactions, total $1000 spending
    transactions = [{"amount": 100} for _ in range(10)]
    burn = calc.calculate_monthly_burn(transactions)
    # 1000 in 10 days -> 3000 in 30 days
    assert burn == 3000.0

def test_annual_projection():
    calc = ExpenseCalculator()
    proj = calc.project_annual_expenses(3000.0, 0.0) # 0% inflation
    assert proj == 36000.0
