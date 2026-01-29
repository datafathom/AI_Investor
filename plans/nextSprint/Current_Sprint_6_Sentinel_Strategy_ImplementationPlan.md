# Implementation Plan: Sprint 6 - Sentinel & Strategy

## Goal
Finalize the high-security hardware bridging and advanced strategy comparison tools (Shadow Engine & Timeline Scrubber).

## 1. Security & Hardware Bridging
### 1.1 Hardware Multi-Sig (Phase 51)
- **Files**: `frontend2/src/services/hardwareService.js`
- **Logic**: Use `WebHID` or `WebUSB` to pair with Ledger/Trezor devices.
- **Trigger**: Intercept `withdraw` or `execute_large_trade` events in `apiClient.js` to require a hardware signature.

### 1.2 Biometric Identity Bridge
- **Logic**: Connect `IdentityService` to the WebAuthn API for physical key verification during admin logins.

## 2. Strategy & Timeline Logic
| Feature | Practical Implementation |
|---------|--------------------------|
| **Shadow Strategy Engine** | Fork a live strategy state in-browser and run a parallel "What-If" simulation using the `ScenarioService`. |
| **Global Event Scrubber** | A `d3.brush` timeline at the bottom of the screen aggregating News, Trades, and Graph shocks. |
| **Sentinel Alpha Alerts** | High-priority push notifications (via Twilio/SendGrid) for "Regime Shift" detections. |

## 3. Acceptance Criteria
- [x] **Hardware Multi-Sig**: $200k transfer requires hardware signature (wired in `apiClient.js`).
- [x] **Shadow Engine**: User can "Copy to Shadow" any live strategy and see 24h projected divergence in < 2 seconds (`ShadowStrategyPanel.jsx`).
- [x] **Timeline**: Dragging the scrubber back 1 hour updates the Master Orchestrator graph to show its historical state (`GraphTimeScrubber.jsx` + `timelineStore` wiring).
- [x] **Security**: 2FA challenge is triggered for ANY secret retrieval in the APIDashboard (`system_api.py` POST /secrets).

## 4. Testing & Code Coverage
- **Unit Tests**:
    - `hardwareService.test.js`: Mock USB signatures and verify payload validation.
    - `timelineStore.test.js`: Verify data aggregation from News, Trade, and Risk streams.
- **E2E Tests**:
    - `test_sentinel_lock.py`: Verify that a "High Value" event successfully triggers the hardware modal and blocks execution until signed.
- **Targets**:
    - 100% coverage for hardware signature validation logic.
    - 85% coverage for the Shadow Simulation engine.
