# End-to-End Testing Guide

This guide explains how to run and maintain E2E tests for the AI Investor platform.

## Overview

E2E tests use Playwright to test critical user journeys across the entire application stack.

## Prerequisites

- Node.js 18+
- Python 3.9+
- Backend server running (port 5050)
- Frontend server running (port 3000)

## Running Tests

### Local Development

**Run all E2E tests:**
```bash
cd frontend2
npm run test:e2e
```

**Run specific test file:**
```bash
npm run test:e2e -- tests/e2e/auth.spec.js
```

**Run tests in headed mode (see browser):**
```bash
npm run test:e2e:headed
```

**Run tests matching pattern:**
```bash
npm run test:e2e -- --grep "Authentication"
```

### CI/CD

E2E tests run automatically on:
- Pull requests
- Main branch commits
- Manual workflow triggers

## Test Structure

### Test Files
- `tests/e2e/auth.spec.js` - Authentication & onboarding
- `tests/e2e/dashboard.spec.js` - Dashboard & navigation
- `tests/e2e/portfolio.spec.js` - Portfolio management
- `tests/e2e/trading.spec.js` - Trading flow

### Test Data Attributes

All interactive elements should have `data-testid` attributes:
```jsx
<button data-testid="login-button">Login</button>
<input data-testid="email-input" />
```

## Writing Tests

### Basic Test Structure

```javascript
import { test, expect } from '@playwright/test';

test.describe('Feature Name', () => {
  test('test description', async ({ page }) => {
    await page.goto('/');
    await expect(page.locator('[data-testid="element"]')).toBeVisible();
  });
});
```

### Best Practices

1. **Use data-testid**: Don't rely on CSS classes or text content
2. **Wait for elements**: Use `waitForSelector` for dynamic content
3. **Clean up**: Clear cookies/localStorage in `beforeEach`
4. **Isolate tests**: Each test should be independent
5. **Use meaningful names**: Test names should describe what they test

## Debugging

### View Test Results

```bash
npx playwright show-report
```

### Debug Mode

```bash
npx playwright test --debug
```

### Screenshots & Videos

Failed tests automatically capture:
- Screenshots
- Videos
- Traces

View in `test-results/` directory.

## CI Integration

Tests run in GitHub Actions on:
- Pull requests
- Main branch
- Scheduled (nightly)

Results are uploaded as artifacts.

## Troubleshooting

### Tests Fail Locally

1. Ensure backend is running: `python -m web.app`
2. Ensure frontend is running: `cd frontend2 && npm run dev`
3. Check test data: Verify test users exist
4. Check network: Ensure no firewall blocking

### Flaky Tests

- Add explicit waits
- Increase timeouts
- Check for race conditions
- Verify test data consistency

## Performance

### Test Execution Time
- Target: < 10 minutes for full suite
- Individual test: < 30 seconds

### Optimization
- Run tests in parallel
- Use test sharding
- Cache dependencies
- Reuse browser instances

## Next Steps

- [ ] Add more test coverage
- [ ] Add visual regression tests
- [ ] Add accessibility tests
- [ ] Add mobile device tests
