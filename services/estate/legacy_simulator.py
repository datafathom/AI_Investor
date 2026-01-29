import logging
from decimal import Decimal
from typing import Dict, List, Any

logger = logging.getLogger(__name__)

class LegacySimulator:
    """
    Simulates the long-term compounding benefits of Dynasty Trusts.
    Compares Dynasty Trust (Estate Tax Bypass) vs. Outright Inheritance.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(LegacySimulator, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, '_initialized') and self._initialized:
            return
        self._initialized = True
        logger.info("LegacySimulator initialized")

    def run_projection(
        self,
        initial_principal: Decimal,
        annual_growth: float,
        generations: int,
        estate_tax_rate: float = 0.40
    ) -> Dict[str, Any]:
        """
        Runs a comparative legacy projection.
        """
        logger.info(f"SIM_LOG: Projecting legacy for {generations} generations starting with {initial_principal}")
        
        # Simple projection logic
        dynasty_value = initial_principal * (Decimal('1') + Decimal(str(annual_growth))) ** (generations * 25)
        taxable_value = initial_principal
        
        for g in range(generations):
            taxable_value *= (Decimal('1') + Decimal(str(annual_growth))) ** 25
            taxable_value *= (Decimal('1') - Decimal(str(estate_tax_rate)))
            
        return {
            "dynasty_value": dynasty_value,
            "taxable_value": taxable_value,
            "tax_savings": dynasty_value - taxable_value
        }
