# Phase 107: Professional Role & Permission Isolation

> **Status**: `[x]` Completed  
> **Last Updated**: 2026-01-25  
> **Owner**: Compliance & Security Team

---

## 📋 Overview

**Description**: Implement Role-Based Access Control (RBAC) that strictly separates professional roles (Wealth Manager, Asset Manager, Financial Planner, Private Banker) with mutually exclusive permissions to prevent conflicts of interest.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON_2.txt - Phase 7 (Professional Role & Permission Isolation)

---

## 🎯 Sub-Deliverables

### 107.1 Mutually Exclusive Permission Sets `[x]`

**Acceptance Criteria**: Implement permission sets where certain roles cannot co-exist (e.g., an Asset Manager who earns SMA kickbacks cannot also serve as a fee-only Financial Planner for the same client).

#### Postgres Schema (Docker-compose: timescaledb service)

```sql
-- Role Definition Table
CREATE TABLE professional_roles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    role_code VARCHAR(50) NOT NULL UNIQUE,
    role_name VARCHAR(100) NOT NULL,
    role_category VARCHAR(50) NOT NULL,     -- FIDUCIARY, NON_FIDUCIARY
    fiduciary_standard BOOLEAN NOT NULL,
    
    -- Revenue Model
    can_earn_commissions BOOLEAN DEFAULT FALSE,
    can_earn_aum_fees BOOLEAN DEFAULT TRUE,
    can_earn_performance_fees BOOLEAN DEFAULT FALSE,
    
    -- Conflict Rules
    exclusive_with JSONB DEFAULT '[]',       -- List of incompatible role codes
    requires_disclosure JSONB DEFAULT '[]',  -- Required disclosures
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- User Role Assignments
CREATE TABLE user_role_assignments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id),
    role_id UUID NOT NULL REFERENCES professional_roles(id),
    client_id UUID,                          -- NULL for global, or specific client
    
    -- Assignment Status
    is_active BOOLEAN DEFAULT TRUE,
    assigned_at TIMESTAMPTZ DEFAULT NOW(),
    expires_at TIMESTAMPTZ,
    assigned_by UUID,
    
    -- Audit
    conflict_check_passed BOOLEAN NOT NULL,
    conflict_check_timestamp TIMESTAMPTZ DEFAULT NOW(),
    
    UNIQUE(user_id, role_id, client_id)
);

-- Permission Matrix
CREATE TABLE role_permissions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    role_id UUID NOT NULL REFERENCES professional_roles(id),
    permission_code VARCHAR(100) NOT NULL,
    permission_scope VARCHAR(50) NOT NULL,   -- PORTFOLIO, CLIENT, TRADE, REPORT
    can_create BOOLEAN DEFAULT FALSE,
    can_read BOOLEAN DEFAULT FALSE,
    can_update BOOLEAN DEFAULT FALSE,
    can_delete BOOLEAN DEFAULT FALSE,
    
    UNIQUE(role_id, permission_code)
);

-- Seed Data
INSERT INTO professional_roles (role_code, role_name, role_category, fiduciary_standard, can_earn_commissions, exclusive_with) VALUES
('WEALTH_MANAGER', 'Wealth Manager', 'FIDUCIARY', TRUE, FALSE, '["BROKER_DEALER"]'),
('ASSET_MANAGER', 'Asset Manager', 'NON_FIDUCIARY', FALSE, TRUE, '["FEE_ONLY_PLANNER"]'),
('FINANCIAL_PLANNER', 'Financial Planner', 'FIDUCIARY', TRUE, FALSE, '[]'),
('FEE_ONLY_PLANNER', 'Fee-Only Financial Planner', 'FIDUCIARY', TRUE, FALSE, '["ASSET_MANAGER", "BROKER_DEALER"]'),
('PRIVATE_BANKER', 'Private Banker', 'NON_FIDUCIARY', FALSE, TRUE, '[]'),
('BROKER_DEALER', 'Broker-Dealer', 'NON_FIDUCIARY', FALSE, TRUE, '["WEALTH_MANAGER", "FEE_ONLY_PLANNER"]');
```

#### Backend Implementation

```python
class RoleConflictValidator:
    """
    Validate that role assignments don't create conflicts of interest.
    
    Rules:
    1. No user can hold mutually exclusive roles for same client
    2. Commission-earning roles can't co-exist with fee-only roles
    3. Fiduciary roles require additional disclosures when combined
    """
    
    def validate_assignment(
        self, 
        user_id: UUID, 
        new_role: ProfessionalRole, 
        client_id: Optional[UUID]
    ) -> ValidationResult:
        """Check if new role assignment creates conflicts."""
        pass
    
    def get_excluded_roles(self, role: ProfessionalRole) -> list[ProfessionalRole]:
        """Get list of roles that cannot co-exist with given role."""
        pass
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Migration | `migrations/107_professional_roles.sql` | `[x]` |
| Role Model | `models/professional_role.py` | `[x]` |
| Assignment Model | `models/role_assignment.py` | `[x]` |
| Conflict Validator | `services/compliance/role_conflict_validator.py` | `[x]` |
| Permission Service | `services/auth/permission_service.py` | `[x]` |
| API Endpoint | `web/api/admin/roles.py` | `[x]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Role Manager | `frontend2/src/components/Admin/RoleManager.jsx` | `[x]` |
| Assignment Form | `frontend2/src/components/Admin/RoleAssignmentForm.jsx` | `[x]` |
| Conflict Warning | `frontend2/src/components/Alerts/RoleConflictWarning.jsx` | `[x]` |
| Permission Matrix View | `frontend2/src/components/Admin/PermissionMatrix.jsx` | `[x]` |
| usePermissions Hook | `frontend2/src/hooks/usePermissions.js` | `[x]` |
| PermissionContext | `frontend2/src/context/PermissionContext.jsx` | `[x]` |

#### Tests

| Test Type | File Path | Status |
|-----------|-----------|--------|
| Unit: Conflict Validator | `tests/unit/test_role_conflict_validator.py` | `[x]` |
| Unit: Permission Service | `tests/unit/test_permission_service.py` | `[x]` |
| Integration: Role API | `tests/integration/test_roles_api.py` | `[x]` |
| E2E: Role Assignment | `tests/e2e/test_role_assignment_ui.py` | `[x]` |

---

### 107.2 Neo4j Wealth Manager vs. Asset Manager Nodes `[x]`

**Acceptance Criteria**: Define Neo4j nodes for different professional types with relationship edges to clients, clearly separating holistic wealth managers from pure-play asset managers.

#### Neo4j Schema (Docker-compose: neo4j service)

```cypher
// Professional Type Nodes
CREATE CONSTRAINT professional_id IF NOT EXISTS FOR (p:PROFESSIONAL) REQUIRE p.id IS UNIQUE;

(:PROFESSIONAL:WEALTH_MANAGER {
    id: "uuid",
    name: "John Smith, CFP",
    fiduciary: true,
    registration_type: "RIA",
    sec_number: "123-45678",
    services: ["TAX_PLANNING", "ESTATE_PLANNING", "INSURANCE", "INVESTMENTS"]
})

(:PROFESSIONAL:ASSET_MANAGER {
    id: "uuid",
    name: "XYZ Capital Management",
    fiduciary: false,
    strategy: "GROWTH_EQUITY",
    aum: 500000000,
    services: ["INVESTMENT_MANAGEMENT"]
})

(:PROFESSIONAL:FINANCIAL_PLANNER {
    id: "uuid",
    name: "Jane Doe, CFP",
    fiduciary: true,
    fee_structure: "FEE_ONLY",
    hourly_rate: 300,
    services: ["BUDGETING", "529_PLANNING", "RETIREMENT_PLANNING"]
})

(:PROFESSIONAL:PRIVATE_BANKER {
    id: "uuid",
    name: "First National Private Bank",
    net_worth_minimum: 10000000,
    services: ["LENDING", "CUSTODY", "TAX_DEFERRAL", "PE_ACCESS"]
})

// Relationships
(:PROFESSIONAL)-[:ADVISES {
    start_date: date(),
    aum_under_management: 5000000,
    fee_type: "AUM_BASED",
    fee_percentage: 0.01
}]->(:CLIENT)

(:PROFESSIONAL)-[:CONFLICTS_WITH {
    reason: "Commission on recommended products",
    disclosure_required: true
}]->(:PROFESSIONAL)

(:PROFESSIONAL)-[:MANAGES]->(PORTFOLIO)
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Professional Graph Service | `services/neo4j/professional_graph.py` | `[x]` |
| Relationship Builder | `services/neo4j/prof_relationship_builder.py` | `[x]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Professional Network Graph | `frontend2/src/components/Neo4j/ProfessionalNetwork.jsx` | `[x]` |
| Advisor Comparison Card | `frontend2/src/components/Advisors/ComparisonCard.jsx` | `[x]` |

#### Tests

| Test Type | File Path | Status |
|-----------|-----------|--------|
| Unit: Graph Service | `tests/unit/test_professional_graph.py` | `[x]` |
| Integration: Neo4j | `tests/integration/test_professional_neo4j.py` | `[x]` |

---

### 107.3 SMA Kickback Conflict Scanner `[x]`

**Acceptance Criteria**: Build an automated scanner that detects when advisors recommend Separately Managed Accounts (SMAs) where they receive revenue sharing (kickbacks), requiring disclosure.

#### Backend Implementation

```python
class SMAKickbackScanner:
    """
    Detect potential kickback conflicts in SMA recommendations.
    
    Scans for:
    1. Revenue sharing agreements between advisor and SMA provider
    2. Higher-fee SMAs recommended over equivalent lower-fee options
    3. Proprietary products recommended without disclosure
    """
    
    def scan_recommendations(
        self, 
        advisor_id: UUID, 
        recommendations: list[SMRecommendation]
    ) -> list[ConflictFlag]:
        pass
    
    def calculate_kickback_amount(
        self, 
        sma_aum: Decimal, 
        revenue_share_pct: Decimal
    ) -> Decimal:
        """Calculate estimated kickback from SMA recommendation."""
        pass
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Kickback Scanner | `services/compliance/sma_kickback_scanner.py` | `[x]` |
| Revenue Share Tracker | `services/compliance/revenue_share_tracker.py` | `[x]` |
| Disclosure Generator | `services/compliance/disclosure_generator.py` | `[x]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Conflict Disclosure Modal | `frontend2/src/components/Modals/ConflictDisclosure.jsx` | `[x]` |
| SMA Comparison Tool | `frontend2/src/components/SMA/ComparisonTool.jsx` | `[x]` |

#### Tests

| Test Type | File Path | Status |
|-----------|-----------|--------|
| Unit: Kickback Scanner | `tests/unit/test_sma_kickback_scanner.py` | `[x]` |
| Unit: Disclosure Generator | `tests/unit/test_disclosure_generator.py` | `[x]` |
| Integration: Full Scan | `tests/integration/test_kickback_scan.py` | `[x]` |

---

### 107.4 Warehouse Advisor Fee Structure Mapping `[x]`

**Acceptance Criteria**: Track and map fee structures for wirehouse advisors including grid payouts, platform fees, and product-specific compensation to identify conflicts.

| Component | File Path | Status |
|-----------|-----------|--------|
| Fee Structure Mapper | `services/compliance/fee_structure_mapper.py` | `[x]` |
| Grid Payout Calculator | `services/compensation/grid_calculator.py` | `[x]` |
| Platform Fee Tracker | `services/compliance/platform_fees.py` | `[x]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Fee Breakdown Chart | `frontend2/src/components/Charts/FeeBreakdownChart.jsx` | `[x]` |
| Conflict Heat Map | `frontend2/src/components/Charts/ConflictHeatMap.jsx` | `[x]` |

#### Tests

| Test Type | File Path | Status |
|-----------|-----------|--------|
| Unit: Fee Mapper | `tests/unit/test_fee_structure_mapper.py` | `[x]` |
| Unit: Grid Calculator | `tests/unit/test_grid_calculator.py` | `[x]` |

---

### 107.5 Professional Role Competence Validator `[x]`

**Acceptance Criteria**: Validate that professionals have required certifications and registrations for their assigned roles (CFP for financial planners, Series 65 for RIAs, etc.).

#### Backend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Competence Validator | `services/compliance/competence_validator.py` | `[x]` |
| Certification Tracker | `services/compliance/certification_tracker.py` | `[x]` |
| Renewal Reminder Service | `services/notifications/renewal_reminders.py` | `[x]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Certification Badge | `frontend2/src/components/Badges/CertificationBadge.jsx` | `[x]` |
| Credentials Panel | `frontend2/src/components/Professional/CredentialsPanel.jsx` | `[x]` |

#### Tests

| Test Type | File Path | Status |
|-----------|-----------|--------|
| Unit: Competence Validator | `tests/unit/test_competence_validator.py` | `[x]` |
| Unit: Certification Tracker | `tests/unit/test_certification_tracker.py` | `[x]` |

---

## 📊 Phase Completion Summary

| Deliverable | Status | E2E Verified |
|-------------|--------|--------------|
| 107.1 Permission Sets | `[x]` | `[ ]` |
| 107.2 Neo4j Professional Nodes | `[x]` | `[ ]` |
| 107.3 SMA Kickback Scanner | `[x]` | `[ ]` |
| 107.4 Fee Structure Mapping | `[x]` | `[ ]` |
| 107.5 Competence Validator | `[x]` | `[ ]` |

**Phase Status**: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py roles list` | List all professional roles | `[x]` |
| `python cli.py roles assign <user> <role>` | Assign role | `[x]` |
| `python cli.py conflicts scan <advisor_id>` | Scan for conflicts | `[x]` |
| `python cli.py credentials check <user>` | Check credentials | `[x]` |

---

*Last verified: 2026-01-25*
