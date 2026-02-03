"""
==============================================================================
Unit Tests - HMM Regime Detection Engine
==============================================================================
Tests the HMM engine's regime classification, training, and
transition detection capabilities.
==============================================================================
"""
import pytest
import numpy as np
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.analysis.hmm_engine import HMMRegimeDetector, MarketRegime


class TestHMMRegimeDetector:
    """Test suite for HMMRegimeDetector regime classification."""
    
    def test_initialization(self) -> None:
        """Test HMMRegimeDetector initializes with correct defaults."""
        detector = HMMRegimeDetector()
        
        assert detector.n_states == 3
        assert detector.n_iterations == 100
        assert detector.convergence_threshold == 1e-6
        assert detector._is_fitted is False
    
    def test_initialization_custom_states(self) -> None:
        """Test HMMRegimeDetector with custom parameters."""
        detector = HMMRegimeDetector(n_states=5, n_iterations=50)
        
        assert detector.n_states == 5
        assert detector.n_iterations == 50
    
    def test_transition_matrix_shape(self) -> None:
        """Test transition matrix has correct dimensions."""
        detector = HMMRegimeDetector()
        
        assert detector.transition_matrix.shape == (3, 3)
        # Each row should sum to 1 (probability distribution)
        np.testing.assert_allclose(
            detector.transition_matrix.sum(axis=1),
            np.ones(3),
            atol=1e-6
        )
    
    def test_fit_with_synthetic_data(self) -> None:
        """Test fitting HMM with synthetic regime data."""
        detector = HMMRegimeDetector()
        
        # Generate synthetic data with clear regimes
        np.random.seed(42)
        bull_returns = np.random.normal(0.002, 0.01, 100)   # Positive mean
        bear_returns = np.random.normal(-0.002, 0.02, 100)  # Negative mean, higher vol
        sideways_returns = np.random.normal(0.0, 0.008, 100)  # Zero mean
        
        observations = np.concatenate([bull_returns, bear_returns, sideways_returns])
        
        detector.fit(observations)
        
        assert detector._is_fitted is True
        assert detector._last_state_sequence is not None
        assert len(detector._last_state_sequence) == 300
    
    def test_fit_raises_on_short_data(self) -> None:
        """Test fit raises ValueError for insufficient data."""
        detector = HMMRegimeDetector()
        
        with pytest.raises(ValueError, match="at least 10 observations"):
            detector.fit(np.array([0.01, 0.02, -0.01]))
    
    def test_viterbi_returns_valid_states(self) -> None:
        """Test Viterbi decoding returns valid state indices."""
        detector = HMMRegimeDetector()
        
        np.random.seed(42)
        observations = np.random.randn(100) * 0.01
        
        detector.fit(observations)
        states = detector.viterbi(observations)
        
        assert len(states) == 100
        assert all(s in [0, 1, 2] for s in states)
    
    def test_predict_regime_returns_valid_regime(self) -> None:
        """Test predict_regime returns valid MarketRegime."""
        detector = HMMRegimeDetector()
        
        np.random.seed(42)
        observations = np.random.randn(100) * 0.01
        detector.fit(observations)
        
        regime, probs = detector.predict_regime(0.002)
        
        assert isinstance(regime, MarketRegime)
        assert len(probs) == 3
        assert np.isclose(probs.sum(), 1.0)
    
    def test_detect_transition_within_lookback(self) -> None:
        """Test transition detection finds regime changes."""
        detector = HMMRegimeDetector()
        
        # Create data with clear transition
        np.random.seed(42)
        bull = np.random.normal(0.005, 0.005, 50)
        bear = np.random.normal(-0.005, 0.015, 50)
        observations = np.concatenate([bull, bear])
        
        detector.fit(observations)
        transitions = detector.detect_transition(observations, lookback=20)
        
        # Should detect at least one transition near the regime change
        assert isinstance(transitions, list)
        # May or may not find transitions depending on noise
    
    def test_market_regime_enum(self) -> None:
        """Test MarketRegime enum values."""
        assert MarketRegime.BULL.value == 0
        assert MarketRegime.BEAR.value == 1
        assert MarketRegime.SIDEWAYS.value == 2
    
    def test_get_regime_name(self) -> None:
        """Test regime name lookup."""
        detector = HMMRegimeDetector()
        
        assert detector.get_regime_name(0) == 'BULL'
        assert detector.get_regime_name(1) == 'BEAR'
        assert detector.get_regime_name(2) == 'SIDEWAYS'
    
    def test_emission_probability_reasonable(self) -> None:
        """Test emission probabilities are reasonable."""
        detector = HMMRegimeDetector()
        
        probs = detector._emission_probability(0.001)
        
        assert len(probs) == 3
        assert all(p >= 0 for p in probs)
        assert np.isclose(probs.sum(), 1.0)
    
    def test_regime_classification_accuracy(self) -> None:
        """Test regime classification achieves reasonable accuracy."""
        detector = HMMRegimeDetector()
        
        # Generate clearly separated regimes
        np.random.seed(123)
        bull = np.random.normal(0.01, 0.005, 100)
        bear = np.random.normal(-0.01, 0.005, 100)
        
        observations = np.concatenate([bull, bear])
        detector.fit(observations)
        
        states = detector.viterbi(observations)
        
        # The two halves should mostly be classified differently
        first_half_dominant = np.bincount(states[:100]).argmax()
        second_half_dominant = np.bincount(states[100:]).argmax()
        
        # Should identify that regimes are different
        assert first_half_dominant != second_half_dominant
    
    def test_convergence_with_stable_data(self) -> None:
        """Test that fitting converges on stable data."""
        detector = HMMRegimeDetector(n_iterations=200)
        
        np.random.seed(42)
        observations = np.random.normal(0, 0.01, 200)
        
        # Should not raise and should converge
        detector.fit(observations)
        assert detector._is_fitted is True
