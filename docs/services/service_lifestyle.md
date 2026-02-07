# Backend Service: Lifestyle (Social Class Maintenance)

## Overview
The **Lifestyle Service** (internally known as **SCM - Social Class Maintenance**) manages the platform's luxury expenditure and inter-generational stability infrastructure. It goes beyond simple expense tracking by modeling **Personal Inflation (CLEW Index)**—the divergence of luxury goods/services from standard CPI—and projecting the impact of family growth on wealth-per-head across multiple generations. Its primary objective is to quantify and mitigate the risk of "Social Class Dilution."

## Core Components

### 1. CLEW Index & Personal Inflation (`scm_service.py`)
Tracks the real cost of maintaining a UHNW lifestyle.
- **Luxury Inflation (CLEW)**: Models the inflation rates of weighted luxury components: Services (security/staff), Private Aviation, Elite Education, and Collectibles. It calculates a "Luxury Inflation Alpha"—the gap between standard consumer inflation and the actual cost increase for a high-net-worth individual.

### 2. Generational Dilution Tracker (`scm_service.py`)
Predicts the sustainability of a legacy across family branches.
- **Wealth-per-Heir Projection**: Projects total wealth and wealth-per-person across N generations based on family growth assumptions (heirs per branch). It helps family offices understand the required "Internal Rate of Return" (IRR) to maintain a specific social standing as the family tree expands.

### 3. Class Risk & Stability Simulator (`scm_service.py`)
A quantitative audit of lifestyle sustainability.
- **Class Stability Monte Carlo**: Simulates the probability of maintaining a current social class across a client's life expectancy. It accounts for the annual "Burn Rate," net worth, and luxury inflation skews to determine if a lifestyle is "SECURE" or "AT RISK" of degrading the principal over time.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used |
| :--- | :--- | :--- |
| **Lifestyle Station**| CLEW Index Pulse | `scm_service.calculate_clew_index()` |
| **Legacy Station** | Generational Dilution Graph | `scm_service.project_wealth_dilution()` |
| **Governance Hub** | Class Maintenance Probability| `scm_service.run_class_risk_sim()` |
| **Lifestyle Station**| Sustainable Burn Monitor | `scm_service.run_class_risk_sim()` |
| **Portfolio Detail** | Luxury Inflation Alpha Card | `scm_service.calculate_clew_index()` |

## Dependencies
- `decimal`: Used for all precision math involving inflation rates, burn rates, and generational wealth distributions.
- `logging`: Records structural insights like "High Wealth Dilution Detected" or "Class Stability Probability Shifts."

## Usage Examples

### Calculating the CLEW Index (Personal Inflation)
```python
from services.lifestyle.scm_service import SCMService
from decimal import Decimal

scm = SCMService()

# Luxury cost inputs (e.g., Private flights inflated 12%, Education 9%)
input_rates = {
    "PRIVATE_FLIGHTS": Decimal("0.12"),
    "ELITE_EDUCATION": Decimal("0.09")
}

stats = scm.calculate_clew_index(components=input_rates)

print(f"Personal Inflation Rate (CLEW): {stats['clew_index_rate']:.2%}")
print(f"Lux Inflation Alpha: {stats['lux_inflation_alpha']:.2%}")
```

### Projecting Wealth Dilution Across 3 Generations
```python
from services.lifestyle.scm_service import SCMService
from decimal import Decimal

scm = SCMService()

# Starting wealth $500M, 3 heirs per generation, over 3 generations
dilution = scm.project_wealth_dilution(
    net_worth=Decimal("500000000.00"),
    heirs=3,
    generations=3
)

for d in dilution:
    print(f"Gen {d['generation']} | Total: ${d['total_wealth']:,.0f} | Per Heir: ${d['wealth_per_heir']:,.0f}")
```

### Running a Class Maintenance Simulator
```python
from services.lifestyle.scm_service import SCMService
from decimal import Decimal

scm = SCMService()

# $50M Net Worth, $2.5M Annual Lifestyle Burn, 7% Luxury Inflation
sim = scm.run_class_risk_sim(
    net_worth=Decimal("50000000.00"),
    annual_burn=Decimal("2500000.00"),
    clew_rate=0.07
)

print(f"Stability Status: {sim['status']}")
print(f"Probability of Class Persistence: {sim['probability']:.0%}")
print(f"Recommended Sustainable Burn: ${sim['sustainable_annual_burn']:,.2f}")
```
