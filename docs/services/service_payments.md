# Backend Service: Payments (Fintech Gateway)

## Overview
The **Payments Service** (plural) acts as the integration hub for external financial APIs. Unlike the "Payment" service (which handles internal trust flows), this service wraps third-party SDKs into a unified interface for the rest of the Sovereign OS. It enables the system to See (Plaid), Earn (Stripe), and Trade (Coinbase/Robinhood).

## Core Components

### 1. Plaid Connector (`plaid_service.py`)
The Bank Bridge.
- **Link Token Exchange**: Manages the multi-step Oauth flow to securely connect users' bank accounts without ever touching their credentials.
- **Micro-Deposit Verification**: (Mocked) logic for validating ACH routing numbers.

### 2. Stripe Manager (`stripe_service.py`)
The Revenue Engine.
- **Subscription Management**: Handles SaaS billing for the platform itself (if monetized) or for collecting tenant rents.
- **Checkout Sessions**: Generates secure payment links for one-off transactions.

### 3. Crypto/Brokerage Bridges (`coinbase_service.py`, `robinhood_service.py`)
The Execution Rails.
- **Unified Trading Interface**: Abstracts away the differences between crypto (Coinbase) and equity (Robinhood) orders, allowing the `OrderExecutionService` to simply call `buy(symbol, qty)`.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used | Frontend Status |
| :--- | :--- | :--- | :--- |
| **Banking Dashboard** | Link Account Btn | `plaid_service.create_link_token()` | **Implemented** (`PlaidLinkModal.jsx`) |
| **Crypto Wallet** | Trade Panel | `coinbase_service.place_order()` | **Implemented** (`CoinbaseTrade.jsx`) |
| **Brokerage** | Account Connect | `robinhood_service.link_account()` | **Implemented** (`RobinhoodConnect.jsx`) |

## Dependencies
- `plaid-python`: Official Plaid SDK.
- `stripe`: Official Stripe SDK.
- `coinbase-advanced-py`: (Future) Coinbase Advanced Trade API client.

## Usage Examples

### Linking a New Bank Account
```python
from services.payments.plaid_service import get_plaid_client

plaid = get_plaid_client()

# 1. Frontend requests a Link Token
token_response = await plaid.create_link_token(user_id="user_123")
print(f"Link Token: {token_response['link_token']}")

# 2. Frontend launches Plaid Link... sends back public_token
# 3. Backend exchanges for Access Token
access_data = await plaid.exchange_public_token("public-sandbox-123")
print(f"Access Token: {access_data['access_token']}")
```

### Creating a Stripe Checkout Session
```python
from services.payments.stripe_service import get_stripe_client

stripe = get_stripe_client()

session = await stripe.create_checkout_session(
    user_id="tenant_01",
    plan_id="price_monthly_rent"
)

print(f"Redirect User to: {session['url']}")
```
