# Backend Service: Enterprise

## Overview
The **Enterprise Service** provides the structural framework for institutional and B2B clients. It enables the creation of complex organizational hierarchies, multi-level team management, and granular resource sharing. This service is the foundation for collaborative wealth management, allowing multiple stakeholders (e.g., family members, advisors, and trustees) to securely interact with shared portfolios and reports.

## Core Components

### 1. Enterprise Management Engine (`enterprise_service.py`)
Handles the "bones" of corporate and family office structures.
- **Organizational Hierarchies**: Supports nested organizations, allowing a parent holding company to manage multiple sub-entities or family branches.
- **Team Management**: Facilitates the creation of functional teams (e.g., "Investment Committee," "Tax Planning Team") within an organization.
- **Role-Based Membership**: Maps users to teams with specific roles (e.g., `Admin`, `Member`, `Contributor`), integrated with the platform's RBAC (Role-Based Access Control) system.

### 2. Multi-User Collaboration (`multi_user_service.py`)
The sharing and permissions layer for institutional assets.
- **Shared Resources**: Enables portfolios, custom reports, and dashboards to be shared across an entire team or organization.
- **Granular Permissions**: Supports fine-grained access control (Read/Write/Execute) on a per-resource, per-team basis.
- **Activity Logging**: (Inferred) Tracks modifications to shared resources to maintain a collaborative audit trail.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used |
| :--- | :--- | :--- |
| **Enterprise Console** | Organization Tree | `enterprise_service.create_organization()` |
| **Enterprise Console** | Team Member List | `enterprise_service.add_team_member()` |
| **Portfolio Terminal** | Share Portfolio Modal | `multi_user_service.share_resource()` |
| **Resource Library** | Shared Documents Grid | `multi_user_service.get_shared_resources()` |
| **Settings / Roles** | Permission Matrix | `enterprise_service.add_team_member()` (Role management) |

## Dependencies
- `schemas.enterprise`: Defines the Pydantic models for `Organization`, `Team`, and `SharedResource`.
- `services.system.cache_service`: Provides long-term persistence for organizational structures and sharing records.
- `RBACService`: (Integration) Enforces the actual access boundaries defined by enterprise roles.

## Usage Examples

### Building a Family Office Hierarchy
```python
from services.enterprise.enterprise_service import get_enterprise_service

enterprise = get_enterprise_service()

# Create a master Family Office org
mfo = await enterprise.create_organization(name="East-West Multi-Family Office")

# Create a specialized Investment Team
inv_team = await enterprise.create_team(
    organization_id=mfo.organization_id, 
    team_name="Investment Committee"
)

# Add a Senior Advisor
await enterprise.add_team_member(
    team_id=inv_team.team_id,
    user_id="user_advisor_123",
    role="SENIOR_ADVISOR"
)
```

### Sharing a Portfolio with a Team
```python
from services.enterprise.multi_user_service import get_multi_user_service

mu_svc = get_multi_user_service()

# Share a specific portfolio with "ReadOnly" permissions for the whole team
shared_ref = await mu_svc.share_resource(
    resource_type="portfolio",
    resource_id="port_aggress_growth_01",
    team_id="team_family_office_A",
    permissions={"read": True, "write": False}
)

print(f"Resource shared successfully. ID: {shared_ref.resource_id}")
```
