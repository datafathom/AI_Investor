"""
==============================================================================
Unit Tests - ETF Catalog
==============================================================================
Tests the ETF categorization and lookup system.
==============================================================================
"""
import pytest

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.etf_catalog import ETFCatalog, ETFCategory, LeverageType


class TestETFCatalog:
    """Test suite for ETF Catalog service."""
    
    def test_initialization(self) -> None:
        """Test catalog initializes with ETFs."""
        catalog = ETFCatalog()
        
        assert len(catalog.etfs) > 0
        assert 'UVXY' in catalog.etfs
        assert 'SPY' in catalog.etfs
    
    def test_get_etf(self) -> None:
        """Test getting ETF by symbol."""
        catalog = ETFCatalog()
        
        uvxy = catalog.get('UVXY')
        
        assert uvxy is not None
        assert uvxy.symbol == 'UVXY'
        assert uvxy.category == ETFCategory.VOLATILITY
    
    def test_case_insensitive_lookup(self) -> None:
        """Test case-insensitive symbol lookup."""
        catalog = ETFCatalog()
        
        assert catalog.get('uvxy') is not None
        assert catalog.get('Uvxy') is not None
    
    def test_get_volatility_products(self) -> None:
        """Test getting all VIX products."""
        catalog = ETFCatalog()
        
        vol_etfs = catalog.get_volatility_products()
        
        assert len(vol_etfs) >= 3
        assert all(e.category == ETFCategory.VOLATILITY for e in vol_etfs)
        symbols = [e.symbol for e in vol_etfs]
        assert 'UVXY' in symbols
        assert 'VIXY' in symbols
    
    def test_get_leveraged_products(self) -> None:
        """Test getting all leveraged ETFs."""
        catalog = ETFCatalog()
        
        leveraged = catalog.get_leveraged_products()
        
        assert len(leveraged) >= 6
        symbols = [e.symbol for e in leveraged]
        assert 'TQQQ' in symbols
        assert 'SQQQ' in symbols
    
    def test_get_currency_products(self) -> None:
        """Test getting currency ETFs."""
        catalog = ETFCatalog()
        
        currency = catalog.get_currency_products()
        
        assert len(currency) >= 3
        symbols = [e.symbol for e in currency]
        assert 'UUP' in symbols
        assert 'FXE' in symbols
    
    def test_leverage_type(self) -> None:
        """Test leverage type is correctly assigned."""
        catalog = ETFCatalog()
        
        tqqq = catalog.get('TQQQ')
        sqqq = catalog.get('SQQQ')
        spy = catalog.get('SPY')
        
        assert tqqq.leverage == LeverageType.TRIPLE
        assert sqqq.leverage == LeverageType.INVERSE_TRIPLE
        assert spy.leverage == LeverageType.NONE
    
    def test_get_related_etfs(self) -> None:
        """Test getting related ETFs."""
        catalog = ETFCatalog()
        
        related = catalog.get_related('UVXY')
        
        assert len(related) > 0
        symbols = [e.symbol for e in related]
        assert 'VIXY' in symbols or 'SVXY' in symbols
    
    def test_get_inverse_pair(self) -> None:
        """Test finding inverse ETF pair."""
        catalog = ETFCatalog()
        
        inverse = catalog.get_inverse_pair('TQQQ')
        
        assert inverse is not None
        assert inverse.symbol == 'SQQQ'
    
    def test_get_hedge_candidates(self) -> None:
        """Test getting ETFs suitable for hedging."""
        catalog = ETFCatalog()
        
        hedges = catalog.get_hedge_candidates()
        
        assert len(hedges) > 0
        # Should include VIX products and inverse ETFs
        symbols = [e.symbol for e in hedges]
        assert any(s in symbols for s in ['UVXY', 'SQQQ', 'SPXU'])
    
    def test_get_aggressive_candidates(self) -> None:
        """Test getting ETFs for aggressive plays."""
        catalog = ETFCatalog()
        
        aggressive = catalog.get_aggressive_candidates()
        
        assert len(aggressive) > 0
        # Should be leveraged bull ETFs
        symbols = [e.symbol for e in aggressive]
        assert 'TQQQ' in symbols
        assert 'SOXL' in symbols
    
    def test_unknown_etf_returns_none(self) -> None:
        """Test that unknown symbol returns None."""
        catalog = ETFCatalog()
        
        assert catalog.get('NOTREAL') is None
    
    def test_list_all(self) -> None:
        """Test listing all ETF symbols."""
        catalog = ETFCatalog()
        
        all_symbols = catalog.list_all()
        
        assert len(all_symbols) > 10
        assert 'SPY' in all_symbols
        assert 'UVXY' in all_symbols
    
    def test_get_summary(self) -> None:
        """Test getting category summary."""
        catalog = ETFCatalog()
        
        summary = catalog.get_summary()
        
        assert 'volatility' in summary
        assert 'leveraged_bull' in summary
        assert summary['volatility'] >= 3
