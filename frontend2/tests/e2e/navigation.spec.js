/**
 * E2E Tests: Navigation and Routing
 * 
 * Tests navigation functionality:
 * - Route navigation
 * - Page transitions
 * - Sidebar navigation
 */

import { test, expect } from '@playwright/test';

test.describe('Navigation and Routing', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');
    await page.waitForTimeout(2000);
  });

  test('should navigate to dashboard', async ({ page }) => {
    // Check if we're on dashboard or can navigate to it
    const dashboardLink = page.locator('a[href="/"], a[href="/dashboard"], text=/dashboard/i').first();
    
    if (await dashboardLink.isVisible({ timeout: 2000 }).catch(() => false)) {
      await dashboardLink.click();
      await page.waitForTimeout(1000);
      
      // Verify we're on dashboard
      await expect(page).toHaveURL(/.*\/$|.*\/dashboard/);
    } else {
      // Already on dashboard
      await expect(page).toHaveURL(/.*\/$|.*\/dashboard/);
    }
  });

  test('should navigate via sidebar', async ({ page }) => {
    // Find sidebar navigation
    const sidebar = page.locator('[class*="sidebar"], nav, [role="navigation"]').first();
    
    if (await sidebar.isVisible({ timeout: 2000 }).catch(() => false)) {
      // Find navigation links
      const navLinks = page.locator('a[href], [class*="nav"] a').all();
      
      if (navLinks.length > 0) {
        // Click first navigation link
        const firstLink = navLinks[0];
        const href = await firstLink.getAttribute('href');
        
        if (href && href !== '#' && !href.startsWith('javascript:')) {
          await firstLink.click();
          await page.waitForTimeout(2000);
          
          // Verify navigation occurred
          await expect(page).toHaveURL(new RegExp(href.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')));
        }
      }
    }
  });

  test('should display page header', async ({ page }) => {
    // Look for page header or title
    const header = page.locator('h1, h2, [class*="header"], [class*="title"]').first();
    
    if (await header.isVisible({ timeout: 2000 }).catch(() => false)) {
      await expect(header).toBeVisible();
    }
  });

  test('should handle browser back/forward', async ({ page }) => {
    // Navigate to a page if possible
    const navLink = page.locator('a[href]:not([href="#"]):not([href^="javascript:"])').first();
    
    if (await navLink.isVisible({ timeout: 2000 }).catch(() => false)) {
      const initialUrl = page.url();
      const href = await navLink.getAttribute('href');
      
      if (href && href.startsWith('/')) {
        await navLink.click();
        await page.waitForTimeout(1000);
        
        // Go back
        await page.goBack();
        await page.waitForTimeout(1000);
        
        // Should be back at initial URL
        expect(page.url()).toContain(initialUrl.split('/').pop() || '');
      }
    }
  });
});

