import pytest
from services.retirement.db_to_dc_migration import DBDCMigrationCalculator

def test_migration_pension_preference():
    svc = DBDCMigrationCalculator()
    # Big pension (5k/mo), Low match (3%), High salary (100k), 10 yrs
    # DB Value: 5k*12*25 = 1.5M
    # Match Vol: 3k/yr * ~13 = ~39k
    res = svc.calculate_equivalence(5000, 0.03, 100000, 10)
    assert res["preference"] == "PENSION"

def test_migration_401k_preference():
    svc = DBDCMigrationCalculator()
    # Tiny pension (100/mo), huge match, long time
    res = svc.calculate_equivalence(100, 0.10, 200000, 30)
    assert res["preference"] == "MATCHING_401K"
