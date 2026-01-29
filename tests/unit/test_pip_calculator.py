"""
Unit tests for PipCalculatorService.
"""
import pytest
from decimal import Decimal
from services.pip_calculator import PipCalculatorService
from config.currency_pairs import MAJOR_PAIRS

class TestPipCalculatorService:
    @pytest.fixture
    def calculator(self):
        return PipCalculatorService()

    def test_calculate_pips_standard_pair(self, calculator):
        # EUR/USD: 1.0950 -> 1.0952 = 2.0 pips
        result = calculator.calculate_pips(1.0950, 1.0952, "EUR/USD")
        assert result == 2.0

    def test_calculate_pips_jpy_pair(self, calculator):
        # USD/JPY: 149.50 -> 149.52 = 2.0 pips
        result = calculator.calculate_pips(149.50, 149.52, "USD/JPY")
        assert result == 2.0

    def test_calculate_pips_negative(self, calculator):
        # EUR/USD: 1.0952 -> 1.0950 = -2.0 pips
        result = calculator.calculate_pips(1.0952, 1.0950, "EUR/USD")
        assert result == -2.0

    def test_calculate_pipettes_standard(self, calculator):
        # EUR/USD: 1.09500 -> 1.09501 = 1 pipette (0.1 pip)
        result = calculator.calculate_pipettes(1.09500, 1.09501, "EUR/USD")
        assert result == 1.0
        
        # In pips, this should be 0.1
        pips = calculator.calculate_pips(1.09500, 1.09501, "EUR/USD")
        assert pips == 0.1

    def test_major_pairs_config_check(self, calculator):
        # Ensure all major pairs calculate without error
        for pair in MAJOR_PAIRS:
            calculator.calculate_pips(1.0, 1.1, pair)

    def test_string_input_handling(self, calculator):
        # Ensure string inputs work to avoid float precision issues
        result = calculator.calculate_pips("1.26956", "1.27056", "GBP/USD")
        assert result == 10.0

    def test_GBP_USD_Benchmark(self, calculator):
        # From requirement: 1.26956 to 1.27056 = 10.0 pips
        result = calculator.calculate_pips(1.26956, 1.27056, "GBP/USD")
        assert result == 10.0
