# Phase 2: Dependency & Mock Audit
## Implementation Plan - Source of Truth

**Parent Roadmap**: [ROADMAP_2_03_26.md](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/plans/2_03_26/ROADMAP_2_03_26.md)

---

## 📋 Phase Overview

| Attribute | Value |
|-----------|-------|
| **Phase Number** | 2 |
| **Focus Area** | Dependency & Mock Audit |
| **Deliverables** | 2 (Mock Tracking + Vendor API Inventory) |
| **Estimated Effort** | 2-3 days |
| **Dependencies** | Phase 1 (for understanding dependencies) |

---

## 2.1 Mock Response Tracking (App-Wide)

### Goal
Create a verbose inventory of **every single** instance of mock/hardcoded data across the entire backend.

### Target Artifact
`notes/MockResponses_needImplemenetation.json`

### Detailed Implementation

#### 1. Audit Script `scripts/runners/mock_audit.py`
We will create a script that recursively scans the following **validated** directories:
- `services/` (989 files) -> High Priority
- `agents/` (15 files) -> Medium Priority
- `web/` (Routes/Blueprints) -> High Priority
- `apis/` -> Legacy API definitions

#### 2. Detection Logic
The script must flag:
- **Keywords**: `mock`, `dummy`, `fake`, `sample_data`, `placeholder`, `TODO`, `FIXME`.
- **Patterns**:
    - Functions returning literal dictionaries/lists > 5 lines long.
    - Files with `from tests` imports (leaking test data into prod).
    - `pass` statements in non-abstract methods.

#### 3. Known "Hotspots" (Pre-identified)
During planning, we identified these specific files as likely containing mocks. The audit script **must** verify them:
- `services/trading/fx_service.py`
- `services/trading/simulation_service.py`
- `services/payments/plaid_service.py` (Often mocks sandbox mode)
- `services/social/youtube_client.py`
- `services/reputation/deepfake_detect.py`

#### 4. Output Schema
The JSON must be actionable:
```json
{
  "summary": { "total": 120, "critical": 45 },
  "entries": [
    {
      "file": "services/trading/fx_service.py",
      "line": 42,
      "type": "hardcoded_return",
      "snippet": "return {'rate': 1.05}",
      "action_item": "Connect to AlphaVantage FX API"
    }
  ]
}
```

## 2.2 Vendor API Inventory (App-Wide)

### Goal
Catalog every external service dependent on an API key or secret.

### Target Artifact
`notes/Vendor_API_Needed.json`

### Known Integrations (Verified)
We have confirmed references to the following vendors. The inventory script must confirm if they are *active*, *mocked*, or *dead code*:

1.  **Financial / Payments**:
    - **Stripe** (`services/payments/stripe_service.py`)
    - **Plaid** (`services/payments/plaid_service.py`)
    - **Coinbase** (`services/payments/coinbase_service.py`)
    - **PayPal** (`services/payments/paypal_service.py`)
    - **Square** (`services/payments/square_service.py`)
    - **Venmo** (`services/payments/venmo_service.py`)
    - **TaxBit** (`services/taxes/taxbit_service.py`)

2.  **Communication / Notifications**:
    - **Twilio** (`services/notifications/twilio_service.py`)
    - **Slack** (`services/notifications/slack_service.py`)
    - **SendGrid** (`services/notifications/sendgrid_service.py`)
    - **PagerDuty** (`services/notifications/pagerduty_service.py`)
    - **Discord** (`services/social/discord_bot.py`)

3.  **Data / Social**:
    - **YouTube** (`services/social/youtube_client.py`)
    - **StockTwits** (`services/social/stocktwits_client.py`)
    - **Reddit** (`services/social/reddit_service.py`)
    - **Facebook** (`services/social/facebook_hype_service.py`)

4.  **Infrastructure**:
    - **S3** (`services/storage/s3_service.py`)

### Automation Strategy
- **Script**: `scripts/runners/vendor_audit.py`
- **Logic**:
    - Scan `services/` for imports matching vendor SDKs (`stripe`, `plaid`, `boto3`, `twilio`).
    - Scan `.env` (safe read) or `config.py` for variables like `STRIPE_KEY`, `TWILIO_SID`.
    - Report "Missing Credentials" if SDK is imported but no Env Var is detected.

## 📊 Verification Plan
### Automated Tests
1.  **Unit Tests**: `tests/scripts/test_mock_audit.py` (Verify it finds a known mock).
2.  **Unit Tests**: `tests/scripts/test_vendor_audit.py` (Verify it identifies Stripe from imports).

### Manual Verification
- Run `python cli.py audit mocks` -> Check output JSON size > 0.
- Run `python cli.py audit vendor-apis` -> Check it lists all 17+ vendors identified above.
