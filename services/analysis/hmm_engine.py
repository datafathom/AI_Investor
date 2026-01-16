"""
==============================================================================
AI Investor - HMM Regime Detection Engine
==============================================================================
PURPOSE:
    Hidden Markov Model engine for market regime detection. Classifies market
    states (bull, bear, sideways) using observable returns data and detects
    state transitions for tactical allocation decisions.

THEORY:
    Markets exhibit regime-dependent behavior. HMM enables probabilistic
    inference of hidden states from observable data, supporting the
    "Complex Adaptive System" philosophy.

ACCEPTANCE CRITERIA:
    - > 70% backtested accuracy in regime classification
    - State transition detection within 2 data points
==============================================================================
"""
from typing import Dict, List, Optional, Tuple
from enum import Enum
import numpy as np
from numpy.typing import NDArray
import logging

logger = logging.getLogger(__name__)


class MarketRegime(Enum):
    """Enumeration of market regime states."""
    BULL = 0      # Uptrending, low volatility
    BEAR = 1      # Downtrending, high volatility
    SIDEWAYS = 2  # Range-bound, moderate volatility


class HMMRegimeDetector:
    """
    Hidden Markov Model for market regime detection.
    
    Uses a 3-state HMM with Gaussian emissions to classify market regimes
    based on observable return data.
    
    Attributes:
        n_states (int): Number of hidden states (default: 3).
        n_iterations (int): Max iterations for Baum-Welch training.
        convergence_threshold (float): Convergence criterion for training.
        transition_matrix (NDArray): State transition probability matrix.
        emission_means (NDArray): Mean of Gaussian emission for each state.
        emission_vars (NDArray): Variance of Gaussian emission for each state.
        initial_probs (NDArray): Initial state probability distribution.
    """
    
    def __init__(
        self, 
        n_states: int = 3,
        n_iterations: int = 100,
        convergence_threshold: float = 1e-6
    ) -> None:
        """
        Initialize the HMM Regime Detector.
        
        Args:
            n_states: Number of hidden states (default: 3 for bull/bear/sideways).
            n_iterations: Maximum Baum-Welch iterations.
            convergence_threshold: Threshold for convergence detection.
        """
        self.n_states = n_states
        self.n_iterations = n_iterations
        self.convergence_threshold = convergence_threshold
        
        # Initialize with reasonable priors for market regimes
        self.transition_matrix = self._init_transition_matrix()
        self.emission_means = np.array([0.001, -0.001, 0.0])  # Bull, Bear, Sideways
        self.emission_vars = np.array([0.0001, 0.0004, 0.0002])  # Low, High, Med vol
        self.initial_probs = np.ones(n_states) / n_states
        
        self._is_fitted = False
        self._last_state_sequence: Optional[NDArray] = None
        
        logger.info(f"HMMRegimeDetector initialized with {n_states} states")
    
    def _init_transition_matrix(self) -> NDArray:
        """
        Initialize transition matrix with regime persistence assumption.
        
        Markets tend to persist in regimes, so diagonal elements are higher.
        """
        # High self-transition probability (regime persistence)
        matrix = np.array([
            [0.95, 0.03, 0.02],  # Bull: likely stays bull
            [0.03, 0.94, 0.03],  # Bear: likely stays bear
            [0.04, 0.04, 0.92],  # Sideways: slightly less persistent
        ])
        return matrix
    
    def _gaussian_pdf(self, x: float, mean: float, var: float) -> float:
        """Calculate Gaussian probability density."""
        if var <= 0:
            var = 1e-10  # Prevent division by zero
        return np.exp(-0.5 * ((x - mean) ** 2) / var) / np.sqrt(2 * np.pi * var)
    
    def _emission_probability(self, observation: float) -> NDArray:
        """Calculate emission probabilities for all states given an observation."""
        probs = np.array([
            self._gaussian_pdf(observation, self.emission_means[i], self.emission_vars[i])
            for i in range(self.n_states)
        ])
        # Normalize to avoid numerical underflow
        total = probs.sum()
        if total > 0:
            probs /= total
        return probs
    
    def fit(self, observations: NDArray) -> 'HMMRegimeDetector':
        """
        Train the HMM using the Baum-Welch algorithm.
        
        Args:
            observations: 1D array of observable data (e.g., daily returns).
            
        Returns:
            Self for method chaining.
            
        Raises:
            ValueError: If observations array is too short.
        """
        if len(observations) < 10:
            raise ValueError("Need at least 10 observations for training")
        
        T = len(observations)
        
        # Initialize emission parameters from data statistics
        self._init_emissions_from_data(observations)
        
        prev_log_likelihood = float('-inf')
        
        for iteration in range(self.n_iterations):
            # E-step: Forward-backward algorithm
            alpha, scale_factors = self._forward(observations)
            beta = self._backward(observations, scale_factors)
            
            # Compute log-likelihood for convergence check
            log_likelihood = np.sum(np.log(scale_factors + 1e-10))
            
            # Check convergence
            if abs(log_likelihood - prev_log_likelihood) < self.convergence_threshold:
                logger.info(f"Converged at iteration {iteration}")
                break
            prev_log_likelihood = log_likelihood
            
            # M-step: Update parameters
            gamma = self._compute_gamma(alpha, beta)
            xi = self._compute_xi(observations, alpha, beta)
            
            self._update_parameters(observations, gamma, xi)
        
        self._is_fitted = True
        # Store the most likely state sequence
        self._last_state_sequence = self.viterbi(observations)
        
        logger.info(f"HMM fitted on {T} observations")
        return self
    
    def _init_emissions_from_data(self, observations: NDArray) -> None:
        """Initialize emission parameters from data quantiles."""
        sorted_obs = np.sort(observations)
        n = len(sorted_obs)
        
        # Split into 3 quantiles for initial means
        bull_region = sorted_obs[2*n//3:]   # Top third (high returns)
        bear_region = sorted_obs[:n//3]     # Bottom third (low returns)
        sideways_region = sorted_obs[n//3:2*n//3]  # Middle third
        
        self.emission_means = np.array([
            np.mean(bull_region),
            np.mean(bear_region),
            np.mean(sideways_region)
        ])
        
        self.emission_vars = np.array([
            max(np.var(bull_region), 1e-6),
            max(np.var(bear_region), 1e-6),
            max(np.var(sideways_region), 1e-6)
        ])
    
    def _forward(self, observations: NDArray) -> Tuple[NDArray, NDArray]:
        """Forward pass of the forward-backward algorithm with scaling."""
        T = len(observations)
        alpha = np.zeros((T, self.n_states))
        scale_factors = np.zeros(T)
        
        # Initialize
        emission_probs = self._emission_probability(observations[0])
        alpha[0] = self.initial_probs * emission_probs
        scale_factors[0] = alpha[0].sum()
        if scale_factors[0] > 0:
            alpha[0] /= scale_factors[0]
        
        # Recursion
        for t in range(1, T):
            emission_probs = self._emission_probability(observations[t])
            alpha[t] = (alpha[t-1] @ self.transition_matrix) * emission_probs
            scale_factors[t] = alpha[t].sum()
            if scale_factors[t] > 0:
                alpha[t] /= scale_factors[t]
        
        return alpha, scale_factors
    
    def _backward(self, observations: NDArray, scale_factors: NDArray) -> NDArray:
        """Backward pass of the forward-backward algorithm."""
        T = len(observations)
        beta = np.zeros((T, self.n_states))
        
        # Initialize
        beta[T-1] = 1.0
        
        # Recursion
        for t in range(T-2, -1, -1):
            emission_probs = self._emission_probability(observations[t+1])
            beta[t] = self.transition_matrix @ (emission_probs * beta[t+1])
            if scale_factors[t+1] > 0:
                beta[t] /= scale_factors[t+1]
        
        return beta
    
    def _compute_gamma(self, alpha: NDArray, beta: NDArray) -> NDArray:
        """Compute state occupation probabilities."""
        gamma = alpha * beta
        # Normalize each row
        row_sums = gamma.sum(axis=1, keepdims=True)
        row_sums[row_sums == 0] = 1  # Prevent division by zero
        gamma /= row_sums
        return gamma
    
    def _compute_xi(
        self, 
        observations: NDArray, 
        alpha: NDArray, 
        beta: NDArray
    ) -> NDArray:
        """Compute joint state transition probabilities."""
        T = len(observations)
        xi = np.zeros((T-1, self.n_states, self.n_states))
        
        for t in range(T-1):
            emission_probs = self._emission_probability(observations[t+1])
            numerator = np.outer(alpha[t], emission_probs * beta[t+1]) * self.transition_matrix
            denominator = numerator.sum()
            if denominator > 0:
                xi[t] = numerator / denominator
        
        return xi
    
    def _update_parameters(
        self, 
        observations: NDArray, 
        gamma: NDArray, 
        xi: NDArray
    ) -> None:
        """M-step: Update model parameters."""
        # Update initial probabilities
        self.initial_probs = gamma[0]
        
        # Update transition matrix
        for i in range(self.n_states):
            denominator = gamma[:-1, i].sum()
            if denominator > 0:
                for j in range(self.n_states):
                    self.transition_matrix[i, j] = xi[:, i, j].sum() / denominator
        
        # Normalize rows
        row_sums = self.transition_matrix.sum(axis=1, keepdims=True)
        row_sums[row_sums == 0] = 1
        self.transition_matrix /= row_sums
        
        # Update emission parameters
        for i in range(self.n_states):
            denominator = gamma[:, i].sum()
            if denominator > 0:
                self.emission_means[i] = (gamma[:, i] * observations).sum() / denominator
                diff = observations - self.emission_means[i]
                self.emission_vars[i] = max(
                    (gamma[:, i] * diff * diff).sum() / denominator,
                    1e-6
                )
    
    def viterbi(self, observations: NDArray) -> NDArray:
        """
        Find the most likely state sequence using the Viterbi algorithm.
        
        Args:
            observations: 1D array of observable data.
            
        Returns:
            Array of predicted state indices.
        """
        T = len(observations)
        delta = np.zeros((T, self.n_states))
        psi = np.zeros((T, self.n_states), dtype=int)
        
        # Initialize
        emission_probs = self._emission_probability(observations[0])
        delta[0] = np.log(self.initial_probs + 1e-10) + np.log(emission_probs + 1e-10)
        
        # Recursion
        log_trans = np.log(self.transition_matrix + 1e-10)
        for t in range(1, T):
            emission_probs = self._emission_probability(observations[t])
            for j in range(self.n_states):
                temp = delta[t-1] + log_trans[:, j]
                psi[t, j] = np.argmax(temp)
                delta[t, j] = temp[psi[t, j]] + np.log(emission_probs[j] + 1e-10)
        
        # Backtrack
        states = np.zeros(T, dtype=int)
        states[T-1] = np.argmax(delta[T-1])
        for t in range(T-2, -1, -1):
            states[t] = psi[t+1, states[t+1]]
        
        return states
    
    def predict_regime(self, observation: float) -> Tuple[MarketRegime, NDArray]:
        """
        Predict the current market regime for a single observation.
        
        Args:
            observation: Single data point (e.g., today's return).
            
        Returns:
            Tuple of (predicted regime, probability distribution).
        """
        emission_probs = self._emission_probability(observation)
        
        if self._last_state_sequence is not None and len(self._last_state_sequence) > 0:
            # Use last known state for prior
            last_state = self._last_state_sequence[-1]
            prior = self.transition_matrix[last_state]
        else:
            prior = self.initial_probs
        
        posterior = prior * emission_probs
        posterior /= posterior.sum()
        
        predicted_state = int(np.argmax(posterior))
        return MarketRegime(predicted_state), posterior
    
    def detect_transition(
        self, 
        observations: NDArray, 
        lookback: int = 5
    ) -> List[Dict]:
        """
        Detect regime transitions in recent observations.
        
        Args:
            observations: Array of recent observations.
            lookback: Number of recent points to analyze.
            
        Returns:
            List of detected transitions with timing and states.
        """
        if len(observations) < 2:
            return []
        
        states = self.viterbi(observations[-lookback:])
        transitions = []
        
        for i in range(1, len(states)):
            if states[i] != states[i-1]:
                transitions.append({
                    'position': i,
                    'points_ago': lookback - i,
                    'from_regime': MarketRegime(states[i-1]).name,
                    'to_regime': MarketRegime(states[i]).name
                })
        
        if transitions:
            logger.info(f"Detected {len(transitions)} regime transitions")
        
        return transitions
    
    def get_regime_name(self, state: int) -> str:
        """Get human-readable regime name."""
        return MarketRegime(state).name
