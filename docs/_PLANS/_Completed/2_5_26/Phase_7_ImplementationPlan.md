# PHASE 7 IMPLEMENTATION PLAN: THE COMPLIANCE SHIELD (LAW & AUDIT)
## FOCUS: TAX COMPLIANCE, IMMUTABLE RECORDS, AND FORENSIC RECONCILIATION

---

## 1. PROJECT OVERVIEW: PHASE 7
Phase 7 is the "Protective Shell" of the OS. This phase builds the **Lawyer (Dept 8)** and **Auditor (Dept 9)** departments. We automate the truth-seeking functions of accounting and the legal/tax safeguards required for a Sovereign entity. This is the "Zero-Maintenance Compliance" stage.

---

## 2. GOALS & ACCEPTANCE CRITERIA
- **G1**: Automated Tax-Loss Harvesting (Agent 8.4) with < $3k wash-sale violation risk.
- **G2**: Immutable "Record Vault" using SHA-256 Hash-Chaining for all financial PDFs and logs.
- **G3**: Cent-by-cent "Ground Truth" reconciliation (Agent 9.5) between the system and the world.
- **G4**: Behavioral Audit (Agent 9.2) to detect human "Trading Tilt" or emotional variance.

---

## 3. FULL STACK SPECIFICATIONS

### 3.1 FRONTEND (The Audit Center)
- **Description**: Implementation of the Lawyer/Auditor workstations with forensic "Ledger Replay" UIs.
- **Acceptance Criteria**:
    - **C1: Record Notary HUD**: Displays the SHA-256 hash and "Notarized Status" (Checkmark) for 100% of files in the vault.
    - **C2: Discrepancy Alert**: High-visibility Dashboard Banner that appears instantly if the Reconciliation Bot detects a cent-variance.
    - **C3: Behavioral Chart**: A "Tilt Graph" (Scatter plot) that maps trade sizes against user heart rate or mouse jitter (Biometric data).

### 3.2 BACKEND (Compliance Logic)
- **Description**: The wash-sale watchdog, hash-chaining middleware, and forensic report generator.
- **Acceptance Criteria**:
    - **C1: Wash-Sale Blocker**: A POST trade request for a ticker sold at a loss in the last 30 days is blocked in < 5ms at the Controller level.
    - **C2: Ledger Hash-Chain**: Every new transaction row is cryptographically signed using the previous row's hash. Tamper detection takes < 1ms.
    - **C3: Tax Engine**: Harvesting logic identifies 100% of "Opportunity Batches" (Realized Gain - Unrealized Loss) on a daily cron.

### 3.3 INFRASTRUCTURE (Immutable Audit Trail)
- **Description**: Managing the cryptographically linked ledger storage and forensic logging.
- **Acceptance Criteria**:
    - **C1: Write-Once-Read-Many (WORM)**: Audit logs are stored on a filesystem configured to prevent deletion or modification of existing blocks.
    - **C2: High Availability**: Audit trails are mirrored across 3 physical storage nodes to prevent data loss or corruption.
    - **C3: HIBP Monitoring**: Real-time Sentry hook to `HaveIBeenPwned` API for 100% of system credential emails.

### 3.4 TESTING & VERIFICATION
- **Description**: Integrity testing and failure simulation.
- **Acceptance Criteria**:
    - **T1: Tamper Test**: If a DBA manually updates an amount in Postgres, the next application startup MUST fail with a "Chain Integrity Violation" error.
    - **T2: Wash-Sale Unit**: Test 50+ corner cases (e.g. buying in IRA vs Taxable for same ticker) to ensure the Blocker is airtight.
    - **T3: E2E**: User initiates a "Mistake Audit" -> System replays the last 30 days of trade/price data -> Identifies 100% of "Process Breaches."

---

## 4. AGENT CONTRACTS

##### 👤 AGENT 8.1: The Wash-Sale Watchdog
- **Acceptance Criteria**: Blocks 100% of trades on tickers with a realized loss in the last 30 days.

##### 👤 AGENT 9.5: The Reconciliation Bot
- **Acceptance Criteria**: Flags 100% of variances > $0.05 between Postgres Ledger and Plaid Bank balance within 60s of cron-job run.

##### 👤 AGENT 9.6: The Mistake Classifier
- **Acceptance Criteria**: Triage of every loss > $500 into: "Systemic Error," "Market Risk," or "Human Tilt."

---

## 5. MILESTONES & TIMELINE
- **Week 1**: Hash-Chained Ledger Database Schema + Middleware.
- **Week 2**: Wash-Sale Watchdog (Blocking Logic) + Tax Engine Alpha.
- **Week 3**: Reconciliation Bot (Plaid vs Ledger) + Automated Reporting.
- **Week 4**: Behavioral Audit (Tilt Graph) + Final Compliance Sweep.

---
**END OF PHASE 7 IMPLEMENTATION PLAN**
