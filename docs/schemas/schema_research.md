# Schema: Research

## File Location
`schemas/research.py`

## Purpose
Pydantic models for research reports and templates including analyst reports, investment theses, and structured research content.

---

## Enums

### ReportType
**Types of research reports.**

| Value | Description |
|-------|-------------|
| `EQUITY` | Stock analysis |
| `SECTOR` | Sector overview |
| `MACRO` | Macroeconomic analysis |
| `THEMATIC` | Thematic investment ideas |

---

### ReportStatus
**Report publication status.**

| Value | Description |
|-------|-------------|
| `DRAFT` | In progress |
| `REVIEW` | Under review |
| `PUBLISHED` | Live |
| `ARCHIVED` | Historical |

---

## Models

### ResearchReport
**Research report document.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `report_id` | `str` | *required* | Unique report ID | Primary key |
| `author_id` | `str` | *required* | Report author | Attribution |
| `title` | `str` | *required* | Report title | Display |
| `report_type` | `ReportType` | *required* | Report category | Classification |
| `symbols` | `List[str]` | `[]` | Covered securities | Linking |
| `summary` | `str` | *required* | Executive summary | Preview |
| `content` | `Dict` | *required* | Structured content | Report body |
| `charts` | `List[Dict]` | `[]` | Embedded charts | Visualization |
| `status` | `ReportStatus` | `DRAFT` | Publication status | Workflow |
| `rating` | `Optional[str]` | `None` | Rating: `BUY`, `HOLD`, `SELL` | Recommendation |
| `target_price` | `Optional[float]` | `None` | Price target | Valuation |
| `created_date` | `datetime` | *required* | Creation timestamp | Audit |
| `published_date` | `Optional[datetime]` | `None` | Publication date | Timing |
| `updated_date` | `datetime` | *required* | Last update | Freshness |

---

### ReportTemplate
**Template for report creation.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `template_id` | `str` | *required* | Template identifier | Primary key |
| `template_name` | `str` | *required* | Template name | Display |
| `report_type` | `ReportType` | *required* | Target report type | Matching |
| `sections` | `List[Dict]` | *required* | Section definitions | Structure |
| `default_charts` | `List[str]` | `[]` | Default chart types | Guidance |
| `created_date` | `datetime` | *required* | Creation timestamp | Audit |

---

## Integration Points

| Service | Usage |
|---------|-------|
| `ResearchService` | Report management |
| `PublishingService` | Report distribution |
| `ChartingService` | Chart generation |

## Frontend Components
- Research portal (FrontendResearch)
- Report editor
- Template manager
