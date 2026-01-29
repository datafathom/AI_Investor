# Implementation Plan: Sprint 2 - Institutional Logic

## Goal
Empower advisors with functional onboarding workflows, revenue forecasting, and real-time client risk assessment.

## 1. Institutional Core Logic
### 1.1 Hierarchical RBAC
- **Logic**: Extend `authStore` to handle `role: advisor` vs `role: super_admin`. 
- **Persistence**: Store organizational parent/child relationships in Neo4j.

### 1.2 Advisor Onboarding Wizard
- **Files**: `frontend2/src/components/Institutional/OnboardingWizard.jsx`
- **Steps**:
    1. **Identity**: Basic KYC collection.
    2. **Compliance**: Multi-jurisdiction check.
    3. **Funding**: Connect Plaid/Stripe.
    4. **Strategy**: Select AI Agent allocation.
    5. **Finalize**: Generate legal engagement PDF.

## 2. Sprint 2 Widgets (Workflows & Analytics)
| Widget | Purpose | Technical Logic |
|--------|---------|-----------------|
| `FeeRevenueForecast` | AUM fee simulator | Calculates `AUM * BPS` with tiered fallback logic from the backend. |
| `ClientRetentionAI` | Churn prediction | Displays "Health Score" from the backend ML model. |
| `DocSignaturePulse` | Legal tracking | Polls the `Documents` API for e-signature status. |
| `AssetAllocationWheel` | Rebalancing UI | Visualizes deviation between target and current allocation. |
| `AdvisorCommissionTracker` | Earnings view | Aggregates successful fee collections for the current user. |
| `KycRiskGauge` | Compliance flags | Displays "Red/Yellow/Green" status based on SAR history. |

## 3. Acceptance Criteria
- [ ] **Onboarding**: A new client can be created, funded, and assigned an agent in a single session.
- [ ] **RBAC**: An "Advisor" cannot see clients belonging to a different advisor in the same organization.
- [ ] **Analytics**: `FeeRevenueForecast` matches the backend calculation for a $10M portfolio at 1.25%.
- [ ] **UI**: `AssetAllocationWheel` allows dragging weightings and triggers a `calculate_drift` request.

## 4. Testing & Code Coverage
- **Unit Tests**:
    - `institutionalStore.test.js`: Verify client filtering and calculation logic.
    - `OnboardingWizard.jsx`: Snapshots for all 5 steps.
- **E2E Tests**:
    - `test_client_lifecycle.py`: Simulate a full onboarding flow from login to "Strategy Assigned".
- **Targets**:
    - 95% coverage for financial calculation logic.
    - 80% coverage for the 6 new widgets.
