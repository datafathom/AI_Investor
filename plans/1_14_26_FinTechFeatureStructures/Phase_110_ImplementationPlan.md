# Phase 110: Custodian Platform & Anti-Fraud Ledger

> **Status**: `[ ]` Not Started  
> **Last Updated**: 2026-01-25  
> **Owner**: Security & Compliance Team

---

## 📋 Overview

**Description**: Implement custodian platform integration and anti-fraud safeguards including third-party custody verification, bank sweep tracking, and anti-Madoff protections to prevent advisor-held asset schemes.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON_2.txt - Phase 10 (Custodian Platform & Anti-Fraud Ledger)

---

## 🎯 Sub-Deliverables

### 110.1 Neo4j Custodian Node (Schwab, Fidelity) `[ ]`

**Acceptance Criteria**: Define Neo4j nodes for major custodians (Schwab, Fidelity, Pershing) with relationships to client accounts and asset holdings.

#### Neo4j Schema (Docker-compose: neo4j service)

```cypher
// Custodian Nodes
CREATE CONSTRAINT custodian_id IF NOT EXISTS FOR (c:CUSTODIAN) REQUIRE c.id IS UNIQUE;

(:CUSTODIAN {
    id: "uuid",
    name: "Charles Schwab",
    type: "QUALIFIED_CUSTODIAN",
    sipc_member: true,
    fdic_member: true,
    regulatory_body: "SEC",
    assets_under_custody: 8000000000000,  // $8T
    security_rating: "A+",
    api_integration: true
})

// Account @ Custodian
(:CLIENT)-[:HAS_ACCOUNT_AT {
    account_number: "XXXX-1234",
    account_type: "BROKERAGE",
    opened_date: date(),
    is_verified: true,
    last_verified: datetime()
}]->(:CUSTODIAN)

// Asset Custody Chain
(:ASSET)-[:CUSTODIED_AT {
    quantity: 1000,
    market_value: 450000,
    registration: "STREET_NAME"
}]->(:CUSTODIAN)

// Advisor Access (Limited)
(:ADVISOR)-[:HAS_TRADING_AUTHORITY {
    type: "LIMITED_POA",
    can_withdraw: false,
    can_transfer_out: false,
    granted_date: date()
}]->(:CLIENT_ACCOUNT)
```

#### Backend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Custodian Graph Service | `services/neo4j/custodian_graph.py` | `[ ]` |
| Account Verifier | `services/custody/account_verifier.py` | `[ ]` |
| Asset Custody Tracker | `services/custody/asset_custody_tracker.py` | `[ ]` |
| API: Schwab Adapter | `services/brokers/schwab_adapter.py` | `[ ]` |
| API: Fidelity Adapter | `services/brokers/fidelity_adapter.py` | `[ ]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Custodian Status Panel | `frontend2/src/components/Custody/StatusPanel.jsx` | `[ ]` |
| Account Verification Badge | `frontend2/src/components/Custody/VerificationBadge.jsx` | `[ ]` |
| Custody Chain Visualizer | `frontend2/src/components/Neo4j/CustodyChain.jsx` | `[ ]` |

#### Tests

| Test Type | File Path | Status |
|-----------|-----------|--------|
| Unit: Custodian Graph | `tests/unit/test_custodian_graph.py` | `[ ]` |
| Unit: Account Verifier | `tests/unit/test_account_verifier.py` | `[ ]` |
| Integration: Broker APIs | `tests/integration/test_broker_adapters.py` | `[ ]` |

---

### 110.2 Postgres Digital Platform Ledger `[ ]`

**Acceptance Criteria**: Create an immutable ledger tracking all digital platform transactions with SHA-256 hashing for audit integrity.

#### Postgres Schema (Docker-compose: timescaledb service)

```sql
CREATE TABLE platform_ledger (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    entry_timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    -- Transaction Details
    transaction_type VARCHAR(50) NOT NULL,    -- DEPOSIT, WITHDRAWAL, TRADE, TRANSFER, FEE
    account_id UUID NOT NULL,
    custodian_id UUID NOT NULL,
    
    -- Amounts
    amount DECIMAL(20, 2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'USD',
    
    -- Counterparty
    from_account VARCHAR(100),
    to_account VARCHAR(100),
    counterparty_name VARCHAR(255),
    
    -- Verification
    custodian_confirmation_id VARCHAR(100),
    custodian_confirmed_at TIMESTAMPTZ,
    is_reconciled BOOLEAN DEFAULT FALSE,
    reconciled_at TIMESTAMPTZ,
    
    -- Audit Trail
    created_by UUID,
    ip_address INET,
    user_agent TEXT,
    
    -- Immutability Hash
    previous_hash VARCHAR(64),
    entry_hash VARCHAR(64) NOT NULL,
    hash_verified BOOLEAN DEFAULT FALSE
);

SELECT create_hypertable('platform_ledger', 'entry_timestamp');
CREATE INDEX idx_ledger_account ON platform_ledger(account_id);
CREATE INDEX idx_ledger_hash ON platform_ledger(entry_hash);

-- Trigger to compute hash
CREATE OR REPLACE FUNCTION compute_ledger_hash()
RETURNS TRIGGER AS $$
BEGIN
    NEW.entry_hash = encode(
        sha256(
            (NEW.id || NEW.entry_timestamp || NEW.transaction_type || 
             NEW.account_id || NEW.amount || COALESCE(NEW.previous_hash, ''))::bytea
        ), 
        'hex'
    );
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER ledger_hash_trigger
    BEFORE INSERT ON platform_ledger
    FOR EACH ROW EXECUTE FUNCTION compute_ledger_hash();
```

#### Backend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Migration | `migrations/110_platform_ledger.sql` | `[ ]` |
| Ledger Model | `models/platform_ledger.py` | `[ ]` |
| Ledger Service | `services/custody/ledger_service.py` | `[ ]` |
| Hash Verifier | `services/audit/hash_verifier.py` | `[ ]` |
| Reconciliation Service | `services/custody/reconciliation.py` | `[ ]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Transaction Ledger View | `frontend2/src/components/Ledger/TransactionLedger.jsx` | `[ ]` |
| Hash Verification Panel | `frontend2/src/components/Audit/HashVerification.jsx` | `[ ]` |
| Reconciliation Status | `frontend2/src/components/Ledger/ReconciliationStatus.jsx` | `[ ]` |

#### Tests

| Test Type | File Path | Status |
|-----------|-----------|--------|
| Unit: Ledger Service | `tests/unit/test_ledger_service.py` | `[ ]` |
| Unit: Hash Verifier | `tests/unit/test_hash_verifier.py` | `[ ]` |
| Unit: Hash Chain Integrity | `tests/unit/test_hash_chain_integrity.py` | `[ ]` |
| Integration: Ledger Pipeline | `tests/integration/test_ledger_pipeline.py` | `[ ]` |

---

### 110.3 Advisor-Held Assets Block (Anti-Madoff) `[ ]`

**Acceptance Criteria**: Implement strict controls that prevent advisors from ever having direct custody of client assets, with alerts on any custody anomalies.

#### Backend Implementation

```python
class AntiMadoffGuard:
    """
    Prevent advisor-held asset fraud patterns.
    
    Red Flags:
    1. Assets held at non-qualified custodian
    2. Advisor has withdrawal authority
    3. Statements issued by advisor, not custodian
    4. Returns too consistent (Madoff pattern)
    5. Audit performed by unknown firm
    """
    
    def validate_custody_arrangement(
        self, 
        account: Account
    ) -> CustodyValidationResult:
        """Ensure proper third-party custody."""
        pass
    
    def detect_too_good_returns(
        self, 
        returns: list[Decimal],
        volatility_threshold: Decimal = Decimal('0.01')
    ) -> bool:
        """Detect suspiciously consistent returns (Madoff pattern)."""
        pass
    
    def validate_statement_source(
        self, 
        statement: Statement
    ) -> SourceValidationResult:
        """Ensure statements come from qualified custodian."""
        pass
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Anti-Madoff Guard | `services/fraud/anti_madoff_guard.py` | `[ ]` |
| Custody Validator | `services/fraud/custody_validator.py` | `[ ]` |
| Returns Anomaly Detector | `services/fraud/returns_anomaly.py` | `[ ]` |
| Alert Publisher | `services/kafka/fraud_alert_publisher.py` | `[ ]` |

#### Kafka Alert Topic

```json
{
    "topic": "fraud-alerts",
    "schema": {
        "alert_id": "uuid",
        "alert_type": "string",
        "severity": "string",
        "account_id": "uuid",
        "description": "string",
        "recommended_action": "string",
        "timestamp": "timestamp"
    }
}
```

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Fraud Alert Banner | `frontend2/src/components/Alerts/FraudAlert.jsx` | `[ ]` |
| Custody Health Check | `frontend2/src/components/Custody/HealthCheck.jsx` | `[ ]` |
| Verification Wizard | `frontend2/src/components/Custody/VerificationWizard.jsx` | `[ ]` |

#### Tests

| Test Type | File Path | Status |
|-----------|-----------|--------|
| Unit: Anti-Madoff Guard | `tests/unit/test_anti_madoff_guard.py` | `[ ]` |
| Unit: Returns Anomaly | `tests/unit/test_returns_anomaly.py` | `[ ]` |
| Integration: Fraud Detection | `tests/integration/test_fraud_detection.py` | `[ ]` |

---

### 110.4 Bank Sweep Interest Revenue Model `[ ]`

**Acceptance Criteria**: Track and optimize bank sweep program interest, comparing custodian sweep rates against high-yield alternatives.

| Component | File Path | Status |
|-----------|-----------|--------|
| Sweep Tracker | `services/banking/sweep_tracker.py` | `[ ]` |
| Interest Comparator | `services/banking/interest_comparator.py` | `[ ]` |
| Optimization Suggester | `services/banking/sweep_optimizer.py` | `[ ]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Sweep Interest Dashboard | `frontend2/src/components/Banking/SweepDashboard.jsx` | `[ ]` |
| Rate Comparison Card | `frontend2/src/components/Banking/RateComparison.jsx` | `[ ]` |

#### Tests

| Test Type | File Path | Status |
|-----------|-----------|--------|
| Unit: Sweep Tracker | `tests/unit/test_sweep_tracker.py` | `[ ]` |
| Unit: Interest Comparator | `tests/unit/test_interest_comparator.py` | `[ ]` |

---

### 110.5 Third-Party Custodian API Bridge `[ ]`

**Acceptance Criteria**: Build a unified API bridge that connects to multiple custodian APIs (Schwab, Fidelity, Pershing) for real-time position and transaction data.

| Component | File Path | Status |
|-----------|-----------|--------|
| Unified API Bridge | `services/brokers/unified_bridge.py` | `[ ]` |
| Schwab API Client | `services/brokers/schwab_client.py` | `[ ]` |
| Fidelity API Client | `services/brokers/fidelity_client.py` | `[ ]` |
| Pershing API Client | `services/brokers/pershing_client.py` | `[ ]` |
| Position Aggregator | `services/portfolio/position_aggregator.py` | `[ ]` |

#### Frontend Implementation

| Component | File Path | Status |
|-----------|-----------|--------|
| Multi-Custodian View | `frontend2/src/components/Portfolio/MultiCustodian.jsx` | `[ ]` |
| Connection Status | `frontend2/src/components/API/ConnectionStatus.jsx` | `[ ]` |

#### Tests

| Test Type | File Path | Status |
|-----------|-----------|--------|
| Unit: Unified Bridge | `tests/unit/test_unified_bridge.py` | `[ ]` |
| Unit: Position Aggregator | `tests/unit/test_position_aggregator.py` | `[ ]` |
| Integration: Multi-Custodian | `tests/integration/test_multi_custodian.py` | `[ ]` |

---

## 📊 Phase Completion Summary

| Deliverable | Status | E2E Verified |
|-------------|--------|--------------|
| 110.1 Neo4j Custodian Nodes | `[ ]` | `[ ]` |
| 110.2 Platform Ledger | `[ ]` | `[ ]` |
| 110.3 Anti-Madoff Guard | `[ ]` | `[ ]` |
| 110.4 Bank Sweep Model | `[ ]` | `[ ]` |
| 110.5 API Bridge | `[ ]` | `[ ]` |

**Phase Status**: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py custody verify <account>` | Verify custody arrangement | `[ ]` |
| `python cli.py ledger audit` | Run ledger hash audit | `[ ]` |
| `python cli.py fraud scan` | Scan for fraud patterns | `[ ]` |
| `python cli.py sweep compare` | Compare sweep rates | `[ ]` |

---

*Last verified: 2026-01-25*
