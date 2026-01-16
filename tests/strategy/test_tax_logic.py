
import pytest
from datetime import datetime, timedelta
from services.strategy.tax_harvester import TaxHarvester

class TestTaxHarvester:
    
    def test_scan_harvestable_losses_thresholds(self):
        harvester = TaxHarvester()
        
        positions = [
            {'symbol': 'BIG_LOSS', 'quantity': 100, 'cost_basis_per_share': 100.0}, # Val $10k
            {'symbol': 'SMALL_LOSS', 'quantity': 100, 'cost_basis_per_share': 100.0},
            {'symbol': 'PROFIT', 'quantity': 100, 'cost_basis_per_share': 100.0},
            {'symbol': 'RAW_LOSS_DOLLAR', 'quantity': 1000, 'cost_basis_per_share': 10.0} # $10k basis
        ]
        
        prices = {
            'BIG_LOSS': 90.0,  # -10% (Should Harvest)
            'SMALL_LOSS': 99.0, # -1% (No Harvest)
            'PROFIT': 110.0,    # +10% (No Harvest)
            'RAW_LOSS_DOLLAR': 9.4 # -6% (-$600). Should Harvest.
        }
        
        recs = harvester.scan_harvestable_losses(positions, prices)
        symbols = [r['symbol'] for r in recs]
        
        assert 'BIG_LOSS' in symbols
        assert 'SMALL_LOSS' not in symbols
        assert 'PROFIT' not in symbols
        assert 'RAW_LOSS_DOLLAR' in symbols

    def test_wash_sale_restriction(self):
        harvester = TaxHarvester()
        
        today = datetime.now()
        recent_loss_date = today - timedelta(days=10)
        old_loss_date = today - timedelta(days=40)
        
        history = [
            {'symbol': 'RECENT_LOSS', 'action': 'SELL', 'date': recent_loss_date.isoformat(), 'pnl': -500.0},
            {'symbol': 'OLD_LOSS', 'action': 'SELL', 'date': old_loss_date.isoformat(), 'pnl': -500.0},
            {'symbol': 'RECENT_GAIN', 'action': 'SELL', 'date': recent_loss_date.isoformat(), 'pnl': 500.0}
        ]
        
        # Recent loss -> Restricted
        assert harvester.check_wash_sale_restriction('RECENT_LOSS', history, today) is True
        
        # Old loss (>30 days) -> Not Restricted
        assert harvester.check_wash_sale_restriction('OLD_LOSS', history, today) is False
        
        # Recent Gain -> Not Restricted
        assert harvester.check_wash_sale_restriction('RECENT_GAIN', history, today) is False
