# Phase 14: Payment Gateway Integration (Stripe)
> **Phase ID**: 14
> **Status**: Completed
> **Date**: 2026-01-19

## Overview
Implement the billing and subscription infrastructure using Stripe. This enables the platform to monetize through tiered access (e.g., Free, Pro, Institutional) and manage recurring payments securely.

## Objectives
- [ ] Add `stripe` to `requirements.txt`.
- [ ] Create `PaymentService` (backend) for Stripe interaction.
- [ ] Implement Tier-based access control logic.
- [ ] Add API endpoints:
    - `POST /api/v1/billing/create-checkout-session`
    - `GET /api/v1/billing/subscription-status`
    - `POST /api/v1/billing/webhook` (Handle Stripe events)
- [ ] Create `BillingDashboard` widget (frontend).
- [ ] Integrate tier checks into specific advanced routes/features.

## Files to Modify/Create
1.  `requirements.txt` (Add `stripe`)
2.  `services/billing/payment_service.py` **[NEW]**
3.  `web/api/billing_api.py` **[NEW]**
4.  `web/app.py` (Register Billing API)
5.  `frontend2/src/widgets/Billing/BillingDashboard.jsx` **[NEW]**
6.  `frontend2/src/pages/Settings.jsx` (Add Billing Tab)

## Technical Design

### Backend (`PaymentService`)
- Manages Stripe API calls (Checkout, Customer Portal, Webhooks).
- **Tiers**:
    - **Free**: Basic scanner, tutorial mode.
    - **Pro**: Live trading, sentiment analysis, advanced charts.
    - **Institutional**: FIX connectivity, custom risk models, multi-user.
- **Webhook Handler**: Listen for `invoice.paid`, `customer.subscription.deleted`, etc., to update user entitlement status in the DB/Cache.

### API
- `POST /create-checkout-session`: Returns a Stripe hosted checkout URL.
- `GET /subscription-status`: Returns current tier and next billing date.
- `POST /webhook`: Unauthenticated but requires Stripe signature verification.

### Frontend
- **BillingDashboard**: Shows current plan, transaction history, and "Upgrade" buttons.
- **TierGuard Component**: A wrapper for components that require a specific tier.

## Verification Plan

### Automated Tests
- `tests/system/test_payment_service.py`:
    - Mock Stripe API sessions.
    - Verify tier entitlement logic.
    - Test webhook parsing (valid vs invalid signatures).

### Manual Verification
1.  Navigate to `/settings/billing`.
2.  Click "Upgrade to Pro".
3.  Verify redirection to Stripe Checkout (simulated/test mode).
4.  Confirm tier updates after successful "payment".
