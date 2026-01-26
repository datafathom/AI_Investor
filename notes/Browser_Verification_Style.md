# Browser Verification Style: The LLM QA Protocol

This document defines how LLM coders and QA engineers must verify UI/UX changes. Traditional manual browsing is forbidden; all verification must be scriptable, repeatable, and mathematically sound.

---

## 1. The "Robust Selenium" Pattern
Always use a local Python script with Selenium for verification. Do not rely on internal agent browser tools for complex flows.

### Essential Setup:
- **Service**: Use `webdriver_manager` for automatic driver handling.
- **Scaling**: Set window size to `1920, 1080` to match standard developer environments.
- **Wait Policy**: Use `WebDriverWait` with `EC` (Expected Conditions). Never use hard `time.sleep()` for element detection.

## 2. Authentic Traceability & Verification (MANDATORY)
LLM coders must NOT use `localStorage` bypasses for authentication. All verification must use real, date-stamped accounts to ensure traceability and state integrity.

### The Auth Protocol:
1.  **Registration**: Trigger the registration modal via UI interaction.
2.  **Date-Stamped Identity**: Use the format `audit_YYYY_MM_DD_HHMMSS@fathom.ai`.
3.  **Programmatic Verification**: After registration, use a background `requests` call to the server's verification endpoint to bypass manual email checks.
4.  **UI Login**: Perform the final login sequence through the browser UI.

```python
# 1. Register via UI
driver.find_element(By.NAME, "email").send_keys(TEST_EMAIL)
driver.find_element(By.NAME, "password").send_keys(TEST_PASS)
driver.find_element(By.CLASS_NAME, "auth-button").click()

# 2. Verify via API (Backend Bypass)
import requests
requests.get(f"http://localhost:5050/api/auth/verify-email?email={TEST_EMAIL}&token=mock_verify_token")

# 3. Login via UI
driver.find_element(By.NAME, "email").send_keys(TEST_EMAIL)
driver.find_element(By.NAME, "password").send_keys(TEST_PASS)
driver.find_element(By.CLASS_NAME, "auth-button").click()
```

## 3. Mathematical Layout Validation
Don't just look at the screen—measure it. To detect overlap (stacking), use the **AABB Intersection Test** on widget containers.

### Overlap Detection Logic:
1.  Find all elements with the `.widget-container` or `.rounded-xl` class.
2.  Extract their `getBoundingClientRect()` using `execute_script`.
3.  Compare every pair:
    ```python
    if (r1['left'] < r2['right'] and r1['right'] > r2['left'] and
        r1['top'] < r2['bottom'] and r1['bottom'] > r2['top']):
        raise Exception("OVERLAP DETECTED")
    ```

## 4. Visual Evidence Protocol
Every verification script MUST capture a full-page screenshot.
- **Path**: `screenshots/VERIFY_[FEATURE_NAME].png`
- **Verification Sign-off**: Before claiming a task is done, the LLM must confirm the screenshot exists and contains the expected data markers (e.g., "Found 'Strike' in Options Chain").

## 5. Identifying the "Gold Standard"
When verifying layout, the script must check for the presence of:
- **`.os-bleed` Class**: On the `main` tag (proves route registry is correct).
- **`.glass-panel-header`**: Proves the widget is using the standardized drag handle.
- **Internal Scroll**: Verify the content wrapper has `overflow-y: auto`.

## 6. Testing User Profile
If a specific user state is required, use the `/api/v1/auth/register` and `/api/v1/auth/verify` endpoints directly via `requests` inside the python script before starting the browser. This ensures a clean slate for every test run.

---
**Standard REFERENCE SCRIPT**: `scripts/robust_verify.py`
