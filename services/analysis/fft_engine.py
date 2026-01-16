"""
==============================================================================
AI Investor - FFT Signal Processor Engine
==============================================================================
PURPOSE:
    Fast Fourier Transform engine for decomposing VIX and market time-series
    data into frequency components. Enables identification of dominant market
    oscillation patterns for regime detection.

THEORY:
    The "Yellowstone Wolf" principle: Markets exhibit natural oscillations
    similar to ecological systems. FFT isolates these frequencies for pattern
    recognition and mean-reversion signal generation.

ACCEPTANCE CRITERIA:
    - < 1% error in signal reconstruction
    - Successfully isolate top 3 dominant frequencies
==============================================================================
"""
from typing import Dict, List, Optional, Tuple
import numpy as np
from numpy.typing import NDArray
import logging

logger = logging.getLogger(__name__)


class FFTEngine:
    """
    Fast Fourier Transform engine for signal decomposition.
    
    Decomposes time-series data into frequency components to identify
    dominant market oscillation patterns.
    
    Attributes:
        sample_rate (float): Sampling rate of input signal (samples/time unit).
        last_fft (Optional[NDArray]): Cached FFT result from last decomposition.
        last_frequencies (Optional[NDArray]): Cached frequency bins.
    """
    
    def __init__(self, sample_rate: float = 1.0) -> None:
        """
        Initialize the FFT Engine.
        
        Args:
            sample_rate: Number of samples per time unit (e.g., 1.0 for daily data).
        """
        self.sample_rate = sample_rate
        self.last_fft: Optional[NDArray] = None
        self.last_frequencies: Optional[NDArray] = None
        self._last_signal_length: int = 0
        logger.info(f"FFTEngine initialized with sample_rate={sample_rate}")
    
    def decompose(self, signal: NDArray) -> Dict[str, NDArray]:
        """
        Apply FFT to decompose the input signal into frequency components.
        
        Args:
            signal: 1D numpy array of time-series data (e.g., VIX values).
            
        Returns:
            Dictionary containing:
                - 'frequencies': Array of frequency bin values
                - 'amplitudes': Magnitude of each frequency component
                - 'phases': Phase angle of each frequency component
                - 'fft_complex': Raw complex FFT output
                
        Raises:
            ValueError: If signal is empty or not 1D.
        """
        if signal.size == 0:
            raise ValueError("Cannot decompose empty signal")
        if signal.ndim != 1:
            raise ValueError(f"Signal must be 1D, got {signal.ndim}D")
        
        n = len(signal)
        self._last_signal_length = n
        
        # Apply FFT
        fft_result = np.fft.fft(signal)
        self.last_fft = fft_result
        
        # Compute frequency bins
        frequencies = np.fft.fftfreq(n, d=1.0/self.sample_rate)
        self.last_frequencies = frequencies
        
        # Compute amplitudes (magnitude) and phases
        amplitudes = np.abs(fft_result) / n
        phases = np.angle(fft_result)
        
        logger.debug(f"Decomposed signal of length {n} into {n} frequency bins")
        
        return {
            'frequencies': frequencies,
            'amplitudes': amplitudes,
            'phases': phases,
            'fft_complex': fft_result
        }
    
    def get_dominant_frequencies(
        self, 
        decomposition: Dict[str, NDArray], 
        n: int = 3
    ) -> List[Tuple[float, float]]:
        """
        Extract the top N dominant frequency components from decomposition.
        
        Args:
            decomposition: Output from decompose() method.
            n: Number of dominant frequencies to return.
            
        Returns:
            List of (frequency, amplitude) tuples sorted by amplitude descending.
            Only positive frequencies are returned (excludes DC and negative).
        """
        frequencies = decomposition['frequencies']
        amplitudes = decomposition['amplitudes']
        
        # Only consider positive frequencies (real signal has symmetric FFT)
        positive_mask = frequencies > 0
        pos_freqs = frequencies[positive_mask]
        pos_amps = amplitudes[positive_mask]
        
        # Sort by amplitude descending
        sorted_indices = np.argsort(pos_amps)[::-1]
        
        # Take top n
        top_n = min(n, len(sorted_indices))
        dominant = [
            (float(pos_freqs[i]), float(pos_amps[i]))
            for i in sorted_indices[:top_n]
        ]
        
        logger.info(f"Identified {top_n} dominant frequencies: {dominant}")
        return dominant
    
    def reconstruct(
        self, 
        fft_complex: NDArray, 
        n_components: Optional[int] = None
    ) -> NDArray:
        """
        Reconstruct the signal from FFT components using inverse FFT.
        
        Args:
            fft_complex: Complex FFT array (from decompose()['fft_complex']).
            n_components: Optional limit on number of frequency components to use.
                         If None, uses all components for perfect reconstruction.
                         
        Returns:
            Reconstructed time-series signal as real-valued array.
        """
        if n_components is not None:
            # Zero out all but the n_components largest magnitudes
            amplitudes = np.abs(fft_complex)
            threshold_idx = np.argsort(amplitudes)[::-1][n_components]
            threshold = amplitudes[threshold_idx]
            
            filtered_fft = fft_complex.copy()
            filtered_fft[amplitudes < threshold] = 0
            reconstructed = np.fft.ifft(filtered_fft).real
        else:
            reconstructed = np.fft.ifft(fft_complex).real
        
        return reconstructed
    
    def calculate_reconstruction_error(
        self, 
        original: NDArray, 
        reconstructed: NDArray
    ) -> float:
        """
        Calculate the normalized reconstruction error (RMSE / signal range).
        
        Args:
            original: Original input signal.
            reconstructed: Reconstructed signal from inverse FFT.
            
        Returns:
            Normalized error as a percentage (0.0 to 100.0+).
            Values < 1.0 meet acceptance criteria.
        """
        if original.size == 0:
            return 0.0
            
        rmse = np.sqrt(np.mean((original - reconstructed) ** 2))
        signal_range = np.ptp(original)  # peak-to-peak range
        
        if signal_range == 0:
            return 0.0 if rmse == 0 else float('inf')
        
        normalized_error = (rmse / signal_range) * 100
        
        logger.debug(f"Reconstruction error: {normalized_error:.4f}%")
        return float(normalized_error)
    
    def analyze(self, signal: NDArray, top_n: int = 3) -> Dict:
        """
        Convenience method: Full analysis pipeline in one call.
        
        Args:
            signal: Input time-series data.
            top_n: Number of dominant frequencies to extract.
            
        Returns:
            Complete analysis dictionary with decomposition results,
            dominant frequencies, and reconstruction validation.
        """
        decomposition = self.decompose(signal)
        dominant = self.get_dominant_frequencies(decomposition, n=top_n)
        
        reconstructed = self.reconstruct(decomposition['fft_complex'])
        error = self.calculate_reconstruction_error(signal, reconstructed)
        
        return {
            'decomposition': decomposition,
            'dominant_frequencies': dominant,
            'reconstructed': reconstructed,
            'reconstruction_error_pct': error,
            'meets_acceptance': error < 1.0
        }
