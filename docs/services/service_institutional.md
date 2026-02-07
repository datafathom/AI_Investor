# Backend Service: Institutional

## Overview
The **Institutional Service** is the platform's multi-tenant engine for financial advisors, banks, and family offices. It provides the infrastructure necessary to manage thousands of client relationships, configure **White-Label** branding for different organizations, and generate high-fidelity **Professional Reports**. It also features an integrated relationship graph (Neo4j) to track advisor-client hierarchies and advanced analytics for revenue forecasting and risk profiling.

## Core Components

### 1. Client & Organization Management (`institutional_service.py`)
The central orchestrator for institutional operations.
- **Advisor-Client Graph**: Utilizes Neo4j to maintain a persistent graph of which advisors manage which clients, enabling complex access control and organizational reporting.
- **White-Label Configuration**: Allows organizations to customize their logo, color palettes, and custom domains, ensuring the platform feels like a native institutional app.
- **Institutional Analytics**: Generates real-time metrics including **Fee Forecasts**, **Churn Probability**, and **KYC Risk Scores** to help advisors manage their business at scale.
- **Risk & Health Profiling**: Continuously monitors client accounts for institutional risk breaches (volatility/drawdown thresholds) and generates proactive health alerts.

### 2. Professional Reporting Terminal (`professional_tools_service.py`)
Handles the generation of high-fidelity documentation for allocators.
- **Advanced Report Engine**: Facilitates the creation of custom reports (e.g., GP/LP quarterly updates, performance audits) that are persisted in the platform's document cache.
- **Mandate Compliance**: Ensures that reports are generated contextually based on the specified institutional mandate and report type.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used |
| :--- | :--- | :--- |
| **Advisor Console** | Client Management Grid | `institutional_service.get_clients_for_advisor()` |
| **Advisor Console** | Revenue Forecast Chart | `institutional_service.get_revenue_forecast()` |
| **White Label Settings**| Branding Preview | `institutional_service.configure_white_label()` |
| **Client Detail** | Risk Profile Pulse | `institutional_service.get_client_risk_profile()` |
| **Reporting Terminal** | Report Generator Wizard | `professional_tools_service.generate_professional_report()` |
| **Document Hub** | e-Signature Tracker | `institutional_service.get_signature_status()` |

## Dependencies
- `neo4j`: Powers the institutional relationship graph.
- `services.system.cache_service`: Provides persistent storage for client data, configurations, and reports.
- `schemas.institutional`: Defines the core Pydantic models for `Client`, `WhiteLabelConfig`, and `ProfessionalReport`.

## Usage Examples

### Configuring White-Label Branding for a Family Office
```python
from services.institutional.institutional_service import get_institutional_service

inst_svc = get_institutional_service()

# Configure custom branding for 'Sovereign Wealth Management'
config = await inst_svc.configure_white_label(
    organization_id="org_sovereign_001",
    branding_name="Sovereign Wealth Portal",
    primary_color="#1a2b3c",
    logo_url="https://cdn.sovereign.net/logo.png"
)

print(f"Branding configured: {config.branding_name}")
```

### Generating an Institutional Revenue Forecast
```python
from services.institutional.institutional_service import InstitutionalService

svc = InstitutionalService()

# Fetch a 12-month revenue forecast for the entire advisory practice
forecast = await svc.get_revenue_forecast()

print(f"Current Monthly Fees: ${forecast['current_fees']:,.2f}")
print(f"Projected Annual Growth: {forecast['growth_rate']:.1%}")
for month in forecast['history'][-3:]:
    print(f"Month: {month['date']} | Revenue: ${month['amount']:,.2f}")
```

### Auditing a Client's Signature Compliance
```python
from services.institutional.institutional_service import get_institutional_service

inst_svc = get_institutional_service()

# Check which institutional onboarding docs are still pending
status = await inst_svc.get_signature_status(client_id="client_jdoe_123")

print(f"Compliance Completion: {status['completion_percentage']}%")
for doc in status['documents']:
    if doc['status'] == "Pending":
        print(f"MISSING: {doc['name']}")
```
