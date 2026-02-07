# Backend Service: Legal

## Overview
The **Legal Service** is the platform's multi-layered defensive and structural infrastructure. It provides institutional-grade "Legal-as-a-Service" (LaaS) for UHNW families and family offices. The service automates the analysis of complex contracts for dangerous clauses, tracks residency thresholds to prevent "Accidental Tax Residency," monitors global court dockets for litigation risks, and resolves complex ownership hierarchies across trusts, LLCs, and individualholdings.

## Core Components

### 1. Contract Analysis Engine (`contract_analyzer.py`)
Autonomous review of legal documents to flag structural risks.
- **Risk Scoring**: Uses keyword analysis and intent mapping to score contracts based on aggressive indemnification, arbitration, or perpetual exclusivity clauses.
- **Clause Flagging**: Automatically identifies and extracts "High-Risk" text, providing a summary and recommendation (Approve/Reject) for legal counsel review.

### 2. Citizenship & Mobility Hedging (`citizenship_hedging_svc.py`)
Stewardship of "Plan B" residency and visa compliance.
- **Residency Threshold Tracking**: Monitors days spent in specific jurisdictions to ensure compliance with the 183-day rule, preventing unintended tax residency recognition.
- **Visa Compliance Audit**: Validates the holding period and investment status of "Golden Visa" or residency-by-investment assets, tracking the progress towards citizenship eligibility.

### 3. Litigation Radar (`litigation_radar.py`)
Proactive monitoring for legal threats.
- **Docket Scraping**: Interfaces with court dockets (e.g., PACER/CourtListener) to monitor filings involving family members, trusts, or holding companies.
- **Jurisdictional Risk Profiling**: Evaluates the legal protection levels of different jurisdictions (e.g., Nevada, Cook Islands) to assist in asset protection planning.

### 4. Ownership & Entity Resolver (`ownership_resolver.py`)
Orchestrates the legal and tax status of diverse account types.
- **Tax Entity Mapping**: Automatically resolves whether an account/asset is owned by an individual (pass-through), a revocable/irrevocable trust, or a business entity. It identifies which structures require separate tax filings and which are legally distinct layers.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used |
| :--- | :--- | :--- |
| **Legal Command** | Contract Risk Scorer | `contract_analysis_service.analyze_document()` |
| **Legal Command** | Global Residency Pulse | `citizenship_hedging_svc.track_residency_threshold()` |
| **Legal Command** | Litigation Docket Monitor | `litigation_radar_service.scan_dockets()` |
| **Trust Station** | Entity Ownership Graph | `legal_ownership_resolver.resolve_tax_entity()` |
| **Governance Hub** | Golden Visa Vesting Progress| `citizenship_hedging_svc.validate_visa_investment_hold()`|

## Dependencies
- `hashlib / json`: Used by internal metadata and archival layers.
- `datetime / date`: Tracks residency thresholds and visa investment timers.
- `logging`: Records structural alerts such as "Risk of Tax Recognition" or "Critical Litigation Found."

## Usage Examples

### Running an Autonomous Contract Risk Audit
```python
from services.legal.contract_analyzer import ContractAnalysisService

analyzer = ContractAnalysisService()

# Run an AI audit on a new Private Equity Subscription Agreement
audit = analyzer.analyze_document(file_path="/vault/contracts/PE_Sub_Agreement.pdf")

print(f"Risk Score: {audit['risk_score']}/100")
print(f"Recommendation: {audit['assessment']}")
for clause in audit['flagged_clauses']:
    print(f"FLAG: {clause['clause']} is {clause['risk']} risk")
```

### Tracking Global Residency for Tax Optimization
```python
from services.legal.citizenship_hedging_svc import CitizenshipHedgingService

hedging_svc = CitizenshipHedgingService()

# Check threshold for the UK after a 120-day summer residence
threshold = hedging_svc.track_residency_threshold(country_code="UK", days_present=120)

print(f"Status in {threshold['country']}: {threshold['status']}")
print(f"Days remaining until Tax Residency: {threshold['days_remaining_to_resident']}")
```

### Resolving Account Ownership for Tax Reporting
```python
from services.legal.ownership_resolver import LegalOwnershipResolver

resolver = LegalOwnershipResolver()

# Resolve status for an Irrevocable Asset Protection Trust
res = resolver.resolve_tax_entity(account_type="IRREVOCABLE_TRUST")

print(f"Legal Entity Type: {res['entity_type']}")
print(f"Requires Separate Tax Return: {res['requires_separate_tax_filing']}")
```
