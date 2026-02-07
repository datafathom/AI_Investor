# Schema: Professional Role

## File Location
`schemas/professional_role.py`

## Purpose
Pydantic models for professional roles and assignments within the advisory structure including role definitions, fiduciary standards, and compensation configurations.

---

## Models

### ProfessionalRoleBase
**Professional role definition.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `role_code` | `str` | *required* | Role identifier: `IAR`, `RR`, `CFA` | Role type |
| `role_name` | `str` | *required* | Display name | Display |
| `fiduciary_standard` | `bool` | `False` | Subject to fiduciary duty | Compliance |
| `can_earn_commission` | `bool` | `False` | Commission eligible | Compensation |
| `can_charge_fees` | `bool` | `True` | Fee eligible | Compensation |
| `required_licenses` | `List[str]` | `[]` | Required licenses | Compliance |
| `supervision_required` | `bool` | `True` | Needs supervision | Oversight |

---

### ProfessionalRole
**Full professional role record.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `id` | `UUID` | `uuid4()` | Unique identifier | Primary key |
| `is_active` | `bool` | `True` | Whether role is active | Status |
| `created_at` | `datetime` | `datetime.now()` | Creation timestamp | Audit |

---

### RoleAssignmentBase
**Assignment of role to individual.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `user_id` | `UUID` | *required* | Assigned user | Individual |
| `role_id` | `UUID` | *required* | Assigned role | Role link |
| `effective_date` | `date` | *required* | Assignment start | Timing |
| `expiration_date` | `Optional[date]` | `None` | Assignment end | Timing |
| `supervising_principal_id` | `Optional[UUID]` | `None` | Supervisor | Oversight |

---

### RoleAssignment
**Full role assignment record.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `id` | `UUID` | `uuid4()` | Unique identifier | Primary key |
| `status` | `str` | `"ACTIVE"` | Status: `ACTIVE`, `SUSPENDED`, `TERMINATED` | Lifecycle |
| `created_at` | `datetime` | `datetime.now()` | Creation timestamp | Audit |

---

## Integration Points

| Service | Usage |
|---------|-------|
| `ProfessionalRoleService` | Role management |
| `ComplianceService` | License verification |
| `SupervisionService` | Oversight tracking |
