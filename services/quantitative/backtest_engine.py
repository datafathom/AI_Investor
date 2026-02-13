import logging
import random
import pandas as pd
import numpy as np
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class BacktestEngine:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(BacktestEngine, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        
        self.results_cache = {}
        self._initialized = True

    async def run_backtest(self, strategy: Dict) -> Dict:
        """
        Strategy: {
            "ticker": "AAPL",
            "start_date": "2023-01-01",
            "end_date": "2023-12-31",
            "initial_capital": 100000,
            "rules": [
                {"type": "entry", "indicator": "RSI", "operator": "<", "value": 30, "action": "BUY"},
                {"type": "exit", "indicator": "RSI", "operator": ">", "value": 70, "action": "SELL"}
            ]
        }
        """
        ticker = strategy.get('ticker', 'AAPL')
        capital = strategy.get('initial_capital', 100000)
        
        # Mock price data generation
        dates = pd.date_range(start=strategy.get('start_date', '2023-01-01'), end=strategy.get('end_date', '2023-12-31'))
        prices = []
        price = 150.0
        rsi_values = []
        
        random.seed(42) # Deterministic for demo
        for _ in dates:
            change = random.normalvariate(0, 2.0)
            price += change
            prices.append(max(0.1, price))
            rsi_values.append(random.uniform(20, 80)) # Mock RSI
            
        # Sim execution
        holdings = 0
        trades = []
        equity_curve = []
        
        entry_rule = next((r for r in strategy.get('rules', []) if r['type'] == 'entry'), None)
        exit_rule = next((r for r in strategy.get('rules', []) if r['type'] == 'exit'), None)
        
        for i, date in enumerate(dates):
            current_price = prices[i]
            current_rsi = rsi_values[i]
            
            # Entry logic
            if holdings == 0 and entry_rule:
                signal = False
                if entry_rule['indicator'] == 'RSI':
                    val = float(entry_rule['value'])
                    if entry_rule['operator'] == '<' and current_rsi < val: signal = True
                    elif entry_rule['operator'] == '>' and current_rsi > val: signal = True
                
                if signal:
                    shares = int(capital / current_price)
                    cost = shares * current_price
                    capital -= cost
                    holdings = shares
                    trades.append({
                        "date": date.strftime("%Y-%m-%d"),
                        "type": "BUY",
                        "price": round(current_price, 2),
                        "shares": shares,
                        "value": round(cost, 2)
                    })

            # Exit logic
            elif holdings > 0 and exit_rule:
                signal = False
                if exit_rule['indicator'] == 'RSI':
                    val = float(exit_rule['value'])
                    if exit_rule['operator'] == '<' and current_rsi < val: signal = True
                    elif exit_rule['operator'] == '>' and current_rsi > val: signal = True
                
                if signal:
                    revenue = holdings * current_price
                    capital += revenue
                    trades.append({
                        "date": date.strftime("%Y-%m-%d"),
                        "type": "SELL",
                        "price": round(current_price, 2),
                        "shares": holdings,
                        "value": round(revenue, 2),
                        "pnl": round(revenue - trades[-1]['value'], 2)
                    })
                    holdings = 0

            equity = capital + (holdings * current_price)
            equity_curve.append({"date": date.strftime("%Y-%m-%d"), "equity": round(equity, 2)})

        # Calc metrics
        total_return = (equity_curve[-1]['equity'] - strategy.get('initial_capital', 100000)) / strategy.get('initial_capital', 100000)
        max_drawdown = 0
        peak = equity_curve[0]['equity']
        for pt in equity_curve:
            if pt['equity'] > peak: peak = pt['equity']
            dd = (peak - pt['equity']) / peak
            if dd > max_drawdown: max_drawdown = dd
            
        result = {
            "id": f"bt_{datetime.now().timestamp()}",
            "equity_curve": equity_curve,
            "trades": trades,
            "metrics": {
                "total_return": round(total_return * 100, 2),
                "max_drawdown": round(max_drawdown * 100, 2),
                "sharpe_ratio": round(random.uniform(0.5, 2.5), 2),
                "win_rate": round(random.uniform(40, 70), 2)
            }
        }
        self.results_cache[result['id']] = result
        return result

    async def get_test_results(self, id: str) -> Optional[Dict]:
        return self.results_cache.get(id)
