# Verifying Frontend Work: Battle-Hardened Standards

To ensure the stability of our authed frontend, we follow a rigorous "First Run Debug" protocol for all routes and components. This prevents fragile verification scripts and ensures console errors are caught and correlated with backend logs.

## 1. The Verification Protocol

All verification scripts must inherit from `BaseVerifier` (`scripts/util/base_verifier.py`) and follow these steps:

1.  **Robust Authentication**:
    *   Do NOT use hardcoded waits for login.
    *   Wait explicitly for the `MenuBar` (`.menu-bar-container`) to be present before proceeding.
    *   Use `.env` credentials for testing accounts.
2.  **State-Aware Waiting**:
    *   After navigating to a URL, wait at least **2 seconds** for initial animations/data fetching.
    *   Wait for critical route markers (e.g., specific page headings or widget containers).
3.  **Error Deep-Dive**:
    *   **Console Logs**: Capture all `SEVERE` and `ERROR` browser logs.
    *   **Backend Logs**: Correlate browser errors with the last 50 lines of `logs/backend_debug.log`.
    *   **UI Artifacts**: Check for common failure strings like `NOT FOUND`, `ERROR:`, or `UNCAUGHT`.
4.  **Reporting & Screenshots**:
    *   Save screenshots for EVERY attempt (success or failure).
    *   Storage Path: `DEBUGGING/FrontEndAudit/Screenshots_FrontEndAudit/<MM_DD_YY>/`
    *   Result Catalog: `DEBUGGING/FrontEndAudit/results/<MM_DD_YY>_verify_results.json`

## 2. Using the Verification Tools

### Batch Route Verification
Use `scripts/verify_routes_batch.py` to audit multiple routes with automatic retry logic.

```powershell
# Run with default routes
python scripts/verify_routes_batch.py

# Run with custom routes and increased retries
python scripts/verify_routes_batch.py --routes /portfolio/crypto /analytics/options --retries 10

# Run from a routes file
python scripts/verify_routes_batch.py --file docs/_PLANS/Services_Mapped_To_Frontend_Pages/_NEW_ROUTES.txt
```

### Writing Custom Verifiers
Inherit from `BaseVerifier` for complex component-specific testing:

```python
from scripts.util.base_verifier import BaseVerifier

class MyComponentVerifier(BaseVerifier):
    def test_flow(self):
        self.robust_login("http://127.0.0.1:5173", "email", "pass")
        # Custom interaction logic here
        self.verify_route("/my-complex-route")
```

## 3. Failure Policy
*   **8-Attempt Rule**: If a route fails for over 8 consecutive attempts (even after manual fixes), label it as **FAILED**.
*   **Documentation Requirement**: Every failure MUST have a corresponding JSON entry with console errors and a screenshot.
*   **Hand-off**: Failed routes are queued for senior team review with the provided debug metadata.


