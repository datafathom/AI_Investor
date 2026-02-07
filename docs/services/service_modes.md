# Backend Service: Modes (System States)

## Overview
The **Modes Service** manages the high-level operational states of the Sovereign OS. Unlike simple configuration flags, "Modes" are systemic regimes that fundamentally alter how the platform behaves. This includes **Zen Mode** (which filters out tactical noise to focus on long-term compounding), **Shield Mode** (which locks down capital during extreme risk), and **GEX Regimes** (which adjust trading logic based on market maker gamma exposure).

## Core Components

### 1. Zen Mode Controller (`zen_mode.py`, `tactical_noise_filter.py`)
The "Homeostasis" engine for psychological safety.
- **Noise Filtering**: When activated, the `TacticalNoiseFilter` suppresses high-frequency alerts, news tickers, and PnL volatility updates. This prevents "chart staring" and FOMO-driven errors.
- **Long-Term Focus**: Shifts the dashboard UI to emphasize "Goal Progress" and "Retirement Horizons" rather than daily price action.

### 2. Volatility Regime Setter (`gex_regime.py`)
Adapts system logic to market structure.
- **Gamma Exposure (GEX) Analysis**: Calculates the total GEX of the market to determine the current volatility regime.
    - **Positive GEX**: Implies mean-reverting behavior (buy dips, sell rips).
    - **Negative GEX**: Implies correlation breakdown and crash acceleration (switch to breakout/momentum logic).

### 3. Shield Logic (`shield_logic.py`)
The global kill-switch and defense mechanism.
- **System Lockdown**: A Redis-backed state that, when active, overrides all other services to block capital outflows and new risk-taking. It is triggered by "Black Swan" events or manual intervention.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used | Frontend Status |
| :--- | :--- | :--- | :--- |
| **Zen Station** | Homeostasis Overlay | `zen_mode.activate()` | **Implemented** (`HomeostasisOverlay.jsx`) |
| **Zen Station** | Retirement Gauge | `zen_mode` (Goal Tracking) | **Implemented** (`RetirementGauge.jsx`) |
| **Market Dashboard** | GEX Profile Chart | `gex_regime.determine_regime()` | **Implemented** (`GEXProfile.jsx`) |
| **Global Header** | Shield Status Indicator| `shield_logic.is_active()` | **Partially Implemented** |

## Dependencies
- `redis`: Persists the Shield Mode state across system restarts.
- `logging`: Critical for auditing state transitions (e.g., "Why did the system enter Shield Mode at 03:00 AM?").

## Usage Examples

### Activating Zen Mode to Prevent Panic Selling
```python
from services.modes.zen_mode import ZenMode
from services.modes.tactical_noise_filter import TacticalNoiseFilter

zen = ZenMode()
noise_filter = TacticalNoiseFilter()

# User engages "Zen Mode" after a 5% market drop
zen.activate(reason="High stress detected. Focusing on 20-year horizon.")

# Backend suppresses all intraday price alerts
noise_filter.enable_zen()

print(f"System State: {zen.get_status()}") 
# Output: {'active': True, 'reason': 'High stress detected...'}
```

### Adjusting Strategy based on GEX Regime
```python
from services.modes.gex_regime import GEXRegimeSetter

gex_setter = GEXRegimeSetter()

# Total Market GEX (in billions)
current_gex = -2500000000.0 # -$2.5B (High Volatility Danger Zone)

regime = gex_setter.determine_regime(total_gex=current_gex)

if regime == "HIGH_VOL_CRASH_ACCELERATION":
    print("WARNING: Negative Gamma Environment. Hedging requirements doubled.")
    # Trigger hedging logic...
```
