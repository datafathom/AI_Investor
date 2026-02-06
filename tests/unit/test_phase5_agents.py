"""
Unit Tests for Phase 5: The Volatility Engine
Tests for Options Pricing math and Physicist agents.
"""

import pytest
import math

from services.physicist.options_pricing_service import get_options_pricing_service
from agents.physicist import get_physicist_agents


class TestOptionsMath:
    """Tests for Black-Scholes and Greeks calculations."""

    def setup_method(self) -> None:
        self.service = get_options_pricing_service()

    def test_black_scholes_call_price(self) -> None:
        """Test Black-Scholes call price calculation."""
        # S=100, K=100, T=1, r=0.05, sigma=0.2
        # Standard result is ~10.45
        result = self.service.black_scholes(S=100, K=100, T=1, r=0.05, sigma=0.2, option_type="call")
        assert round(result["price"], 2) == 10.45

    def test_black_scholes_put_price(self) -> None:
        """Test Black-Scholes put price calculation."""
        # Standard result for same params is ~5.57
        result = self.service.black_scholes(S=100, K=100, T=1, r=0.05, sigma=0.2, option_type="put")
        assert round(result["price"], 2) == 5.57

    def test_delta_call(self) -> None:
        """Test call delta calculation."""
        # ATM call delta should be around 0.6
        result = self.service.black_scholes(S=100, K=100, T=1, r=0.05, sigma=0.2, option_type="call")
        assert 0.60 <= result["delta"] <= 0.65

    def test_implied_volatility(self) -> None:
        """Test IV inversion."""
        iv = self.service.calculate_implied_volatility(
            market_price=10.45,
            S=100,
            K=100,
            T=1,
            r=0.05,
            option_type="call"
        )
        assert 0.19 <= iv <= 0.21


class TestPhysicistAgents:
    """Tests for Physicist Department agents (5.1-5.6)."""

    def setup_method(self) -> None:
        self.agents = get_physicist_agents()

    def test_all_physicist_agents_registered(self) -> None:
        """Test that 5 agents are instantiated."""
        assert len(self.agents) == 5
        assert "physicist.theta.5.1" in self.agents
        assert "physicist.mapper.5.2" in self.agents
        assert "physicist.hedger.5.4" in self.agents
        assert "physicist.solver.5.5" in self.agents
        assert "physicist.watcher.5.6" in self.agents

    def test_theta_measurement(self) -> None:
        """Test theta collector measurement."""
        agent = self.agents["physicist.theta.5.1"]
        agent.start()

        event = {
            "type": "theta.measure",
            "positions": [
                {
                    "price": 100.0,
                    "strike": 100.0,
                    "expiry_years": 1.0,
                    "iv": 0.2,
                    "type": "call",
                    "quantity": 10
                }
            ]
        }

        result = agent.process_event(event)
        assert result["status"] == "measured"
        assert result["daily_theta"] < 0  # Theta is negative for long options

    def test_surface_mapping_latency(self) -> None:
        """Test volatility surface mapping SLA."""
        agent = self.agents["physicist.mapper.5.2"]
        agent.start()

        event = {
            "type": "surface.map",
            "strikes": [90, 100, 110],
            "expiries": [0.1, 0.5, 1.0],
            "iv_data": {}
        }

        result = agent.process_event(event)
        assert result["status"] == "mapped"
        assert result["under_50ms_sla"] is True

    def test_delta_hedging_signal(self) -> None:
        """Test delta hedging recommendation."""
        agent = self.agents["physicist.hedger.5.4"]
        agent.start()

        event = {
            "type": "delta.analyze",
            "positions": [
                {
                    "price": 100.0,
                    "strike": 100.0,
                    "expiry_years": 1.0,
                    "iv": 0.2,
                    "type": "call",
                    "quantity": 10  # ~600 delta
                }
            ],
            "stock_qty": 0.0,
            "threshold": 100.0
        }

        result = agent.process_event(event)
        assert result["status"] == "analyzed"
        assert result["needs_hedge"]  # Use truthiness instead of 'is True'
        assert result["recommendation"]["quantity"] < 0  # Should sell stock to hedge long calls
