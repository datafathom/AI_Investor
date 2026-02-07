# Backend Service: Treasury (The Cash Desk)

## Overview
The **Treasury Service** manages corporate cash and liquidity across the family office. It optimizes idle cash placement and manages sweep accounts.

## Core Components

### 1. Cash Management Service (`cash_management_service.py`)
- **Cash Position Tracking**: Monitors cash across all accounts.
- **Sweep Rules**: Defines when and where to move excess cash.

### 2. Idle Sweeper (`idle_sweeper.py`)
- **Automatic Sweep**: Moves idle cash to money market funds overnight.
- **Threshold Management**: Only sweeps amounts above a minimum balance.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used | Frontend Status |
| :--- | :--- | :--- | :--- |
| **Treasury Dashboard** | Cash Status | `cash_management_service` | **Missing** |

## Notes
This is a smaller service focused on operational treasury functions. Larger investment decisions are handled by the Planning and Strategy services.
