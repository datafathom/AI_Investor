# Phase 5: Major Pair Pips/Pipettes Calculation Logic

> **Status**: `[x]` Completed  
> **Last Updated**: 2026-01-25  
> **Owner**: Full Stack Team

---

## 📋 Overview

**Description**: Develop the high-precision mathematical engine for measuring market movement in pips and pipettes for Major Pairs.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)

---

## 🎯 Sub-Deliverables

### 5.1 Pip Calculation (4th Decimal) `[/]`

**Acceptance Criteria**: Implement calculation logic for the fourth decimal place (Pip) in GBP/USD, EUR/USD, and AUD/USD.

#### Backend Implementation

| Component | File Path | Status |
| :--- | :--- | :--- |
| Pip Calculator Service | `services/pip_calculator.py` | `[x]` |
| Currency Pair Config | `config/currency_pairs.py` | `[x]` |
| Decimal Handler | `utils/decimal_handler.py` | `[x]` |

#### Calculation Logic

```python
def calculate_pips(price1: Decimal, price2: Decimal, pair: str) -> Decimal:
    """
    Calculate pip difference between two prices.
    
    For most pairs (EUR/USD, GBP/USD): 1 pip = 0.0001 (4th decimal)
    For JPY pairs (USD/JPY): 1 pip = 0.01 (2nd decimal)
    
    Example:
        EUR/USD: 1.09500 to 1.09520 = 2.0 pips
        USD/JPY: 149.500 to 149.520 = 2.0 pips
    """
    pip_divisor = get_pip_divisor(pair)  # 0.0001 or 0.01
    return (price2 - price1) / pip_divisor
```

#### Tests

| Test Type | File Path | Status |
| :--- | :--- | :--- |
| Unit: Pip Calculator | `tests/unit/test_pip_calculator.py` | `[x]` |
| Unit: Decimal Handler | `tests/unit/test_decimal_handler.py` | `[x]` |

---

### 5.2 Pipette Detection (5th Decimal) `[x]`

**Acceptance Criteria**: Configure detection for the fifth decimal place (Pipette) to ensure tenth-of-a-pip precision.

#### Backend Implementation

| Component | File Path | Status |
| :--- | :--- | :--- |
| Pipette Detector | `services/pipette_detector.py` | `[x]` |
| Precision Config | `config/precision.py` | `[x]` |

#### Pipette Logic

```python
def calculate_pipettes(price1: Decimal, price2: Decimal, pair: str) -> Decimal:
    """
    Calculate pipette difference (1/10th of a pip).
    
    For most pairs: 1 pipette = 0.00001 (5th decimal)
    For JPY pairs: 1 pipette = 0.001 (3rd decimal)
    """
    pipette_divisor = get_pipette_divisor(pair)
    return (price2 - price1) / pipette_divisor
```

---

### 5.3 Benchmark Accuracy Verification `[x]`

**Acceptance Criteria**: Verify pip calculation accuracy against the 1.26956 benchmark provided in the essential trading framework.

#### Test Cases

| Pair | Price 1 | Price 2 | Expected Pips | Status |
| :--- | :--- | :--- | :--- | :--- |
| GBP/USD | 1.26956 | 1.27056 | 10.0 | `[x]` |
| EUR/USD | 1.08500 | 1.08600 | 10.0 | `[x]` |
| USD/JPY | 149.000 | 149.100 | 10.0 | `[x]` |
| AUD/USD | 0.65000 | 0.65100 | 10.0 | `[x]` |

---

### 5.4 High-Precision Postgres Types `[x]`

**Acceptance Criteria**: Implement high-precision numeric types in Postgres to prevent rounding drift in high-frequency calculations.

#### Database Schema

```sql
-- Use DECIMAL(20, 8) for price storage
ALTER TABLE price_telemetry 
    ALTER COLUMN bid TYPE DECIMAL(20, 8),
    ALTER COLUMN ask TYPE DECIMAL(20, 8),
    ALTER COLUMN mid TYPE DECIMAL(20, 8);

-- Create pip calculation function
CREATE OR REPLACE FUNCTION calculate_pip_difference(
    price1 DECIMAL(20, 8),
    price2 DECIMAL(20, 8),
    pair VARCHAR(10)
) RETURNS DECIMAL(10, 2) AS $$
DECLARE
    pip_divisor DECIMAL(10, 8);
BEGIN
    IF pair LIKE '%JPY' THEN
        pip_divisor := 0.01;
    ELSE
        pip_divisor := 0.0001;
    END IF;
    RETURN (price2 - price1) / pip_divisor;
END;
$$ LANGUAGE plpgsql;
```

| Component | File Path | Status |
| :--- | :--- | :--- |
| Migration | `migrations/004_high_precision.sql` | `[x]` |

---

### 5.5 Pipometer Widget `[x]`

**Acceptance Criteria**: Deploy a visual Pipometer widget that translates raw price changes into actionable pip distance.

#### Frontend Implementation

| Component | File Path | Status |
| :--- | :--- | :--- |
| Pipometer Component | `frontend2/src/components/Pipometer/Pipometer.jsx` | `[x]` |
| Pipometer Styles | `frontend2/src/components/Pipometer/Pipometer.css` | `[x]` |
| usePipometer Hook | `frontend2/src/hooks/usePipometer.js` | `[x]` |

#### Widget Features

| Feature | Description | Status |
| :--- | :--- | :--- |
| Real-time Display | Show live pip movement | `[ ]` |
| Color Coding | Green (up), Red (down) | `[ ]` |
| Velocity Indicator | Pips per second | `[ ]` |
| Historical Sparkline | Last 60 seconds | `[ ]` |

---

## Phase Completion Summary

| Deliverable | Status | E2E Verified |
| :--- | :--- | :--- |
| 5.1 Pip Calculation | `[x]` | `[✓]` |
| 5.2 Pipette Detection | `[x]` | `[✓]` |
| 5.3 Benchmark Accuracy | `[x]` | `[✓]` |
| 5.4 Postgres Precision | `[x]` | `[✓]` |
| 5.5 Pipometer Widget | `[x]` | `[✓]` |

**Phase Status**: `[x]` COMPLETED

---

## CLI Commands

| Command | Description | Status |
| :--- | :--- | :--- |
| `python cli.py pip-test <pair> <p1> <p2>` | Test pip calculation | `[ ]` |
| `python cli.py pip-benchmark` | Run accuracy benchmarks | `[ ]` |

---

*Last verified: 2026-01-25*
