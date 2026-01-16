"""
==============================================================================
Unit Tests - FFT Signal Processor Engine
==============================================================================
Tests the FFT Engine's signal decomposition, frequency extraction,
and reconstruction capabilities.
==============================================================================
"""
import pytest
import numpy as np
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.analysis.fft_engine import FFTEngine


class TestFFTEngine:
    """Test suite for FFTEngine signal processing."""
    
    def test_initialization(self) -> None:
        """Test FFTEngine initializes with correct defaults."""
        engine = FFTEngine()
        
        assert engine.sample_rate == 1.0
        assert engine.last_fft is None
        assert engine.last_frequencies is None
    
    def test_initialization_custom_sample_rate(self) -> None:
        """Test FFTEngine with custom sample rate."""
        engine = FFTEngine(sample_rate=252.0)  # Trading days per year
        
        assert engine.sample_rate == 252.0
    
    def test_decompose_sinusoidal(self) -> None:
        """Test FFT correctly decomposes a pure sinusoidal signal."""
        engine = FFTEngine(sample_rate=100)
        
        # Create a 5Hz sine wave sampled at 100Hz
        t = np.linspace(0, 1, 100, endpoint=False)
        signal = np.sin(2 * np.pi * 5 * t)
        
        result = engine.decompose(signal)
        
        assert 'frequencies' in result
        assert 'amplitudes' in result
        assert 'phases' in result
        assert 'fft_complex' in result
        assert len(result['frequencies']) == 100
    
    def test_decompose_empty_signal_raises(self) -> None:
        """Test decompose raises ValueError for empty signal."""
        engine = FFTEngine()
        
        with pytest.raises(ValueError, match="empty signal"):
            engine.decompose(np.array([]))
    
    def test_decompose_non_1d_raises(self) -> None:
        """Test decompose raises ValueError for non-1D signal."""
        engine = FFTEngine()
        
        with pytest.raises(ValueError, match="must be 1D"):
            engine.decompose(np.array([[1, 2], [3, 4]]))
    
    def test_get_dominant_frequencies(self) -> None:
        """Test extraction of dominant frequencies from composite signal."""
        engine = FFTEngine(sample_rate=100)
        
        # Create composite signal: 5Hz (large) + 20Hz (medium) + 35Hz (small)
        t = np.linspace(0, 1, 100, endpoint=False)
        signal = 3 * np.sin(2 * np.pi * 5 * t) + \
                 2 * np.sin(2 * np.pi * 20 * t) + \
                 1 * np.sin(2 * np.pi * 35 * t)
        
        decomposition = engine.decompose(signal)
        dominant = engine.get_dominant_frequencies(decomposition, n=3)
        
        assert len(dominant) == 3
        # Frequencies should be approximately 5, 20, 35 Hz (sorted by amplitude)
        freqs = [f for f, a in dominant]
        assert any(abs(f - 5) < 1 for f in freqs)
        assert any(abs(f - 20) < 1 for f in freqs)
        assert any(abs(f - 35) < 1 for f in freqs)
    
    def test_reconstruct_perfect(self) -> None:
        """Test that full reconstruction produces original signal."""
        engine = FFTEngine()
        
        # Create arbitrary signal
        signal = np.array([1.0, 2.5, 3.2, 1.8, 0.5, 2.1, 4.0, 3.3])
        
        decomposition = engine.decompose(signal)
        reconstructed = engine.reconstruct(decomposition['fft_complex'])
        
        np.testing.assert_allclose(signal, reconstructed, atol=1e-10)
    
    def test_reconstruction_error_below_threshold(self) -> None:
        """Test reconstruction error is < 1% (acceptance criteria)."""
        engine = FFTEngine(sample_rate=100)
        
        # Create realistic VIX-like signal with noise
        np.random.seed(42)
        t = np.linspace(0, 10, 1000)
        signal = 20 + 5 * np.sin(2 * np.pi * 0.1 * t) + np.random.randn(1000) * 0.1
        
        decomposition = engine.decompose(signal)
        reconstructed = engine.reconstruct(decomposition['fft_complex'])
        error = engine.calculate_reconstruction_error(signal, reconstructed)
        
        assert error < 1.0, f"Reconstruction error {error}% exceeds 1% threshold"
    
    def test_analyze_full_pipeline(self) -> None:
        """Test the analyze convenience method."""
        engine = FFTEngine(sample_rate=100)
        
        # Simple sinusoidal signal
        t = np.linspace(0, 1, 100, endpoint=False)
        signal = np.sin(2 * np.pi * 10 * t)
        
        result = engine.analyze(signal, top_n=3)
        
        assert 'decomposition' in result
        assert 'dominant_frequencies' in result
        assert 'reconstructed' in result
        assert 'reconstruction_error_pct' in result
        assert 'meets_acceptance' in result
        assert result['meets_acceptance'] is True
    
    def test_single_point_signal(self) -> None:
        """Test handling of single-point signal (edge case)."""
        engine = FFTEngine()
        
        signal = np.array([5.0])
        decomposition = engine.decompose(signal)
        
        assert len(decomposition['frequencies']) == 1
        assert decomposition['amplitudes'][0] == pytest.approx(5.0)
    
    def test_constant_signal(self) -> None:
        """Test handling of constant signal (DC only)."""
        engine = FFTEngine()
        
        signal = np.full(100, 15.0)
        decomposition = engine.decompose(signal)
        
        # DC component should dominate
        dominant = engine.get_dominant_frequencies(decomposition, n=1)
        # For constant signal, all positive frequency amplitudes should be ~0
        assert len(dominant) <= 1
