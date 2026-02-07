# Backend Service: International

## Overview
The **International Service** is the platform's geopolitical and cross-border risk engine. It is designed to navigate the structural complexities of global markets, focusing on the identification of **State-Owned Enterprises (SOEs)** and the monitoring of **Index Skew** in international markets. It provides institutional-grade risk ratings for emerging and developed market exposures, ensuring that portfolios aren't silently concentrated in sanctioned regions or single-company dominated indices.

## Core Components

### 1. International Concentration Analyzer (`concentration_analyzer.py`)
Monitors structural skews within global equity indices.
- **Index Skew Detection**: Automatically flags international indices where a single ticker holds >20% weight (e.g., TSMC's dominance in the Taiwan market). This prevents the "Passive Concentration" trap where an investor believes they are diversified across a country but are actually highly leveraged to a single firm's idiosyncratic risk.

### 2. State-Owned Enterprise (SOE) Classifier (`soe_classifier.py`)
The geopolitical risk layer for global mandates.
- **Ownership Analysis**: Classifies companies as SOEs based on government ownership thresholds (>50%) or the presence of strategic sovereign entities (e.g., SASAC, Temasek, Mubadala).
- **Geopolitical Risk Rating**: Assigns risk levels based on the entity's status and its region. SOEs in sanctioned or high-friction regions (e.g., RU, CN) are flagged as "CRITICAL" or "HIGH" risk, while those in stable partner regions are rated "LOW."

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used |
| :--- | :--- | :--- |
| **Geopolitical Station**| Global SOE Exposure Map | `soe_classifier.classify_soe()` |
| **Geopolitical Station**| Country Skew Alert Feed | `intl_concentration_analyzer.analyze_index_skew()` |
| **Portfolio Detail** | Regulatory Risk Rating Card| `soe_classifier.get_risk_rating()` |
| **Strategist Station** | Sanctioned Entity Ledger | `soe_classifier.py` (Risk logic) |

## Dependencies
- `logging`: Records the discovery of significant index skews and high-risk SOE classifications for the audit trail.

## Usage Examples

### Detecting a Structural Skew in an Emerging Market Index
```python
from services.international.concentration_analyzer import IntlConcentrationAnalyzer

analyzer = IntlConcentrationAnalyzer()

# Mock holdings for the Taiwan Index
taiwan_holdings = [
    {"ticker": "TSMC", "weight": 0.28}, # 28% weight
    {"ticker": "HON_HAI", "weight": 0.05},
    {"ticker": "MEDIATEK", "weight": 0.04}
]

skew_report = analyzer.analyze_index_skew(index_name="Taiwan_TAIEX", holdings=taiwan_holdings)

if skew_report['is_skewed']:
    print(f"Index {skew_report['index_name']} is SKEWED.")
    print(f"Top Holding {skew_report['top_ticker']} accounts for {skew_report['top_weight']:.1%} of index.")
```

### Classifying an Entity as a State-Owned Risk
```python
from services.international.soe_classifier import SOEClassifier

classifier = SOEClassifier()

# Classify an entity controlled by SASAC (State-owned Assets Supervision and Administration Commission)
is_soe = classifier.classify_soe(ownership_pct=0.15, controlling_entity="SASAC")

risk_rating = classifier.get_risk_rating(is_soe=is_soe, country_code="CN")

print(f"SOE Classification: {is_soe}")
print(f"Geopolitical Risk Rating: {risk_rating}")
```
