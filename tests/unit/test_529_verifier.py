import pytest
from services.compliance.expense_verifier import EducationExpenseVerifier

def test_qualified_tuition():
    svc = EducationExpenseVerifier()
    res = svc.verify_expense("TUITION", 10000)
    assert res["is_qualified"] == True

def test_room_board_status_check():
    svc = EducationExpenseVerifier()
    # Room & Board requires half-time
    res = svc.verify_expense("ROOM_BOARD", 5000, student_status="LESS_THAN_HALF")
    assert res["is_qualified"] == False
    assert "at least half-time" in res["verification_note"]

def test_non_qualified_luxury():
    svc = EducationExpenseVerifier()
    res = svc.verify_expense("LUXURY_CAR", 20000)
    assert res["is_qualified"] == False
