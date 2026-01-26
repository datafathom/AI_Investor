# Phase 196: Rule 144(a) & Promo-Volume Anomaly Detector

> **Status**: `[ ]` Not Started  
> **Last Updated**: 2026-01-25  
> **Owner**: Compliance Team

---

## 📋 Overview

**Description**: Advanced detection of "Pump and Dump" schemes targeting Rule 144(a) private placements or micro-cap stocks held by clients. Detect if a stock is experiencing "Promo Volume" (fake paid endorsements) which often precedes a crash.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON_2.txt - Epoch X Phase 16

---

## 🎯 Sub-Deliverables

### 196.1 Anomaly Detection Algorithm (Volume/Price Divergence) `[ ]`

**Acceptance Criteria**: Detect when price rises on low/declining volume, or volume spikes without news. Classic sign of manipulation.

```python
class AnomalyDetector:
    """
    Detect manipulation signatures.
    """
    def check_divergence(self, price_series: Series, vol_series: Series) -> AnomalyScore:
        correlation = price_series.corr(vol_series)
        if price_series.trend == "UP" and vol_series.trend == "DOWN":
            return AnomalyScore(score=85, reason="Price/Vol Divergence")
        return AnomalyScore(score=10)
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Detector Engine | `services/market/anomaly_detector.py` | `[ ]` |

---

### 196.2 Social Botnet Activity Monitor `[ ]`

**Acceptance Criteria**: Scrape Twitter/Reddit/$CASHTAGS. Detect bot-like activity (1000 accounts tweeting the same message) promoting a specific ticker.

| Component | File Path | Status |
|-----------|-----------|--------|
| Bot Monitor | `services/social/bot_monitor.py` | `[ ]` |

---

### 196.3 News Sentiment vs. Price Action Correlation `[ ]`

**Acceptance Criteria**: If price skyrockets with Neutral or Negative news, flag as anomalous.

| Component | File Path | Status |
|-----------|-----------|--------|
| Sentiment Correlator | `services/analysis/sentiment_check.py` | `[ ]` |

---

### 196.4 Restricted Stock Legitimacy Verifier `[ ]`

**Acceptance Criteria**: Verify the "Safe Harbor" status of 144(a) securities. Ensure valid opinion letters from counsel exist before removing legends.

| Component | File Path | Status |
|-----------|-----------|--------|
| Legend Remover | `services/compliance/legend_check.py` | `[ ]` |

---

### 196.5 "Pump & Dump" Pre-Crash Warning System `[ ]`

**Acceptance Criteria**: Alert system. "Probability of Dump: 80%". Advise selling into the pump.

| Component | File Path | Status |
|-----------|-----------|--------|
| Crash Warning | `services/alerts/pump_dump.py` | `[ ]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Manipulation Gauge | `frontend2/src/components/Compliance/ManipGauge.jsx` | `[ ]` |
| Promo Feed | `frontend2/src/components/Social/PromoFeed.jsx` | `[ ]` |

---

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py scan-anomalies` | Check watchlist | `[ ]` |
| `python cli.py check-bots <ticker>` | Analyze social output | `[ ]` |

---

*Last verified: 2026-01-25*
