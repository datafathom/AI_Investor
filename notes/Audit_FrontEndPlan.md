# Frontend Audit Plan: AI Investor Platform

This plan outlines the systematic audit of all frontend pages to ensure 100% accessibility from the navigation menu and flawless UI/UX compliance with the "Gold Standard."

## 1. Environment Preparation
- **Clean State**: Run `python cli.py stop-all` to clear existing runtimes.
- **Boot**: Run `python cli.py dev` to start a fresh development environment.
- **Auth Protocol (MANDATORY)**:
  - Register a unique date-stamped account: `audit_YYYY_MM_DD@fathom.ai`.
  - Programmatically verify via `/api/auth/verify-email?email=...&token=mock_verify_token`.
  - Perform a manual-style UI Login.

## 2. Navigation Completion (Phase 1)
- **Mapping**: Compare all `<Route>` definitions in `App.jsx` against the `MENU_ITEMS` in `MenuBar.jsx`.
- **Accessibility Fixes**:
  - Ensure every functional route has a corresponding entry in the "Routes" dropdown or its sub-menus.
  - Verify "Account" and "Settings" routes are active and mapped.
  - **Success Criteria**: Every page registered in `App.jsx` must be reachable within 3 clicks from the MenuBar.

## 3. Automated Audit Execution (Phase 2)
### Tooling
- **Selenium Driver**: Chrome (Window-size 1920x1080).
- **Stabilization**: 7-second wait per page to allow widget data population.

### Detection
- **Error Checks**: Scan for "404", "Not Found", or React crashes.
- **Gold Standard Check**: Confirm presence of `.glass-panel` and `.glass-panel-header`.
- **Overlap Check**: Execute mathematical AABB intersection test on all widget containers.

## 4. One-by-One Remediation Protocol (Phase 3)
For every failure in `screenshots/1_14_26/fail/`:

1.  **Diagnosis**: Determine if the failure is CRASH (functional bug), EMPTY (lack of implementation), or IMPROPER (UI/UX non-compliance).
2.  **Implementation**:
    - **Frontend**: Implement/Refactor component to follow the `.glass-panel` architecture.
    - **Backend**: Ensure corresponding Python service/route is active and returning valid data.
    - **Integration**: verify data-binding via strictly typed services in `frontend2/src/services/`.
3.  **Verification**: 
    - Re-run targeted Selenium capture for that specific route.
    - Confirm layout is balanced and data is visible.
4.  **Promotion**:
    - Save initial screenshot to `success/` as `<Category>_<PageName>.png`.
    - **NEW STANDARD**: Save a second screenshot scrolled to the bottom as `<Category>_<PageName>_scrolled.png`.
    - **MANDATORY**: Delete the original failure from `fail/`.

