# Backend Service: Journal

## Overview
The **Journal Service** is the platform's behavioral auditing and strategy optimization layer. It transforms standard trade logs into actionable insights by analyzing the psychological and structural patterns of an investor's performance. By identifying statistically dominant "Setups" and highlighting temporal performance skews (e.g., specific days of the week), it helps traders refine their edge and eliminate sub-optimal behaviors.

## Core Components

### 1. Journal Pattern Analyzer (`analyzer.py`)
The quantitative core of the trading diary.
- **Temporal PnL Analysis**: Aggregates trade performance by the day of the week. This allows investors to identify biological or psychological patterns (e.g., high fatigue on Fridays leading to poor decision-making).
- **Setup Leaderboard**: Evaluates different trading strategies (e.g., Mean Reversion, Momentum, Pullback) based on their average **R-Multiple**. It identifies which "Setup" is statistically most profitable for the account, enabling the investor to focus capital on their strongest competitive advantages.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used |
| :--- | :--- | :--- |
| **Trader Station** | Setup Efficiency Leaderboard | `journal_analyzer.get_best_setup()` |
| **Trader Station** | Day-of-Week PnL Heatmap | `journal_analyzer.analyze_by_day()` |
| **Portfolio Detail** | Behavioral Consistency Score | `journal_analyzer.analyze_by_day()` |
| **Strategist Station** | Strategy Drift Audit | `journal_analyzer` (Historical r-multiples) |

## Dependencies
- `logging`: Records the extraction of significant strategic insights from the trade journal.

## Usage Examples

### Identifying the Most Profitable Trading Setup
```python
from services.journal.analyzer import JournalAnalyzer

analyzer = JournalAnalyzer()

# Historical trades with R-Multiple performance
history = [
    {"setup": "BREAKOUT", "r_multiple": 3.5},
    {"setup": "MEAN_REVERSION", "r_multiple": 1.2},
    {"setup": "BREAKOUT", "r_multiple": 4.0},
    {"setup": "PULLBACK", "r_multiple": 2.1}
]

best = analyzer.get_best_setup(trades=history)
print(f"Statistically Dominant Setup: {best}")
```

### Analyzing PnL Distribution by Day
```python
from services.journal.analyzer import JournalAnalyzer

analyzer = JournalAnalyzer()

trades = [
    {"day": "Monday", "pnl": 1200.0},
    {"day": "Monday", "pnl": -500.0},
    {"day": "Friday", "pnl": -2500.0},  # Significant loss on Friday
    {"day": "Wednesday", "pnl": 800.0}
]

daily_stats = analyzer.analyze_by_day(trades=trades)

for day, pnl in daily_stats.items():
    print(f"Day: {day} | Cumulative Net PnL: ${pnl:,.2f}")
```
