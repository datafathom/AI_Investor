"""
==============================================================================
FILE: services/retirement/withdrawal_strategy_service.py
ROLE: Withdrawal Strategy Optimizer
PURPOSE: Optimizes retirement withdrawal strategies with tax-efficient
         sequencing, RMD calculations, and withdrawal rate optimization.

INTEGRATION POINTS:
    - RetirementProjectionService: Retirement projections
    - TaxOptimizationService: Tax-efficient withdrawal sequencing
    - AccountService: Account balances and types
    - WithdrawalAPI: Withdrawal strategy endpoints
    - FrontendRetirement: Withdrawal planning dashboard

FEATURES:
    - Tax-efficient withdrawal sequencing
    - RMD calculations
    - Multiple withdrawal strategies
    - Withdrawal rate optimization

AUTHOR: AI Investor Team
CREATED: 2026-01-21
LAST_MODIFIED: 2026-01-21
==============================================================================
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from models.retirement import (
    WithdrawalPlan, WithdrawalStrategy, RMDCalculation
)
from services.tax.tax_optimization_service import get_tax_optimization_service
from services.system.cache_service import get_cache_service

logger = logging.getLogger(__name__)


class WithdrawalStrategyService:
    """
    Service for retirement withdrawal strategy optimization.
    """
    
    def __init__(self):
        """Initialize service with dependencies."""
        self.tax_optimization_service = get_tax_optimization_service()
        self.cache_service = get_cache_service()
        
    async def create_withdrawal_plan(
        self,
        user_id: str,
        strategy: str,
        initial_withdrawal_amount: float,
        withdrawal_rate: Optional[float] = None,
        inflation_adjustment: bool = True
    ) -> WithdrawalPlan:
        """
        Create optimized withdrawal plan.
        
        Args:
            user_id: User identifier
            strategy: Withdrawal strategy type
            initial_withdrawal_amount: Initial annual withdrawal
            withdrawal_rate: Optional withdrawal rate (if None, calculated)
            inflation_adjustment: Whether to adjust for inflation
            
        Returns:
            WithdrawalPlan with optimized strategy
        """
        logger.info(f"Creating withdrawal plan for user {user_id}")
        
        # Get account balances
        accounts = await self._get_account_balances(user_id)
        
        # Optimize account withdrawal sequence
        account_sequence = await self._optimize_account_sequence(accounts)
        
        # Calculate RMDs if applicable
        rmd_calculations = await self._calculate_rmds(user_id, accounts)
        
        plan = WithdrawalPlan(
            plan_id=f"withdrawal_{user_id}_{datetime.utcnow().timestamp()}",
            strategy=WithdrawalStrategy(strategy),
            initial_withdrawal_amount=initial_withdrawal_amount,
            withdrawal_rate=withdrawal_rate or (initial_withdrawal_amount / sum(a.get('balance', 0) for a in accounts.values())),
            inflation_adjustment=inflation_adjustment,
            account_sequence=account_sequence,
            rmd_calculations=rmd_calculations
        )
        
        # Cache plan
        cache_key = f"withdrawal_plan:{user_id}"
        self.cache_service.set(cache_key, plan.dict(), ttl=86400)
        
        return plan
    
    async def calculate_rmd(
        self,
        account_type: str,
        account_balance: float,
        age: int
    ) -> RMDCalculation:
        """
        Calculate Required Minimum Distribution.
        
        Args:
            account_type: Account type (IRA, 401k, etc.)
            account_balance: Account balance as of Dec 31 of prior year
            age: Age as of Dec 31 of current year
            
        Returns:
            RMDCalculation with RMD amount
        """
        logger.info(f"Calculating RMD for {account_type} account, age {age}")
        
        # Get life expectancy factor from IRS table
        life_expectancy = self._get_life_expectancy_factor(age)
        
        # RMD = Balance / Life Expectancy Factor
        rmd_amount = account_balance / life_expectancy
        
        # RMD must be taken by Dec 31
        distribution_date = datetime(datetime.now().year, 12, 31)
        
        return RMDCalculation(
            account_type=account_type,
            account_balance=account_balance,
            age=age,
            rmd_amount=rmd_amount,
            distribution_date=distribution_date
        )
    
    async def optimize_withdrawal_rate(
        self,
        retirement_savings: float,
        annual_expenses: float,
        years_in_retirement: int,
        expected_return: float = 0.06
    ) -> Dict:
        """
        Optimize withdrawal rate for retirement.
        
        Args:
            retirement_savings: Total retirement savings
            annual_expenses: Annual expenses in retirement
            years_in_retirement: Expected years in retirement
            expected_return: Expected annual return
            
        Returns:
            Optimization results with recommended withdrawal rate
        """
        logger.info("Optimizing withdrawal rate")
        
        # Calculate sustainable withdrawal rate using 4% rule as baseline
        baseline_rate = 0.04
        
        # Adjust based on years in retirement
        if years_in_retirement > 30:
            adjusted_rate = 0.035  # Lower for longer retirements
        elif years_in_retirement < 20:
            adjusted_rate = 0.045  # Higher for shorter retirements
        else:
            adjusted_rate = baseline_rate
        
        # Calculate if current savings can support expenses
        required_savings = annual_expenses / adjusted_rate
        sufficient = retirement_savings >= required_savings
        
        return {
            'recommended_withdrawal_rate': adjusted_rate,
            'recommended_annual_withdrawal': retirement_savings * adjusted_rate,
            'required_savings': required_savings,
            'current_savings': retirement_savings,
            'sufficient': sufficient,
            'shortfall': max(0, required_savings - retirement_savings) if not sufficient else 0
        }
    
    async def _optimize_account_sequence(
        self,
        accounts: Dict[str, Dict]
    ) -> List[str]:
        """Optimize account withdrawal sequence for tax efficiency."""
        # Use tax optimization service
        total_withdrawal = sum(a.get('balance', 0) for a in accounts.values())
        account_types = list(accounts.keys())
        
        result = await self.tax_optimization_service.optimize_withdrawal_sequence(
            portfolio_id="retirement",  # Simplified
            withdrawal_amount=total_withdrawal,
            account_types=account_types
        )
        
        return [s['account_type'] for s in result.get('sequence', [])]
    
    async def _calculate_rmds(
        self,
        user_id: str,
        accounts: Dict[str, Dict]
    ) -> Optional[Dict]:
        """Calculate RMDs for all applicable accounts."""
        rmds = {}
        
        for account_type, account_data in accounts.items():
            if account_type in ['ira', '401k', '403b']:
                balance = account_data.get('balance', 0)
                age = account_data.get('age', 72)  # Default RMD age
                
                if age >= 72:  # RMD age
                    rmd = await self.calculate_rmd(account_type, balance, age)
                    rmds[account_type] = rmd.dict()
        
        return rmds if rmds else None
    
    async def _get_account_balances(self, user_id: str) -> Dict[str, Dict]:
        """Get account balances by type."""
        # In production, fetch from account service
        return {
            'taxable': {'balance': 200000.0, 'age': 65},
            'ira': {'balance': 500000.0, 'age': 72},
            '401k': {'balance': 300000.0, 'age': 65},
            'tax_free': {'balance': 100000.0, 'age': 65}
        }
    
    def _get_life_expectancy_factor(self, age: int) -> float:
        """Get IRS life expectancy factor (simplified Uniform Lifetime Table)."""
        # Simplified table - in production, use full IRS tables
        factors = {
            72: 27.4,
            73: 26.5,
            74: 25.5,
            75: 24.6,
            76: 23.7,
            77: 22.9,
            78: 22.0,
            79: 21.1,
            80: 20.2
        }
        
        if age in factors:
            return factors[age]
        elif age < 72:
            return 27.4  # Use 72 factor for ages < 72
        else:
            # Linear interpolation for ages > 80
            return max(1.0, 20.2 - (age - 80) * 0.5)


# Singleton instance
_withdrawal_strategy_service: Optional[WithdrawalStrategyService] = None


def get_withdrawal_strategy_service() -> WithdrawalStrategyService:
    """Get singleton withdrawal strategy service instance."""
    global _withdrawal_strategy_service
    if _withdrawal_strategy_service is None:
        _withdrawal_strategy_service = WithdrawalStrategyService()
    return _withdrawal_strategy_service
