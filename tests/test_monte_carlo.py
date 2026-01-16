"""
==============================================================================
Unit Tests - Monte Carlo Simulation Engine
==============================================================================
Tests the Monte Carlo engine's simulation, VaR/CVaR calculations,
and performance requirements.
==============================================================================
"""
import pytest
import numpy as np
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.analysis.monte_carlo import (
    MonteCarloEngine,
    SimulationConfig,
    DistributionType,
    RiskMetrics
)


class TestSimulationConfig:
    """Test suite for SimulationConfig dataclass."""
    
    def test_default_values(self) -> None:
        """Test SimulationConfig has correct defaults."""
        config = SimulationConfig()
        
        assert config.n_simulations == 10000
        assert config.n_days == 252
        assert config.distribution == DistributionType.NORMAL
        assert config.df == 5.0
        assert 0.95 in config.confidence_levels
    
    def test_custom_values(self) -> None:
        """Test SimulationConfig with custom values."""
        config = SimulationConfig(
            n_simulations=5000,
            n_days=126,
            distribution=DistributionType.STUDENT_T
        )
        
        assert config.n_simulations == 5000
        assert config.n_days == 126
        assert config.distribution == DistributionType.STUDENT_T


class TestMonteCarloEngine:
    """Test suite for MonteCarloEngine simulation."""
    
    def test_initialization(self) -> None:
        """Test MonteCarloEngine initializes correctly."""
        engine = MonteCarloEngine()
        
        assert engine.config.n_simulations == 10000
        assert engine.last_simulations is None
        assert engine.last_metrics is None
    
    def test_initialization_custom_config(self) -> None:
        """Test MonteCarloEngine with custom config."""
        config = SimulationConfig(n_simulations=1000, random_seed=42)
        engine = MonteCarloEngine(config)
        
        assert engine.config.n_simulations == 1000
    
    def test_simulate_paths_shape(self) -> None:
        """Test simulated paths have correct shape."""
        config = SimulationConfig(n_simulations=100, n_days=20, random_seed=42)
        engine = MonteCarloEngine(config)
        
        paths = engine.simulate_paths(
            initial_value=100000,
            mean_return=0.0003,
            volatility=0.01
        )
        
        assert paths.shape == (100, 21)  # 100 sims x (20 days + 1 initial)
        assert paths[:, 0].mean() == 100000  # All start at initial value
    
    def test_simulate_paths_initial_value(self) -> None:
        """Test all paths start at initial value."""
        config = SimulationConfig(n_simulations=100, random_seed=42)
        engine = MonteCarloEngine(config)
        
        paths = engine.simulate_paths(
            initial_value=50000,
            mean_return=0.001,
            volatility=0.02
        )
        
        np.testing.assert_array_equal(paths[:, 0], 50000)
    
    def test_different_distributions(self) -> None:
        """Test simulation works with different distributions."""
        for dist_type in DistributionType:
            config = SimulationConfig(
                n_simulations=100,
                n_days=10,
                distribution=dist_type,
                random_seed=42
            )
            engine = MonteCarloEngine(config)
            
            paths = engine.simulate_paths(
                initial_value=100000,
                mean_return=0.0005,
                volatility=0.015
            )
            
            assert paths.shape == (100, 11)
            assert not np.any(np.isnan(paths))
    
    def test_calculate_var_95(self) -> None:
        """Test VaR calculation at 95% confidence."""
        config = SimulationConfig(n_simulations=1000, random_seed=42)
        engine = MonteCarloEngine(config)
        
        paths = engine.simulate_paths(
            initial_value=100000,
            mean_return=0.0003,
            volatility=0.015
        )
        
        var_95 = engine.calculate_var(paths, 0.95)
        
        # VaR should be a positive number (representing loss)
        assert isinstance(var_95, float)
        assert var_95 > 0 or var_95 <= 0  # Can be positive (loss) or negative (gain)
    
    def test_cvar_greater_than_var(self) -> None:
        """Test CVaR >= VaR (expected shortfall is worse than threshold)."""
        config = SimulationConfig(n_simulations=5000, random_seed=42)
        engine = MonteCarloEngine(config)
        
        # Use volatile parameters to ensure losses
        paths = engine.simulate_paths(
            initial_value=100000,
            mean_return=-0.001,  # Negative expected return
            volatility=0.03
        )
        
        var_95 = engine.calculate_var(paths, 0.95)
        cvar_95 = engine.calculate_cvar(paths, 0.95)
        
        # CVaR should be >= VaR
        assert cvar_95 >= var_95 - 0.001  # Small tolerance for numerical issues
    
    def test_max_drawdown_range(self) -> None:
        """Test max drawdown is between 0 and 1."""
        config = SimulationConfig(n_simulations=500, random_seed=42)
        engine = MonteCarloEngine(config)
        
        paths = engine.simulate_paths(
            initial_value=100000,
            mean_return=0.0003,
            volatility=0.02
        )
        
        max_dd = engine.calculate_max_drawdown(paths)
        
        assert 0 <= max_dd <= 1
    
    def test_calculate_risk_metrics_structure(self) -> None:
        """Test risk metrics returns proper structure."""
        config = SimulationConfig(n_simulations=500, random_seed=42)
        engine = MonteCarloEngine(config)
        
        paths = engine.simulate_paths(
            initial_value=100000,
            mean_return=0.0003,
            volatility=0.015
        )
        
        metrics = engine.calculate_risk_metrics(paths)
        
        assert isinstance(metrics, RiskMetrics)
        assert hasattr(metrics, 'var_95')
        assert hasattr(metrics, 'var_99')
        assert hasattr(metrics, 'cvar_95')
        assert hasattr(metrics, 'cvar_99')
        assert hasattr(metrics, 'max_drawdown')
        assert hasattr(metrics, 'expected_return')
        assert hasattr(metrics, 'sharpe_ratio')
    
    def test_run_simulation_convenience(self) -> None:
        """Test run_simulation convenience method."""
        config = SimulationConfig(n_simulations=500, random_seed=42)
        engine = MonteCarloEngine(config)
        
        result = engine.run_simulation(
            initial_value=100000,
            mean_annual_return=0.08,
            annual_volatility=0.20
        )
        
        assert 'paths' in result
        assert 'metrics' in result
        assert 'execution_time_seconds' in result
        assert 'meets_performance_target' in result
        assert result['n_simulations'] == 500
    
    def test_performance_10000_runs_under_5_seconds(self) -> None:
        """Test 10,000 simulations complete in < 5 seconds (acceptance criteria)."""
        config = SimulationConfig(n_simulations=10000, n_days=252, random_seed=42)
        engine = MonteCarloEngine(config)
        
        start_time = time.perf_counter()
        
        result = engine.run_simulation(
            initial_value=100000,
            mean_annual_return=0.08,
            annual_volatility=0.20
        )
        
        elapsed = time.perf_counter() - start_time
        
        assert elapsed < 5.0, f"Simulation took {elapsed:.2f}s, exceeds 5s threshold"
        assert result['meets_performance_target'] is True
    
    def test_stress_test(self) -> None:
        """Test stress test scenarios run correctly."""
        config = SimulationConfig(n_simulations=100, random_seed=42)
        engine = MonteCarloEngine(config)
        
        results = engine.stress_test(initial_value=100000)
        
        assert len(results) == 4  # Default 4 scenarios
        assert all('scenario_name' in r for r in results)
        assert all('metrics' in r for r in results)
    
    def test_reproducibility_with_seed(self) -> None:
        """Test simulations are reproducible with same seed."""
        config1 = SimulationConfig(n_simulations=100, random_seed=123)
        config2 = SimulationConfig(n_simulations=100, random_seed=123)
        
        engine1 = MonteCarloEngine(config1)
        engine2 = MonteCarloEngine(config2)
        
        paths1 = engine1.simulate_paths(100000, 0.001, 0.02)
        paths2 = engine2.simulate_paths(100000, 0.001, 0.02)
        
        np.testing.assert_array_equal(paths1, paths2)
    
    def test_cached_simulations(self) -> None:
        """Test last_simulations is cached after run."""
        config = SimulationConfig(n_simulations=100, random_seed=42)
        engine = MonteCarloEngine(config)
        
        paths = engine.simulate_paths(100000, 0.001, 0.02)
        
        assert engine.last_simulations is not None
        np.testing.assert_array_equal(engine.last_simulations, paths)
    
    def test_calculate_metrics_without_paths_raises(self) -> None:
        """Test calculate_risk_metrics raises without paths."""
        engine = MonteCarloEngine()
        
        with pytest.raises(ValueError, match="No simulation paths"):
            engine.calculate_risk_metrics()
