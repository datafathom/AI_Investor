# Phase 12: Major Pair Decimal Scaling Configuration

> **Status**: `[ ]` Not Started  
> **Last Updated**: 2026-01-25  
> **Owner**: Trading Infrastructure Team

---

## 📋 Overview

**Description**: Lock the system's numeric engine to the specific decimal precision required for institutional FX major pairs.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)

---

## 🎯 Sub-Deliverables

### 12.1 5-Decimal Precision Engine `[ ]`

**Acceptance Criteria**: Configure the pricing engine to handle 5 decimal places (including pipettes) for EUR/USD and GBP/USD.

| Component | File Path | Status |
|-----------|-----------|--------|
| Precision Engine | `services/pricing/precision_engine.py` | `[ ]` |
| Decimal Config | `config/decimal_precision.py` | `[ ]` |

---

### 12.2 JPY Pair 3-Decimal Handling `[ ]`

**Acceptance Criteria**: Verify scaling logic for JPY pairs (e.g., USD/JPY) to ensure correct 3-decimal precision handling.

| Currency Pair | Decimal Places | Pip Position |
|---------------|----------------|--------------|
| EUR/USD | 5 | 4th |
| GBP/USD | 5 | 4th |
| USD/JPY | 3 | 2nd |
| EUR/JPY | 3 | 2nd |

---

### 12.3 Floating-Point Rounding Logic `[ ]`

**Acceptance Criteria**: Implement rounding logic that prevents floating-point inaccuracies from polluting position size calculations.

| Component | File Path | Status |
|-----------|-----------|--------|
| Safe Rounding | `utils/safe_rounding.py` | `[ ]` |
| Decimal Handler | `utils/decimal_handler.py` | `[ ]` |

---

### 12.4 Dynamic GUI Decimal Display `[ ]`

**Acceptance Criteria**: Ensure the GUI dynamically adjusts decimal visibility based on the asset's quote currency standards.

| Component | File Path | Status |
|-----------|-----------|--------|
| Price Formatter | `frontend2/src/utils/priceFormatter.js` | `[ ]` |
| Decimal Display | `frontend2/src/components/PriceDisplay.jsx` | `[ ]` |

---

### 12.5 Flash Crash Stress Test `[ ]`

**Acceptance Criteria**: Test scaling logic against a 1,000-pip flash crash scenario to ensure no numeric overflow errors.

| Component | File Path | Status |
|-----------|-----------|--------|
| Stress Test | `tests/stress/test_flash_crash.py` | `[ ]` |

---

## 📊 Phase Completion Summary

| Deliverable | Status | E2E Verified |
|-------------|--------|--------------|
| 12.1 5-Decimal Precision | `[ ]` | `[ ]` |
| 12.2 JPY Handling | `[ ]` | `[ ]` |
| 12.3 Rounding Logic | `[ ]` | `[ ]` |
| 12.4 GUI Decimal Display | `[ ]` | `[ ]` |
| 12.5 Flash Crash Test | `[ ]` | `[ ]` |

**Phase Status**: `[ ]` NOT STARTED

---

*Last verified: 2026-01-25*
