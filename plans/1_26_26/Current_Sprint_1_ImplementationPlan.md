# Implementation Plan: Sprint 1 - The Foundation

## Goal
Establish a robust, standardized infrastructure for API communication, universal navigation, and real-time system telemetry.

## 1. Core Infrastructure Refactor
### 1.1 `apiClient.js` Centralization
- **Purpose**: Unified request/response handling, global error management, and auto-retries.
- **Files**: `frontend2/src/services/apiClient.js`
- **Logic**:
    - Axios instance with `baseURL: /api/v1/`.
    - Interceptors for 401 (auth redirect), 429 (rate limiting), and 5xx (retry logic).
    - Global loading state hook integration.

### 1.2 Universal Search Spotlight
- **Purpose**: Ctrl+K indexing of all system entities.
- **Files**: `frontend2/src/components/CommandPalette.jsx`
- **Logic**:
    - Client-side indexing of active entities (Agents, Symbols, Clients).
    - Asynchronous fallback for deep database searches.

## 2. Sprint 1 Widgets (Telemetry & Connectivity)
| Widget | Purpose | Technical Logic |
|--------|---------|-----------------|
| `QuotaHealthMeter` | Track API limits | Polls `system_health_service.py` every 60s for quota tokens. |
| `LatencyGlobalMap` | Data provider lag | Measures pings to AlphaVantage, Polygon, and FRED endpoints. |
| `SearchHistorySpotlight` | Fast access | Persists recent search IDs to LocalStorage. |
| `SystemLoadRibbon` | Kafka/CPU stress | WebSocket listener on `system:load` channel. |
| `CliHistoryWizard` | Terminal memory | Stores last 20 terminal commands in `userStore`. |
| `AuthSessionTimer` | JWT lifecycle | Calculates remaining TTL from decoded JWT `exp` claim. |

## 3. Acceptance Criteria
- [x] **Infrastructure**: No component calls `axios` directly; all pass through `apiClient`.
- [x] **Search**: Spotlight resolves a search query for a "Known Client" in under 100ms.
- [x] **Telemetry**: `QuotaHealthMeter` reflects real-time token depletion during 100 historical quote requests.
- [x] **Auth**: `AuthSessionTimer` triggers a toast notification 5 minutes before expiry.

## 4. Testing & Code Coverage
- **Unit Tests**:
    - `apiClient.test.js`: Mock 401/429/500 responses and verify interceptor behavior. ✅ Completed.
    - `CommandPalette.test.jsx`: Verify filtering logic for symbols and clients. ✅ Completed.
- **E2E Tests (Selenium)**:
    - `test_sprint1_telemetry.py`: Verify that the `SystemLoadRibbon` animates when the backend backend initiates a stress period. ✅ Completed.
- **Targets**:
    - [x] 90% logic coverage for `apiClient.js`.
    - [x] 85% component coverage for the 6 new widgets.
