# Backend Service: Research (The Analyst Desk)

## Overview
The **Research Service** generates comprehensive research reports by combining qualitative analysis (SEC filings, moat scoring) with quantitative valuation (DCF models). It produces PDF-ready documents for portfolio analysis, company research, and market outlook.

## Core Components

### 1. Research Service (`research_service.py`)
- **Portfolio Reports**: Aggregates performance, risk metrics, and recommendations.
- **Company Research**: Integrates `FilingAnalyzer` (qualitative) and `DCFEngine` (quantitative) to produce actionable investment theses.
- **Caching**: Reports are cached for 365 days.

### 2. Report Generator (`report_generator.py`)
- Handles PDF export formatting.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used | Frontend Status |
| :--- | :--- | :--- | :--- |
| **Research Dashboard** | Company Deep Dive | `research_service.generate_company_research()` | **Implemented** (`ResearchWidget.jsx`) |
| **Reports Page** | PDF Export | `report_generator` | **Partially Implemented** |

## Usage Example

```python
from services.research.research_service import get_research_service

service = get_research_service()

report = await service.generate_company_research(
    user_id="user_01",
    symbol="NVDA"
)

print(f"Report: {report.title}")
print(f"Content: {report.content}")
print(f"Fair Value: ${report.data['fair_value']}")
```
