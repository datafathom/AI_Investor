
import pytest
from services.execution.paper_exchange import PaperExchange

class TestPaperExchange:
    
    def test_buy_stock(self):
        exchange = PaperExchange(initial_cash=10000.0)
        
        # Buy 10 AAPL @ $150
        order = exchange.submit_market_order('AAPL', 10, 'BUY', 150.0)
        
        assert order['status'] == 'FILLED'
        assert exchange.cash == 8500.0 # 10000 - 1500
        assert exchange.positions['AAPL']['quantity'] == 10
        assert exchange.positions['AAPL']['avg_price'] == 150.0
        
    def test_insufficient_funds(self):
        exchange = PaperExchange(initial_cash=100.0)
        order = exchange.submit_market_order('AAPL', 10, 'BUY', 150.0)
        
        assert order['status'] == 'REJECTED'
        assert order['reason'] == 'Insufficient Funds'
        assert exchange.cash == 100.0 # Unchanged
        
    def test_sell_stock(self):
        exchange = PaperExchange(initial_cash=1000.0)
        # Setup position
        exchange.submit_market_order('TSLA', 5, 'BUY', 200.0)
        
        # Sell 2 TSLA @ $210
        order = exchange.submit_market_order('TSLA', 2, 'SELL', 210.0)
        
        assert order['status'] == 'FILLED'
        assert exchange.positions['TSLA']['quantity'] == 3 # 5 - 2
        assert exchange.cash == 420.0 # 0 remaining cash + 420 proceeds (initial was spent)
        
    def test_sell_more_than_owned(self):
        exchange = PaperExchange(initial_cash=1000.0)
        order = exchange.submit_market_order('TSLA', 1, 'SELL', 200.0)
        
        assert order['status'] == 'REJECTED'
        assert 'Insufficient Position' in order['reason']
