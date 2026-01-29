# Implementation Plan: Sprint 5 - System Zenith (Taskbar & UX)

## Goal
Transform the bottom taskbar into a functional OS command center with window management, agent telemetry, and a global kill switch.

## 1. OS Taskbar Logic
### 1.1 Window & Workspace Management
- **Active App Previews**: Implement `onMouseEnter` logic in `TaskbarIcon.jsx` to render a miniature `html2canvas` snapshot of the target window.
- **Workspace Switcher**: Add logical grouping (Research/Strategy/Admin) to the taskbar JSON config.

### 1.2 Live Agent Status (Mood Icons)
- **Logic**: 
    - Map Agent P&L/Volatility vectors to a set of 5 SVG "Mood" states (Happy, Neutral, Stressed, Panic, Aggressive).
    - Update icons via the `presenceService` heartbeat.

## 2. System Controls
| Module | Practical Implementation |
|--------|--------------------------|
| **The "Start" Menu** | Searchable list of all 80+ routes, grouped by Phase. |
| **System Mini-Meters** | 1px SVG bars at the top of the taskbar showing live Kafka throughput. |
| **Global Kill Switch** | Red glowing button with 3-second long-press requirement + MFA verification. |

## 3. Acceptance Criteria
- [x] **Taskbar**: Clicking an icon brings the corresponding window to front and focuses it.
- [x] **Previews**: Hovering over icons shows a recognizable snapshot (currently rich skeleton, ready for html2canvas).
- [x] **Kill Switch**: Activating the switch sends a broadcast `HALT` to all connected browser clients and backend services (MFA verified - 3s press → MFA modal → backend validation).
- [x] **Badges**: Icons display counts (e.g., notifications, alerts) integrated from window state.

## 4. Testing & Code Coverage
- **Unit Tests**:
    - `taskbarStore.test.js`: Verify icon pinning and workspace grouping logic.
    - `KillSwitch.test.jsx`: Verify MFA promise resolution before triggering the `HALT` event.
- **E2E Tests**:
    - `test_taskbar_integration.py`: Open 5 windows, verify all show in the taskbar, and test minimize/restore behavior.
- **Targets**:
    - 90% logic coverage for window management state.
    - 80% coverage for the Taskbar UI components.
