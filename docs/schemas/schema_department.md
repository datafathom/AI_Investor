# Schema: Department

## File Location
`schemas/department.py`

## Purpose
Pydantic models for the organizational department structure within the AI Investor platform. Represents the 14-department system with agents, metrics, and operational status. Used for the Mission Control dashboard and agent workforce management.

---

## Models

### AgentRead
**Read model for agent within a department.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `agent_id` | `str` | *required* | Unique agent identifier (e.g., `trader.4.1`) | Agent tracking |
| `role` | `Optional[str]` | `None` | Agent's assigned role | Role identification |
| `status` | `str` | *required* | Agent status: `ACTIVE`, `IDLE`, `ERROR` | Operational monitoring |

---

### DepartmentRead
**Read model for department information.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `id` | `int` | *required* | Department ID | Primary key |
| `name` | `str` | *required* | Department name (e.g., `Quant Research`) | Display |
| `slug` | `str` | *required* | URL-friendly identifier | Routing |
| `quadrant` | `str` | *required* | Mission Control quadrant assignment | UI layout |
| `status` | `str` | *required* | Department status: `NOMINAL`, `WARNING`, `CRITICAL` | Health monitoring |
| `metrics` | `Dict[str, float]` | *required* | Key performance metrics | Dashboard display |
| `agents` | `List[AgentRead]` | *required* | Agents in department | Agent management |
| `last_update` | `Optional[str]` | `None` | Last activity timestamp | Freshness |

**Config:** `from_attributes = True` - Enables ORM mode.

---

### DepartmentUpdate
**Update model for department properties.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `status` | `Optional[str]` | `None` | New department status | Status update |
| `primary_metric_value` | `Optional[float]` | `None` | Updated primary metric | Metric refresh |

---

## Integration Points

| Service | Usage |
|---------|-------|
| `DepartmentService` | Department management |
| `AgentOrchestrationService` | Agent lifecycle |
| `MetricsService` | Department metrics collection |
| `MissionControlService` | Dashboard aggregation |

## Related Database
- `schemas/postgres/030_departments.sql` - Department table

## Frontend Components
- Mission Control dashboard
- Department status cards
- Agent health indicators
