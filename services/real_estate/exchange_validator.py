
import logging
from decimal import Decimal
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class ExchangeValidator:
    """
    Validates IRS Section 1031 Like-Kind Exchange metrics.
    Ensures 'Equal or Greater Value' and 'Equal or Greater Equity' rules.
    """
    
    def validate_metrics(
        self,
        relinquished_value: Decimal,
        relinquished_equity: Decimal,
        relinquished_mortgage: Decimal,
        replacement_value: Decimal,
        replacement_equity: Decimal,
        replacement_mortgage: Decimal
    ) -> Dict[str, Any]:
        """
        Relinquished: Property being sold.
        Replacement: Property being bought.
        """
        logger.info(f"Validating 1031 Exchange: Relinquished(${relinquished_value}) -> Replacement(${replacement_value})")
        
        # Rule 1: Net Sales Price Rule
        value_gap = relinquished_value - replacement_value
        value_rule_met = replacement_value >= relinquished_value
        
        # Rule 2: Net Equity Rule (Invest all cash)
        equity_gap = relinquished_equity - replacement_equity
        equity_rule_met = replacement_equity >= relinquished_equity
        
        # Rule 3: Debt Rule (Mortgage must be equal or greater)
        mortgage_gap = relinquished_mortgage - replacement_mortgage
        mortgage_rule_met = replacement_mortgage >= relinquished_mortgage
        
        # Calculation of 'Boot' (Taxable portion)
        # Boot is the higher of Rule 1 or Rule 2/3 deficiencies
        boot = Decimal('0.00')
        if not value_rule_met:
            boot = max(boot, value_gap)
        if not equity_rule_met:
            boot = max(boot, equity_gap)
            
        logger.info(f"Exchange Result: ValueRule={value_rule_met}, EquityRule={equity_rule_met}, Boot=${boot}")
        
        return {
            "is_fully_deferred": value_rule_met and equity_rule_met,
            "boot_detected": boot > 0,
            "taxable_boot_amount": boot,
            "value_gap": value_gap,
            "equity_gap": equity_gap,
            "mortgage_gap": mortgage_gap
        }
