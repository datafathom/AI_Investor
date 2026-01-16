"""
==============================================================================
AI Investor - Monte Carlo Simulation Engine
==============================================================================
PURPOSE:
    Portfolio simulation engine using Monte Carlo methods. Generates 
    thousands of potential future scenarios to calculate risk metrics
    like VaR (Value at Risk) and CVaR (Conditional VaR / Expected Shortfall).

THEORY:
    Monte Carlo simulation runs many random trials based on historical
    or assumed return distributions to model portfolio uncertainty.
    Supports both normal and fat-tailed distributions for realistic
    tail risk modeling.

ACCEPTANCE CRITERIA:
    - 10,000-run simulation in < 5 seconds
    - VaR/CVaR calculations at multiple confidence levels
    - Support for customizable distribution parameters
==============================================================================
"""
from typing import Dict, List, Optional, Tuple, Union
from enum import Enum
from dataclasses import dataclass
import numpy as np
from numpy.typing import NDArray
import logging
import time

logger = logging.getLogger(__name__)


class DistributionType(Enum):
    """Supported probability distributions for returns."""
    NORMAL = "normal"
    STUDENT_T = "student_t"  # Fat-tailed
    LAPLACE = "laplace"      # Double exponential (peaked, fat tails)


@dataclass
class SimulationConfig:
    """Configuration for Monte Carlo simulation."""
    n_simulations: int = 10000
    n_days: int = 252  # Trading days in a year
    distribution: DistributionType = DistributionType.NORMAL
    df: float = 5.0  # Degrees of freedom for Student-t
    confidence_levels: Tuple[float, ...] = (0.95, 0.99)
    random_seed: Optional[int] = None


@dataclass
class RiskMetrics:
    """Container for calculated risk metrics."""
    var_95: float
    var_99: float
    cvar_95: float  # Expected Shortfall
    cvar_99: float
    max_drawdown: float
    expected_return: float
    volatility: float
    sharpe_ratio: float


class MonteCarloEngine:
    """
    Monte Carlo simulation engine for portfolio risk analysis.
    
    Generates thousands of simulated return paths to calculate
    probabilistic risk metrics and stress test portfolio strategies.
    
    Attributes:
        config (SimulationConfig): Simulation parameters.
        last_simulations (Optional[NDArray]): Cached simulation results.
        last_metrics (Optional[RiskMetrics]): Cached risk metrics.
    """
    
    def __init__(self, config: Optional[SimulationConfig] = None) -> None:
        """
        Initialize the Monte Carlo engine.
        
        Args:
            config: Simulation configuration. Uses defaults if not provided.
        """
        self.config = config or SimulationConfig()
        self.last_simulations: Optional[NDArray] = None
        self.last_metrics: Optional[RiskMetrics] = None
        self._rng = np.random.default_rng(self.config.random_seed)
        
        logger.info(f"MonteCarloEngine initialized: {self.config.n_simulations} runs, "
                    f"{self.config.distribution.value} distribution")
    
    def _generate_returns(
        self,
        mean: float,
        std: float,
        shape: Tuple[int, ...]
    ) -> NDArray:
        """
        Generate random returns based on configured distribution.
        
        Args:
            mean: Mean daily return (e.g., 0.0005 for 0.05%).
            std: Daily standard deviation (e.g., 0.02 for 2%).
            shape: Shape of output array (n_simulations, n_days).
            
        Returns:
            Array of simulated daily returns.
        """
        if self.config.distribution == DistributionType.NORMAL:
            returns = self._rng.normal(mean, std, shape)
            
        elif self.config.distribution == DistributionType.STUDENT_T:
            # Student-t has fatter tails
            df = self.config.df
            returns = self._rng.standard_t(df, shape)
            # Scale to match mean and std
            returns = mean + returns * std * np.sqrt((df - 2) / df)
            
        elif self.config.distribution == DistributionType.LAPLACE:
            # Laplace (double exponential) - peaked with fat tails
            scale = std / np.sqrt(2)  # Match variance
            returns = self._rng.laplace(mean, scale, shape)
            
        else:
            returns = self._rng.normal(mean, std, shape)
        
        return returns
    
    def simulate_paths(
        self,
        initial_value: float,
        mean_return: float,
        volatility: float,
        n_simulations: Optional[int] = None,
        n_days: Optional[int] = None
    ) -> NDArray:
        """
        Generate simulated portfolio value paths.
        
        Args:
            initial_value: Starting portfolio value.
            mean_return: Expected daily return.
            volatility: Daily volatility (standard deviation).
            n_simulations: Override number of simulations.
            n_days: Override number of days.
            
        Returns:
            Array of shape (n_simulations, n_days+1) with portfolio values.
        """
        n_sims = n_simulations or self.config.n_simulations
        n_d = n_days or self.config.n_days
        
        start_time = time.perf_counter()
        
        # Generate daily returns
        returns = self._generate_returns(
            mean_return,
            volatility,
            shape=(n_sims, n_d)
        )
        
        # Convert to price paths using cumulative product
        # Start with initial value
        price_factors = 1 + returns
        cumulative = np.cumprod(price_factors, axis=1)
        
        # Add initial value column
        paths = np.zeros((n_sims, n_d + 1))
        paths[:, 0] = initial_value
        paths[:, 1:] = initial_value * cumulative
        
        self.last_simulations = paths
        
        elapsed = time.perf_counter() - start_time
        logger.info(f"Generated {n_sims} simulations x {n_d} days in {elapsed:.3f}s")
        
        return paths
    
    def calculate_var(
        self,
        paths: NDArray,
        confidence_level: float = 0.95
    ) -> float:
        """
        Calculate Value at Risk (VaR) from simulation paths.
        
        VaR represents the maximum expected loss at a given confidence level.
        
        Args:
            paths: Simulated portfolio value paths.
            confidence_level: Confidence level (e.g., 0.95 for 95%).
            
        Returns:
            VaR as a percentage loss (positive number).
        """
        # Calculate total returns for each simulation
        final_values = paths[:, -1]
        initial_value = paths[:, 0].mean()
        
        returns = (final_values - initial_value) / initial_value
        
        # VaR is the quantile at (1 - confidence_level)
        var = -np.percentile(returns, (1 - confidence_level) * 100)
        
        return float(var)
    
    def calculate_cvar(
        self,
        paths: NDArray,
        confidence_level: float = 0.95
    ) -> float:
        """
        Calculate Conditional VaR (CVaR / Expected Shortfall).
        
        CVaR is the expected loss given that loss exceeds VaR.
        More sensitive to tail risk than VaR.
        
        Args:
            paths: Simulated portfolio value paths.
            confidence_level: Confidence level.
            
        Returns:
            CVaR as a percentage loss (positive number).
        """
        final_values = paths[:, -1]
        initial_value = paths[:, 0].mean()
        
        returns = (final_values - initial_value) / initial_value
        
        # Find threshold (VaR)
        var_threshold = np.percentile(returns, (1 - confidence_level) * 100)
        
        # CVaR is mean of returns below VaR threshold
        tail_returns = returns[returns <= var_threshold]
        
        if len(tail_returns) == 0:
            return self.calculate_var(paths, confidence_level)
        
        cvar = -tail_returns.mean()
        
        return float(cvar)
    
    def calculate_max_drawdown(self, paths: NDArray) -> float:
        """
        Calculate maximum drawdown across all simulations.
        
        Args:
            paths: Simulated portfolio value paths.
            
        Returns:
            Maximum drawdown as a percentage (positive number).
        """
        # Calculate running maximum for each path
        running_max = np.maximum.accumulate(paths, axis=1)
        
        # Drawdown at each point
        drawdowns = (running_max - paths) / running_max
        
        # Maximum drawdown across all paths
        max_dd = np.max(drawdowns)
        
        return float(max_dd)
    
    def calculate_risk_metrics(
        self,
        paths: Optional[NDArray] = None
    ) -> RiskMetrics:
        """
        Calculate comprehensive risk metrics from simulation paths.
        
        Args:
            paths: Simulated paths. Uses cached if not provided.
            
        Returns:
            RiskMetrics dataclass with all calculated metrics.
        """
        if paths is None:
            paths = self.last_simulations
        
        if paths is None:
            raise ValueError("No simulation paths available. Run simulate_paths first.")
        
        # Calculate returns
        final_values = paths[:, -1]
        initial_value = paths[:, 0].mean()
        total_returns = (final_values - initial_value) / initial_value
        
        metrics = RiskMetrics(
            var_95=self.calculate_var(paths, 0.95),
            var_99=self.calculate_var(paths, 0.99),
            cvar_95=self.calculate_cvar(paths, 0.95),
            cvar_99=self.calculate_cvar(paths, 0.99),
            max_drawdown=self.calculate_max_drawdown(paths),
            expected_return=float(total_returns.mean()),
            volatility=float(total_returns.std()),
            sharpe_ratio=self._calculate_sharpe(total_returns)
        )
        
        self.last_metrics = metrics
        
        logger.info(f"Risk metrics: VaR95={metrics.var_95:.2%}, "
                    f"CVaR95={metrics.cvar_95:.2%}, MaxDD={metrics.max_drawdown:.2%}")
        
        return metrics
    
    def _calculate_sharpe(
        self,
        returns: NDArray,
        risk_free_rate: float = 0.02
    ) -> float:
        """Calculate annualized Sharpe ratio."""
        if returns.std() == 0:
            return 0.0
        
        excess_return = returns.mean() - risk_free_rate
        sharpe = excess_return / returns.std()
        
        return float(sharpe)
    
    def run_simulation(
        self,
        initial_value: float = 100000,
        mean_annual_return: float = 0.08,
        annual_volatility: float = 0.20
    ) -> Dict:
        """
        Convenience method: Full simulation pipeline.
        
        Args:
            initial_value: Starting portfolio value.
            mean_annual_return: Expected annual return (e.g., 0.08 for 8%).
            annual_volatility: Annual volatility (e.g., 0.20 for 20%).
            
        Returns:
            Dictionary with paths, metrics, and timing information.
        """
        # Convert annual to daily
        trading_days = self.config.n_days
        daily_return = mean_annual_return / trading_days
        daily_vol = annual_volatility / np.sqrt(trading_days)
        
        start_time = time.perf_counter()
        
        paths = self.simulate_paths(
            initial_value=initial_value,
            mean_return=daily_return,
            volatility=daily_vol
        )
        
        metrics = self.calculate_risk_metrics(paths)
        
        total_time = time.perf_counter() - start_time
        
        return {
            'paths': paths,
            'metrics': metrics,
            'n_simulations': self.config.n_simulations,
            'n_days': self.config.n_days,
            'distribution': self.config.distribution.value,
            'execution_time_seconds': total_time,
            'meets_performance_target': total_time < 5.0
        }
    
    def stress_test(
        self,
        initial_value: float = 100000,
        scenarios: Optional[List[Dict]] = None
    ) -> List[Dict]:
        """
        Run stress test scenarios.
        
        Args:
            initial_value: Starting portfolio value.
            scenarios: List of scenario configs with name, return, volatility.
            
        Returns:
            List of results for each scenario.
        """
        if scenarios is None:
            scenarios = [
                {'name': 'Normal Market', 'return': 0.08, 'volatility': 0.15},
                {'name': 'High Volatility', 'return': 0.04, 'volatility': 0.35},
                {'name': 'Bear Market', 'return': -0.15, 'volatility': 0.40},
                {'name': 'Black Swan', 'return': -0.30, 'volatility': 0.60},
            ]
        
        results = []
        for scenario in scenarios:
            result = self.run_simulation(
                initial_value=initial_value,
                mean_annual_return=scenario['return'],
                annual_volatility=scenario['volatility']
            )
            result['scenario_name'] = scenario['name']
            results.append(result)
            
            logger.info(f"Stress test '{scenario['name']}': "
                        f"VaR95={result['metrics'].var_95:.2%}")
        
        return results
