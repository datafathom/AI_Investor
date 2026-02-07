# Backend Service: Impact

## Overview
The **Impact Service** is the platform's verifiable philanthropy and ESG infrastructure. It transforms charitable giving into a high-fidelity, data-driven operation. By utilizing **Impact Oracles** for off-chain verification and **Smart Contracts** for automated grant issuance, it ensures that philanthropic capital is deployed only when real-world KPIs are met. It also features a **Quadratic Voting** system for family councils to democratically prioritize impact initiatives.

## Core Components

### 1. Impact Verification Oracle (`impact_oracle.py`)
The platform's truth layer for real-world social impact.
- **KPI Verification**: Integrates with off-chain data sources—including satellite imagery, IoT sensors, and government APIs—to confirm that social or environmental milestones (e.g., carbon recapture, school enrollment) have been achieved.
- **Confidence Scoring**: Assigns a confidence metric to verified events based on the reliability and redundancy of the source data.

### 2. Grant Smart Contracts (`grant_smart_contract.py`)
Automates the lifecycle of philanthropic funding.
- **On-Chain Proposals**: Creates formal grant proposals on public or private ledgers (Ethereum/Solana), binding the fund release to specific verifiable KPIs.
- **Conditional Fund Release**: Automatically triggers the disbursement of funds once the Impact Oracle confirms KPI achievement, eliminating administrative delays and ensuring transparency.

### 3. Quadratic Voting Service (`voting_svc.py`)
Empowers democratic decision-making within Family Councils.
- **Quadratic Logic**: Implements a voting mechanism where the cost of power increases by the square of the votes (Cost = Power²). This encourages members to put more weight on initiatives they are truly passionate about while preventing a single dominant member from controlling the entire philanthropic budget.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used |
| :--- | :--- | :--- |
| **Impact Tracker** | KPI Verification Pulse | `impact_oracle.verify_kpi()` |
| **Philanthropy Hub** | Grant Creation Wizard | `grant_smart_contract.propose_grant()` |
| **Council Station** | Quadratic Voting Terminal | `voting_service.cast_vote()` |
| **Philanthropy Hub** | Grant Settlement Ledger | `grant_smart_contract.release_funds()` |
| **Impact Tracker** | Oracle Source Timeline | `impact_oracle.verified_sources` |

## Dependencies
- `math`: Used for calculating vote power (square roots) in the quadratic voting engine.
- `logging`: Records oracle verifications, grant proposals, and voting results for auditability.

## Usage Examples

### Verifying a Philanthropic KPI via Oracle
```python
from services.impact.impact_oracle import ImpactOracleService

oracle = ImpactOracleService()

# Verify if a clean water project KPI (ID: CW_202) has been met
result = oracle.verify_kpi(kpi_id="CW_202", kpi_type="Water_Purity_IoT")

if result['verified']:
    print(f"KPI Verified via {result['source']} with {result['confidence']:.1%} confidence.")
else:
    print("KPI Verification Failed. Grant funds held.")
```

### Casting a Quadratic Vote
```python
from services.impact.voting_svc import VotingService

voting = VotingService()

# Alice spends 25 credits to get 5 votes on "AI Safety Research" (Prop ID: 2)
vote_result = voting.cast_vote(user="Alice", proposal_id=2, credits_spent=25)

print(f"Votes Cast: {vote_result['votes_cast']}")
print(f"Remaining Governance Credits: {vote_result['remaining_credits']}")
```
