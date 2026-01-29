import unittest
from decimal import Decimal
from services.economics.clew_index_svc import CLEWIndexService
from services.planning.lifestyle_burn_svc import LifestyleBurnService
from services.estate.dilution_tracker_svc import DilutionTrackerService

class TestLifestyleEconomics(unittest.TestCase):

    def setUp(self):
        self.clew_svc = CLEWIndexService()
        self.burn_svc = LifestyleBurnService()
        self.dilution_svc = DilutionTrackerService()

    def test_clew_index_calculation(self):
        """Test the UHNW personal inflation calculation."""
        basket = [
            {"category": "Tuition", "weight_pct": 0.25, "annual_inflation_rate": 0.07},
            {"category": "Staff", "weight_pct": 0.15, "annual_inflation_rate": 0.04}, # Wages sticky but rising
            {"category": "Aviation", "weight_pct": 0.10, "annual_inflation_rate": 0.03}, # Fuel variance
            {"category": "Health", "weight_pct": 0.20, "annual_inflation_rate": 0.06}, # Concierge
            {"category": "General", "weight_pct": 0.30, "annual_inflation_rate": 0.03}  # CPI
        ]
        
        result = self.clew_svc.calculate_personal_inflation(basket)
        
        # Expected: (0.25*0.07) + (0.15*0.04) + (0.10*0.03) + (0.20*0.06) + (0.30*0.03)
        # = 0.0175 + 0.006 + 0.003 + 0.012 + 0.009 = 0.0475 (4.75%)
        
        self.assertEqual(result["clew_index_rate"], Decimal('0.0475'))
        self.assertTrue(result["is_above_cpi"])
        self.assertEqual(result["basket_items_count"], 5)

    def test_lifestyle_burn_projection(self):
        """Test projecting future costs using CLEW."""
        current_spend = Decimal('1000000') # $1M/year
        clew_rate = Decimal('0.05') # 5% inflation
        years = 20
        
        result = self.burn_svc.project_burn_rate(current_spend, clew_rate, years)
        
        # 1M * (1.05^20) ~= 1M * 2.653 = 2.653M
        expected_future_spend = current_spend * ((Decimal('1') + clew_rate) ** years)
        
        self.assertAlmostEqual(result["future_spend_annual"], round(expected_future_spend, 2), places=1)
        # SWR check: 2.653M / 0.03 ~= 88.4M required corpus
        self.assertTrue(result["required_corpus_at_future_date"] > Decimal('80000000'))

    def test_generational_dilution(self):
        """Test wealth per capita dilution across generations."""
        initial_wealth = Decimal('100000000') # $100M
        heirs_per_generation = 3
        generations = 3 # Founder -> Children -> Grandchildren
        
        result = self.dilution_svc.calculate_generational_dilution(initial_wealth, heirs_per_generation, generations)
        
        # Gen 1 (1 person) -> Gen 2 (3 people) -> Gen 3 (9 people)
        # $100M / 9 = $11.11M per person
        
        expected_descendants = 9
        expected_per_capita = round(initial_wealth / Decimal(expected_descendants), 2)
        
        self.assertEqual(result["total_heirs_estimated"], expected_descendants)
        self.assertEqual(result["wealth_per_capita_future"], expected_per_capita)
        self.assertEqual(result["social_standing_status"], "MAINTAINING_CLASS") # > $10M

    def test_generational_dilution_failure(self):
        """Test when wealth drops below social class threshold."""
        initial_wealth = Decimal('50000000') # $50M
        heirs_per_generation = 4
        generations = 3 
        
        # Gen 3 = 16 people. 50M / 16 = ~3.125M < 10M
        result = self.dilution_svc.calculate_generational_dilution(initial_wealth, heirs_per_generation, generations)
        
        self.assertEqual(result["social_standing_status"], "CLASS_DROP_RISK")

if __name__ == '__main__':
    unittest.main()
