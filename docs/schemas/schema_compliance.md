# Schema: Compliance

## File Location
`schemas/compliance.py`

## Purpose
Pydantic models for regulatory compliance checking, violation tracking, and compliance reporting. Ensures platform and user activities comply with SEC, FINRA, and other regulatory requirements.

---

## Enums

### ViolationSeverity
**Compliance violation severity levels.**

| Value | Description |
|-------|-------------|
| `LOW` | Minor violation, informational |
| `MEDIUM` | Moderate violation requiring attention |
| `HIGH` | Serious violation requiring immediate action |
| `CRITICAL` | Severe violation with regulatory implications |

---

## Models

### ComplianceRule
**Definition of a compliance rule to be checked.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `rule_id` | `str` | *required* | Unique rule identifier | Primary key |
| `regulation` | `str` | *required* | Regulatory body: `SEC`, `FINRA`, etc. | Rule categorization |
| `rule_name` | `str` | *required* | Human-readable rule name | Display |
| `description` | `str` | *required* | Detailed rule description | Documentation |
| `rule_logic` | `Union[Dict, str]` | `{}` | Rule evaluation logic | Automated checking |

---

### ComplianceViolation
**A detected compliance violation.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `violation_id` | `str` | *required* | Unique violation identifier | Primary key |
| `rule_id` | `str` | *required* | Rule that was violated | Links to rule |
| `user_id` | `str` | *required* | User who triggered violation | Attribution |
| `severity` | `ViolationSeverity` | *required* | Violation severity | Prioritization |
| `description` | `str` | *required* | Violation details | Investigation context |
| `detected_date` | `datetime` | *required* | When violation was detected | Timeline |
| `resolved_date` | `Optional[datetime]` | `None` | When resolved | Resolution tracking |
| `status` | `str` | `"open"` | Status: `open`, `resolved`, `false_positive` | Workflow state |

---

### ComplianceReport
**Generated compliance report.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `report_id` | `str` | *required* | Unique report identifier | Primary key |
| `user_id` | `str` | *required* | Report subject | Scoping |
| `report_type` | `str` | *required* | Type: `regulatory`, `custom`, etc. | Report categorization |
| `period_start` | `datetime` | *required* | Report period start | Time window |
| `period_end` | `datetime` | *required* | Report period end | Time window |
| `violations` | `List[str]` | `[]` | Violation IDs in period | Violation listing |
| `generated_date` | `datetime` | *required* | Report generation time | Audit trail |

---

## Integration Points

| Service | Usage |
|---------|-------|
| `ComplianceEngine` | Rule evaluation |
| `ReportingService` | Report generation |
| `AlertService` | Violation notifications |
| `AuditService` | Compliance audit trails |

## Frontend Components
- Compliance dashboard (FrontendCompliance)
- Violation list with severity indicators
- Report generation wizard
