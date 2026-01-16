# E2E Testing with Playwright

This directory contains End-to-End (E2E) tests using Playwright.

## Setup

E2E tests are already configured. To run them:

```bash
# Run all E2E tests
npm run test:e2e

# Run E2E tests with UI
npm run test:e2e:ui

# Run E2E tests in headed mode (see browser)
npm run test:e2e:headed
```

## Test Files

- `auth.spec.js` - Authentication flow tests (register, login, logout)
- `menu-actions.spec.js` - Menu bar and menu item tests
- `widgets.spec.js` - Widget interaction tests
- `layout.spec.js` - Layout management tests (drag, resize, save/load)
- `socketio.spec.js` - Real-time Socket.io feature tests

## Configuration

E2E tests are configured in `playwright.config.js` at the project root.

The configuration:
- Starts the dev server automatically before tests
- Uses Chromium by default
- Generates HTML reports
- Captures screenshots and videos on failure

## Writing Tests

Example test structure:

```javascript
import { test, expect } from '@playwright/test';

test.describe('Feature Name', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');
  });

  test('should do something', async ({ page }) => {
    // Test implementation
    await expect(page.locator('selector')).toBeVisible();
  });
});
```

## Best Practices

1. **Use data-testid attributes** when possible for stable selectors
2. **Wait for network idle** before interacting with elements
3. **Use page.waitForTimeout()** sparingly - prefer waiting for specific elements
4. **Handle async operations** properly with await
5. **Clean up state** in beforeEach/afterEach hooks

## Debugging

To debug a failing test:

```bash
# Run specific test file
npx playwright test tests/e2e/auth.spec.js

# Run in headed mode with devtools
npx playwright test --headed --debug

# Use Playwright Inspector
npx playwright test --debug
```

## CI/CD Integration

E2E tests can be integrated into CI/CD pipelines. The config already supports CI mode with retries and proper reporting.

