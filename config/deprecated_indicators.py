"""
Deprecated Retail Indicators.
Blacklist of indicators categorized as 'Retail Noise' and removed from institutional engine.
"""

RETAIL_INDICATOR_BLACKLIST = [
    'RSI',
    'Relative Strength Index',
    'MACD',
    'Moving Average Convergence Divergence',
    'Bollinger Bands',
    'Stochastic Oscillator',
    'EMA Crossover',
    'SMA Crossover'
]

PURGE_REASON = "Retail indicators are often lagging and used as liquidity by institutional players. Decommissioned in favor of Market Structure and Order Flow."
