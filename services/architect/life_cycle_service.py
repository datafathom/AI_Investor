"""
Life-Cycle Modeler Service
Phase 6 Implementation: The Financial Fortress

This service handles long-term financial projections, inflation adjustments,
and "Year of Financial Independence" calculations.

ACCEPTANCE CRITERIA from Phase_6_ImplementationPlan.md:
- 50-year projection with Inflation and Tax alpha.
- Updates in <1s after parameter changes.
"""

import logging
import time
import math
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)

@dataclass
class ProjectionResult:
    """Result of a life-cycle simulation."""
    years: List[int]
    net_worth: List[float]
    real_spending: List[float]
    fi_year: Optional[int]
    fi_age: Optional[int]
    success_rate: float
    execution_time_ms: float

class LifeCycleService:
    """
    Service for long-term wealth architectural modeling.
    """

    # Singleton pattern
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LifeCycleService, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        logger.info("LifeCycleService initialized")

    def run_simulation(
        self,
        current_nw: float,
        monthly_savings: float,
        monthly_burn: float,
        expected_return: float = 0.07,
        inflation: float = 0.03,
        horizon_years: int = 50,
        current_age: int = 30
    ) -> ProjectionResult:
        """
        Run a deterministic life-cycle simulation.
        
        AC: Projection updates instantly (<1s).
        """
        start_time = time.perf_counter()
        
        years = []
        nw_path = []
        burn_path = []
        fi_year = None
        fi_age = None
        
        running_nw = current_nw
        running_burn = monthly_burn * 12
        
        for y in range(horizon_years):
            year = datetime.now().year + y
            years.append(year)
            
            # 4% rule / SWR check for FI
            # If NW * 0.04 > annual burn, FI achieved
            if fi_year is None and running_nw * 0.04 >= running_burn:
                fi_year = year
                fi_age = current_age + y
                
            nw_path.append(running_nw)
            burn_path.append(running_burn)
            
            # Step forward
            investment_gain = running_nw * expected_return
            savings = monthly_savings * 12
            
            running_nw = running_nw + investment_gain + savings - running_burn
            running_burn *= (1 + inflation) # Inflation impact on spending
            
        elapsed_ms = (time.perf_counter() - start_time) * 1000
        
        return ProjectionResult(
            years=years,
            net_worth=nw_path,
            real_spending=burn_path,
            fi_year=fi_year,
            fi_age=fi_age,
            success_rate=100.0 if running_nw > 0 else 0.0,
            execution_time_ms=elapsed_ms
        )

# Singleton instance
lifecycle_service = LifeCycleService()

def get_lifecycle_service() -> LifeCycleService:
    return lifecycle_service
