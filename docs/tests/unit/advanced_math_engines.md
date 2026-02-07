# Documentation: `tests/unit/test_fft_engine.py` & `test_hmm_engine.py`

## Overview
These components represent the "Advanced Signal Processing" layer. They decompose market noise into actionable frequencies (FFT) and classify market phases into BULL, BEAR, or SIDEWAYS (HMM).

## Components Under Test
- `services.analysis.fft_engine.FFTEngine`: Fast Fourier Transform for frequency extraction.
- `services.analysis.hmm_engine.HMMRegimeDetector`: Hidden Markov Model for phase classification.

## Key Test Scenarios

### 1. Signal Signal Decomposition (FFT)
- **Goal**: Verify that pure frequencies can be extracted from composite signals.
- **Assertions**:
    - Correctly identifies 5Hz, 20Hz, and 35Hz dominant frequencies.
    - **Acceptance Criteria**: Reconstruction error must be < 1% when regenerating the original signal from its spectral components.

### 2. Regime Detection (HMM)
- **Goal**: Verify the ability to learn and classify market states.
- **Assertions**: 
    - Correctly identifies transitions between synthetic BULL and BEAR datasets.
    - Convergence is achieved on stable data within the iteration limit.
    - Transition matrix follows probability rules (rows sum to 1.0).

## Holistic Context
Market regimes are the "weather" for trading. The HMM engine detects the weather, while the FFT engine listens to the "vibrations" (volatility cycles). Together, they allow the AI to switch its strategy from aggressive to defensive before a crash fully manifests.
