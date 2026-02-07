# Backend Service: Payment (Trust Administration)

## Overview
The **Payment Service** (singular) is a specialized module for **Trust Administration**. Unlike general bill pay, this service handles the complex, compliance-heavy outflows required for Irrevocable Life Insurance Trusts (ILITs) and Special Needs Trusts (SNTs). It ensures that every dollar leaving these entities follows strict legal protocols to preserve tax benefits and government aid eligibility.

## Core Components

### 1. ILIT Flow Manager (`ilit_flow.py`)
The Estate Tax Shield.
- **Workflow Enforcement**: detailed logic to ensure the "Crummey" process is followed:
    1.  Grantor Gifts cash to Trust.
    2.  Trustees send "Crummey Notices" to beneficiaries (giving them a window to withdraw).
    3.  Trust pays the Insurance Carrier.
- **Audit Trail**: Logs every step to prove to the IRS that the gift was "present interest," qualifying for the annual exclusion.

### 2. Vendor Direct (`vendor_direct.py`)
The SNT Guardian.
- **SSI/Medicaid Protection**: Ensures payments are made **directly to vendors** (e.g., paying a landlord or phone company) rather than giving cash to the beneficiary. This prevents the beneficiary from losing government benefits due to "income" rules.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used | Frontend Status |
| :--- | :--- | :--- | :--- |
| **Bill Pay** | Trust Payment Portal | `vendor_direct.process_vendor_payment()` | **Implemented** (`BillPaymentDashboard.jsx`) |
| **Estate Admin** | Crummey Tracker | `ilit_flow.process_premium_cycle()` | **Missing** (Backend logic exists, UI pending) |

## Dependencies
- `logging`: Critical for audit trails in legal defense.
- `typing`: Type enforcement for financial safety.

## Usage Examples

### Processing an ILIT Premium
```python
from services.payment.ilit_flow import ILITFlowService

ilit_svc = ILITFlowService()

# 1. Grantor gifts $50k
# 2. Notices sent...
# 3. Time to pay the carrier
result = ilit_svc.process_premium_cycle(
    ilit_id="ilit_dynasty_01",
    premium_amount=50000.00
)

print(f"Workflow Status: {result['workflow_status']}")
for step in result['audit_trail']:
    print(f"- {step['step']}: {step['status']}")
```

### Paying a Vendor from an SNT
```python
from services.payment.vendor_direct import VendorDirectPayment

snt_pay = VendorDirectPayment()

# Pay Rent directly to Landlord (Approved Expense)
receipt = snt_pay.process_vendor_payment(
    trust_id="snt_beneficiary_01",
    vendor_id="landlord_llc",
    amount=2500.00,
    category="SHELTER"
)

print(f"Payment ID: {receipt['payment_id']}")
print(f"Status: {receipt['status']}")
```
