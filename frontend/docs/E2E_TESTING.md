# End-to-End Testing Documentation

## Overview

This project uses [Playwright](https://playwright.dev/) for End-to-End (E2E) testing. E2E tests verify that the entire application works correctly from a user's perspective.

## Quick Start

```bash
# Run all E2E tests
npm run test:e2e

# Run with UI (interactive mode)
npm run test:e2e:ui

# Run in headed mode (see browser)
npm run test:e2e:headed

# Run specific test file
npx playwright test tests/e2e/auth.spec.js

# Debug a test
npx playwright test --debug
```

## Test Structure

E2E tests are located in `tests/e2e/`:

- **auth.spec.js** - Authentication flow (register, login, logout, protected routes)
- **menu-actions.spec.js** - Menu bar functionality and menu item actions
- **widgets.spec.js** - Widget interactions (open/close, visibility, Docker widget)
- **layout.spec.js** - Layout management (drag & drop, resize, save/load layouts)
- **socketio.spec.js** - Real-time Socket.io features (chat, presence)
- **navigation.spec.js** - Navigation and routing tests

## Configuration

Playwright is configured in `playwright.config.js`:

- **Base URL**: `http://localhost:5176`
- **Browser**: Chromium (default)
- **Auto-start server**: Dev server starts automatically before tests
- **Retries**: 2 retries in CI, 0 in local development
- **Reporting**: HTML reports with screenshots and videos on failure

## Test Coverage

### Authentication Flow ✅
- Login modal display
- User registration
- User login
- User logout
- Protected route access

### Menu Actions ✅
- Menu dropdown open/close
- Theme toggling
- Open/close all widgets
- Reset layout
- Help menu items

### Widget Interactions ✅
- Widget display
- Widget visibility toggling
- Docker widget interaction
- Widget content display

### Layout Management ✅
- Widget grid display
- Drag and drop widgets
- Save layout
- Reset layout

### Real-time Features ✅
- Socket connection
- Chat interface
- Send chat messages

### Navigation ✅
- Dashboard navigation
- Sidebar navigation
- Page headers
- Browser back/forward

## Writing New Tests

Example test structure:

```javascript
import { test, expect } from '@playwright/test';

test.describe('Feature Name', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');
    await page.waitForTimeout(2000);
  });

  test('should do something', async ({ page }) => {
    // Find element
    const element = page.locator('selector');
    
    // Interact
    await element.click();
    
    // Assert
    await expect(element).toBeVisible();
  });
});
```

## Best Practices

1. **Wait for network idle** before interacting with elements
2. **Use specific selectors** - prefer data-testid attributes when available
3. **Handle async operations** - always use await
4. **Clean up state** - use beforeEach/afterEach hooks
5. **Use page.waitForTimeout() sparingly** - prefer waiting for specific elements
6. **Test user flows** - focus on what users actually do

## Debugging

### View Test Execution
```bash
npm run test:e2e:ui
```

### Debug Specific Test
```bash
npx playwright test --debug tests/e2e/auth.spec.js
```

### Run in Headed Mode
```bash
npm run test:e2e:headed
```

### View Test Report
After running tests, view the HTML report:
```bash
npx playwright show-report
```

## CI/CD Integration

E2E tests are configured for CI/CD:

- **Retries**: 2 retries on failure in CI
- **Workers**: 1 worker in CI for stability
- **Artifacts**: Screenshots and videos saved on failure
- **Reports**: HTML reports generated

## Troubleshooting

### Tests Fail to Start
- Ensure dev server can start on port 5176
- Check that backend server is running on port 3002
- Verify all dependencies are installed

### Selectors Not Found
- Use browser DevTools to inspect elements
- Check if elements are dynamically loaded (add waits)
- Verify data-testid attributes are present

### Timeout Issues
- Increase timeout in test configuration
- Add explicit waits for async operations
- Check network requests are completing

## Future Enhancements

Potential improvements:
- Visual regression testing
- Performance testing
- Cross-browser testing (Firefox, Safari)
- Mobile device testing
- Accessibility testing integration

## Resources

- [Playwright Documentation](https://playwright.dev/)
- [Playwright Best Practices](https://playwright.dev/docs/best-practices)
- [Playwright API Reference](https://playwright.dev/docs/api/class-playwright)

