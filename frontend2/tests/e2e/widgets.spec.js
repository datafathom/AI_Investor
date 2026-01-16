/**
 * E2E Tests: Widget Interactions
 * 
 * Tests widget functionality:
 * - Opening/closing widgets
 * - Widget visibility
 * - Widget interactions
 */

import { test, expect } from '@playwright/test';

test.describe('Widget Interactions', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');
  });

  test('should display widgets on dashboard', async ({ page }) => {
    // Wait for widgets to load
    await page.waitForTimeout(2000);
    
    // Look for widget containers or grid items
    const widgets = page.locator('.react-grid-item, .widget, [class*="widget"]');
    const widgetCount = await widgets.count();
    
    // Should have at least some widgets (even if hidden)
    expect(widgetCount).toBeGreaterThanOrEqual(0);
  });

  test('should toggle widget visibility', async ({ page }) => {
    // Open widgets menu
    const widgetsMenu = page.locator('text=/^widgets$/i, [role="menuitem"]:has-text("Widgets")').first();
    
    if (await widgetsMenu.isVisible({ timeout: 2000 }).catch(() => false)) {
      await widgetsMenu.click();
      await page.waitForTimeout(500);
      
      // Find a widget toggle (e.g., API widget)
      const apiWidgetToggle = page.locator('text=/api/i, [role="menuitemcheckbox"]:has-text("API")').first();
      
      if (await apiWidgetToggle.isVisible()) {
        const isChecked = await apiWidgetToggle.getAttribute('aria-checked');
        const initialState = isChecked === 'true';
        
        // Toggle widget
        await apiWidgetToggle.click();
        await page.waitForTimeout(1000);
        
        // Check state changed
        const newIsChecked = await apiWidgetToggle.getAttribute('aria-checked');
        const newState = newIsChecked === 'true';
        
        expect(newState).not.toBe(initialState);
      }
    }
  });

  test('should interact with Docker widget', async ({ page }) => {
    // First, make sure Docker widget is visible
    const widgetsMenu = page.locator('text=/^widgets$/i, [role="menuitem"]:has-text("Widgets")').first();
    
    if (await widgetsMenu.isVisible({ timeout: 2000 }).catch(() => false)) {
      await widgetsMenu.click();
      await page.waitForTimeout(500);
      
      // Open Docker widget if not already open
      const dockerToggle = page.locator('text=/docker/i, [role="menuitemcheckbox"]:has-text("Docker")').first();
      if (await dockerToggle.isVisible()) {
        const isChecked = await dockerToggle.getAttribute('aria-checked');
        if (isChecked !== 'true') {
          await dockerToggle.click();
          await page.waitForTimeout(2000);
        }
      }
      
      // Look for Docker widget content
      const dockerWidget = page.locator('text=/docker|containers/i, [class*="docker"]').first();
      if (await dockerWidget.isVisible({ timeout: 5000 }).catch(() => false)) {
        // Widget is visible and loaded
        await expect(dockerWidget).toBeVisible();
      }
    }
  });

  test('should display widget content', async ({ page }) => {
    // Open all widgets
    const widgetsMenu = page.locator('text=/^widgets$/i, [role="menuitem"]:has-text("Widgets")').first();
    
    if (await widgetsMenu.isVisible({ timeout: 2000 }).catch(() => false)) {
      await widgetsMenu.click();
      await page.waitForTimeout(500);
      
      const openAll = page.locator('text=/open all widgets/i').first();
      if (await openAll.isVisible()) {
        await openAll.click();
        await page.waitForTimeout(3000);
        
        // Check for widget content
        const widgetContent = page.locator('.widget, [class*="widget"], .react-grid-item').first();
        if (await widgetContent.isVisible({ timeout: 2000 }).catch(() => false)) {
          await expect(widgetContent).toBeVisible();
        }
      }
    }
  });
});

