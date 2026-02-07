# Schema: Enterprise

## File Location
`schemas/enterprise.py`

## Purpose
Pydantic models for enterprise features including organizations, teams, and shared resources. Supports multi-user collaboration for institutional clients and advisory firms.

---

## Enums

### TeamRole
**Roles within a team.**

| Value | Description |
|-------|-------------|
| `ADMIN` | Full administrative access |
| `MANAGER` | Team management capabilities |
| `ANALYST` | Analysis and reporting access |
| `VIEWER` | Read-only access |

---

## Models

### Organization
**Top-level organization entity.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `organization_id` | `str` | *required* | Unique organization identifier | Primary key |
| `name` | `str` | *required* | Organization name | Display |
| `parent_organization_id` | `Optional[str]` | `None` | Parent org for hierarchy | Nested organizations |
| `created_date` | `datetime` | *required* | Creation timestamp | Audit |
| `updated_date` | `datetime` | *required* | Last modification | Change tracking |

---

### Team
**Team within an organization.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `team_id` | `str` | *required* | Unique team identifier | Primary key |
| `organization_id` | `str` | *required* | Parent organization | Hierarchy |
| `team_name` | `str` | *required* | Team name | Display |
| `members` | `List[Dict]` | `[]` | Member list: `[{user_id, role}]` | Access control |
| `created_date` | `datetime` | *required* | Creation timestamp | Audit |
| `updated_date` | `datetime` | *required* | Last modification | Change tracking |

---

### SharedResource
**Resource shared among team members.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `resource_id` | `str` | *required* | Unique resource identifier | Primary key |
| `resource_type` | `str` | *required* | Type: `portfolio`, `report`, `watchlist` | Resource classification |
| `team_id` | `str` | *required* | Owning team | Access scope |
| `permissions` | `Dict` | `{}` | User permissions: `{user_id: level}` | Access control |
| `created_date` | `datetime` | *required* | Creation timestamp | Audit |
| `updated_date` | `datetime` | *required* | Last modification | Change tracking |

---

## Integration Points

| Service | Usage |
|---------|-------|
| `EnterpriseService` | Organization/team management |
| `MultiUserService` | Shared resource management |
| `AuthorizationService` | Permission enforcement |

## Frontend Components
- Enterprise dashboard (FrontendEnterprise)
- Team management interface
- Resource sharing controls
