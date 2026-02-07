# Backend Service: External

## Overview
The **External Service** acts as the platform's universal bridge to the outside world. It provides specialized **Adapters** that integrate niche alternative asset classes—such as luxury watches and blue-chip art—into the platform's unified portfolio view. Additionally, it integrates with institutional ecosystems like **Salesforce** to synchronize high-fidelity relationship data and deal-sourcing signals.

## Core Components

### 1. Alternative Asset Adapters
- **Chrono24 Adapter (`chrono24_adapter.py`)**: A valuation feed for the luxury watch market. It tracks pricing for elite references (e.g., Rolex, Patek Philippe) to ensure that a client's physical "Wrist Portfolio" is marked-to-market alongside their liquid assets.
- **Masterworks Adapter (`masterworks_adapter.py`)**: Connects to the fractional art secondary market. It fetches current appraisal values and market pricing for high-value artwork held by the platform's UHNW clients.

### 2. Enterprise CRM Integration
- **Salesforce Adapter (`salesforce_adapter.py`)**: The data bridge for institutional relationships.
    - **Contact Synchronization**: Automatically pulls contacts tagged as "Institutional" or "UHNW" into the platform's internal network graph.
    - **Deal Signal Extraction**: Scans activity logs for keywords like "Pitch Deck" or "Investment Opportunity" to proactively flag potential deal flow for the internal investment committee.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used |
| :--- | :--- | :--- |
| **Alternative Assets** | Watch Collection List | `chrono24_adapter.fetch_watch_value()` |
| **Alternative Assets** | Art Valuation Card | `masterworks_adapter.fetch_artwork_value()` |
| **Network Hub** | Salesforce Sync Panel | `salesforce_adapter.sync_contacts()` |
| **Deal Sourcing** | CRM Signal Feed | `salesforce_adapter.fetch_deal_signal()` |
| **Portfolio Detail** | Physical Asset Breakdown | All Alternative Adapters |

## Dependencies
- `uuid`: Used for mapping external contacts and assets to internal platform identifiers.
- `random`: Utilized in mock adapters as "Valuation Perturbators" (simulating market fluctuations in testing environments).

## Usage Examples

### Sourcing a Deal Signal from Salesforce
```python
from services.external.salesforce_adapter import SalesforceAdapter

sf = SalesforceAdapter()

# Scan for activity from a high-priority institutional contact
signal = sf.fetch_deal_signal(contact_name="Sarah Venture")

if signal['signal_strength'] == "HIGH":
    print(f"ALERT: Significant deal signal detected from {signal['contact']}")
    print(f"Recent Activity: {signal['recent_activity']}")
```

### Valuation of a Luxury Asset
```python
from services.external.chrono24_adapter import Chrono24Adapter

chrono = Chrono24Adapter()

# Fetch latest valuation for a specific reference
valuation = chrono.fetch_watch_value(brand="Patek Philippe", reference="5711/1A")

print(f"Current Market Value: ${valuation['market_value_usd']:,.2f}")
print(f"Source: {valuation['source']} | Condition: {valuation['condition_grade']}")
```
