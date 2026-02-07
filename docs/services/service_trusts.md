# Backend Service: Trusts (The Estate Vault)

## Overview
The **Trusts Service** manages Charitable Remainder Trusts (CRTs) and other trust structures for estate planning. It handles distributions, remainder calculations, and tax benefits.

## Core Components

### 1. CRT Service (`crt_service.py`)
- **Distribution Management**: Calculates annual distributions based on trust type.
- **Remainder Tracking**: Monitors the remainder interest for charitable beneficiaries.

### 2. CRT Distribution (`crt_distribution.py`)
- Calculates specific payout amounts based on unitrust or annuity trust rules.

### 3. Remainder Trigger (`remainder_trigger.py`)
- Monitors when the remainder interest passes to charity.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used | Frontend Status |
| :--- | :--- | :--- | :--- |
| **Estate Planning** | CRT Calculator | `crt_service` | **Partially Implemented** |

## Notes
CRTs provide income streams to donors while benefiting charities, with significant tax advantages.
