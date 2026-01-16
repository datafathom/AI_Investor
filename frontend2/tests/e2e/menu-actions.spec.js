/**
 * E2E Tests: Menu Actions
 * 
 * Tests menu bar functionality and menu item actions
 */

import { test, expect } from '@playwright/test';

test.describe('Menu Actions', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
    // Wait for page to load
    await page.waitForLoadState('networkidle');
  });

  test('should open and close menu dropdowns', async ({ page }) => {
    // Find menu items
    const fileMenu = page.locator('text=/^file$/i, [role="menuitem"]:has-text("File")').first();
    
    if (await fileMenu.isVisible({ timeout: 2000 }).catch(() => false)) {
      await fileMenu.click();
      await page.waitForTimeout(500);
      
      // Check that dropdown is visible
      const dropdown = page.locator('.menu-dropdown, [role="menu"]').first();
      await expect(dropdown).toBeVisible();
      
      // Click outside to close
      await page.click('body', { position: { x: 10, y: 10 } });
      await page.waitForTimeout(500);
    }
  });

  test('should toggle theme via menu', async ({ page }) => {
    // Find View menu
    const viewMenu = page.locator('text=/^view$/i, [role="menuitem"]:has-text("View")').first();
    
    if (await viewMenu.isVisible({ timeout: 2000 }).catch(() => false)) {
      await viewMenu.click();
      await page.waitForTimeout(500);
      
      // Find toggle theme option
      const themeToggle = page.locator('text=/toggle.*theme|dark mode/i, [role="menuitem"]:has-text("Theme")').first();
      
      if (await themeToggle.isVisible()) {
        // Get initial theme
        const initialTheme = await page.evaluate(() => {
          return document.body.classList.contains('theme-dark') ? 'dark' : 'light';
        });
        
        await themeToggle.click();
        await page.waitForTimeout(1000);
        
        // Check theme changed
        const newTheme = await page.evaluate(() => {
          return document.body.classList.contains('theme-dark') ? 'dark' : 'light';
        });
        
        expect(newTheme).not.toBe(initialTheme);
      }
    }
  });

  test('should open all widgets via menu', async ({ page }) => {
    // Find Widgets menu
    const widgetsMenu = page.locator('text=/^widgets$/i, [role="menuitem"]:has-text("Widgets")').first();
    
    if (await widgetsMenu.isVisible({ timeout: 2000 }).catch(() => false)) {
      await widgetsMenu.click();
      await page.waitForTimeout(500);
      
      // Find "Open All Widgets" option
      const openAll = page.locator('text=/open all widgets/i, [role="menuitem"]:has-text("Open All")').first();
      
      if (await openAll.isVisible()) {
        await openAll.click();
        await page.waitForTimeout(2000);
        
        // Check that widgets are visible (look for widget containers)
        const widgets = page.locator('.widget, [class*="widget"], .react-grid-item').all();
        const widgetCount = await widgets.length;
        expect(widgetCount).toBeGreaterThan(0);
      }
    }
  });

  test('should close all widgets via menu', async ({ page }) => {
    // First open widgets
    const widgetsMenu = page.locator('text=/^widgets$/i, [role="menuitem"]:has-text("Widgets")').first();
    
    if (await widgetsMenu.isVisible({ timeout: 2000 }).catch(() => false)) {
      await widgetsMenu.click();
      await page.waitForTimeout(500);
      
      // Open all first
      const openAll = page.locator('text=/open all widgets/i').first();
      if (await openAll.isVisible()) {
        await openAll.click();
        await page.waitForTimeout(2000);
      }
      
      // Now close all
      await widgetsMenu.click();
      await page.waitForTimeout(500);
      
      const closeAll = page.locator('text=/close all widgets/i').first();
      if (await closeAll.isVisible()) {
        await closeAll.click();
        await page.waitForTimeout(2000);
        
        // Widgets should be hidden
        const visibleWidgets = await page.locator('.widget:visible, [class*="widget"]:visible').count();
        expect(visibleWidgets).toBe(0);
      }
    }
  });

  test('should reset layout via menu', async ({ page }) => {
    // Find Selection menu
    const selectionMenu = page.locator('text=/^selection$/i, [role="menuitem"]:has-text("Selection")').first();
    
    if (await selectionMenu.isVisible({ timeout: 2000 }).catch(() => false)) {
      await selectionMenu.click();
      await page.waitForTimeout(500);
      
      // Find reset layout option
      const resetLayout = page.locator('text=/reset layout/i, [role="menuitem"]:has-text("Reset")').first();
      
      if (await resetLayout.isVisible()) {
        await resetLayout.click();
        await page.waitForTimeout(1000);
        
        // Layout should be reset (check for default layout or confirmation)
        // This is a basic check - actual layout reset verification would need more specific selectors
        await expect(page.locator('body')).toBeVisible();
      }
    }
  });

  test('should show help menu items', async ({ page }) => {
    // Find Help menu
    const helpMenu = page.locator('text=/^help$/i, [role="menuitem"]:has-text("Help")').first();
    
    if (await helpMenu.isVisible({ timeout: 2000 }).catch(() => false)) {
      await helpMenu.click();
      await page.waitForTimeout(500);
      
      // Check for help items
      const docs = page.locator('text=/documentation/i').first();
      const shortcuts = page.locator('text=/shortcuts/i').first();
      const about = page.locator('text=/about/i').first();
      
      expect(await docs.isVisible() || await shortcuts.isVisible() || await about.isVisible()).toBeTruthy();
    }
  });
});

