# Phase 5: HITL, Security & Cold-Haven

## Overview
This is the "Defensive Shield" phase. We are implementing the Human-in-the-Loop (HITL) checkpoints using cryptographic biometric signatures and the "Nuclear Option" Panic Protocol. This ensures that even in an autonomous system, the human remains the ultimate anchor for high-value decisions and failsafe extraction.

## Deliverables

### 1. WebAuthn Biometric Gateway (React)
**Description**: Integration of the browser's native Public Key Credential API (Fingerprint/FaceID) for mission approvals.
- **Acceptance Criteria**:
  - "Approve" button triggers a native biometric prompt (Windows Hello/TouchID).
  - Cryptographic signature of the `approval_id` is generated locally and sent to the backend.
  - UI displays a "Secure Signature Verified" visual state upon success.

### 2. "Checkpoint & Resume" Approval Logic
**Description**: Backend state-machine that pauses high-value agent tasks until a human signature is received.
- **Acceptance Criteria**:
  - Missions with a `risk_score` > Threshold automatically enter a `PENDING_APPROVAL` state in Redis.
  - Suspended job state is persisted for up to 24 hours without data loss.
  - Resume signal is only accepted if the `approval_id` signature matches the human's stored public key.

### 3. Global "Panic Mode" Protocol
**Description**: A one-click (and auto-triggered) mechanism to freeze the entire OS and evacuate assets.
- **Acceptance Criteria**:
  - `triggerPanicProtocol` terminates 100% of active ARQ jobs in < 50ms.
  - Outbound network tunnels are immediately dropped to isolate the "Cage."
  - UI displays a full-screen "SYSTEM_LOCKED" overlay until a master recovery key is provided.

### 4. Cold-Haven Evacuation Engine
**Description**: Automatic sweep of all mission-controlled wallets to a hardcoded "Cold Storage" address.
- **Acceptance Criteria**:
  - Successfully aggregates P&L from 10+ mock wallets and submits a "Sweep" transaction to the EVM gateway.
  - Extraction priority logic (Stablecoins First) is followed during the sweep.
  - Final extraction report is generated and stored in the encrypted Historian log.

### 5. Dead Man's Switch (Inactivity Heartbeat)
**Description**: A timer that triggers the Panic Mode if the operator does not "check-in" within a certain window.
- **Acceptance Criteria**:
  - Heartbeat can be set via the `ColdHavenConfig` HUD (12h to 7 days).
  - Background process correctly counts down and executes Panic if the `last_heartbeat` key in Redis expires.
  - "Warning" notifications are sent to the UI 1 hour before the switch trips.

### 6. PGP-Encrypted Off-Site Backup Script
**Description**: Exporting all Postgres and Neo4j data into an encrypted archive sent to isolated storage.
- **Acceptance Criteria**:
  - Backup file is encrypted using a PGP key that is NOT stored on the server.
  - Script runs inside the `internal-network` container (raw data never touches the DMZ).
  - Successful mock restoration from an encrypted archive verified.

## Proposed Changes

### [Backend] [Identity]
- [NEW] [webauthn_service.py](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/services/webauthn_service.py): Signature verification logic.
- [NEW] [approval_router.py](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/web/routes/approval_router.py): HITL management.

### [Frontend] [Security]
- [NEW] [ApprovalPortal.jsx](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/frontend/src/components/ApprovalPortal.jsx): The Biometric overlay.
- [NEW] [ColdHavenConfig.jsx](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/frontend/src/components/ColdHavenConfig.jsx): Dead Man's Switch and extraction settings.

## Verification Plan

### Automated Tests
- `pytest tests/security/test_panic_killswitch.py`
- `pytest tests/security/test_webauthn_flow.py`

### Manual Verification
- Set Heartbeat to 2 mins, wait, and verify "Panic Mode" activates automatically.
- Attempt to approve a $10,000 "Mock Trade" without biometrics (verify refusal).
