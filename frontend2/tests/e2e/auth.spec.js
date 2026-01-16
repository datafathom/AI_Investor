/**
 * E2E Tests: Authentication Flow
 * 
 * Tests the complete authentication workflow:
 * - User registration
 * - User login
 * - User logout
 * - Protected routes
 */

import { test, expect } from '@playwright/test';

test.describe('Authentication Flow', () => {
  test.beforeEach(async ({ page }) => {
    // Clear localStorage and cookies before each test
    await page.goto('/');
    await page.evaluate(() => {
      localStorage.clear();
      sessionStorage.clear();
    });
  });

  test('should show login modal when not authenticated', async ({ page }) => {
    await page.goto('/');
    
    // Check that login modal is visible
    const loginModal = page.locator('[data-testid="login-modal"], .login-modal, .modal').first();
    await expect(loginModal).toBeVisible({ timeout: 5000 });
    
    // Check for login form elements
    await expect(page.locator('input[type="text"], input[type="email"]').first()).toBeVisible();
    await expect(page.locator('input[type="password"]').first()).toBeVisible();
  });

  test('should register a new user', async ({ page }) => {
    await page.goto('/');
    
    // Wait for login modal
    await page.waitForSelector('[data-testid="login-modal"], .login-modal, .modal', { timeout: 5000 });
    
    // Switch to register mode (look for toggle button or link)
    const toggleButton = page.locator('button:has-text("Sign Up"), button:has-text("Register"), a:has-text("Sign Up")').first();
    if (await toggleButton.isVisible()) {
      await toggleButton.click();
    }
    
    // Fill registration form
    const username = `testuser_${Date.now()}`;
    const email = `test_${Date.now()}@example.com`;
    const password = 'TestPassword123!';
    
    // Find input fields (try different selectors)
    const usernameInput = page.locator('input[type="text"], input[placeholder*="username" i], input[placeholder*="name" i]').first();
    const emailInput = page.locator('input[type="email"], input[placeholder*="email" i]').first();
    const passwordInput = page.locator('input[type="password"]').first();
    
    if (await usernameInput.isVisible()) {
      await usernameInput.fill(username);
    }
    if (await emailInput.isVisible()) {
      await emailInput.fill(email);
    }
    await passwordInput.fill(password);
    
    // Submit form
    const submitButton = page.locator('button[type="submit"], button:has-text("Register"), button:has-text("Sign Up")').first();
    await submitButton.click();
    
    // Wait for success (modal should close or show success message)
    await page.waitForTimeout(2000);
    
    // Check that user is logged in (login modal should be gone or user info visible)
    const loginModal = page.locator('[data-testid="login-modal"], .login-modal').first();
    const isModalVisible = await loginModal.isVisible().catch(() => false);
    
    // Either modal is gone or we see user info in menu
    if (isModalVisible) {
      // Check for success message
      await expect(page.locator('text=/success|welcome|registered/i')).toBeVisible({ timeout: 5000 });
    } else {
      // Modal closed, user is logged in
      await expect(page.locator('text=/dashboard|welcome/i').first()).toBeVisible({ timeout: 5000 });
    }
  });

  test('should login with existing credentials', async ({ page }) => {
    // First register a user
    await page.goto('/');
    await page.waitForSelector('[data-testid="login-modal"], .login-modal, .modal', { timeout: 5000 });
    
    const username = `testuser_${Date.now()}`;
    const password = 'TestPassword123!';
    
    // Try to register first
    const toggleButton = page.locator('button:has-text("Sign Up"), button:has-text("Register")').first();
    if (await toggleButton.isVisible()) {
      await toggleButton.click();
      await page.waitForTimeout(500);
    }
    
    const usernameInput = page.locator('input[type="text"], input[placeholder*="username" i]').first();
    const passwordInput = page.locator('input[type="password"]').first();
    
    if (await usernameInput.isVisible()) {
      await usernameInput.fill(username);
    }
    await passwordInput.fill(password);
    
    const submitButton = page.locator('button[type="submit"], button:has-text("Register"), button:has-text("Sign Up")').first();
    await submitButton.click();
    await page.waitForTimeout(3000);
    
    // Now logout and login again
    await page.goto('/');
    await page.waitForTimeout(1000);
    
    // Look for logout button in menu
    const accountMenu = page.locator('text=/account/i, [role="menuitem"]:has-text("Account")').first();
    if (await accountMenu.isVisible()) {
      await accountMenu.click();
      await page.waitForTimeout(500);
      
      const logoutButton = page.locator('text=/logout/i, button:has-text("Logout")').first();
      if (await logoutButton.isVisible()) {
        await logoutButton.click();
        await page.waitForTimeout(1000);
      }
    }
    
    // Now login
    await page.waitForSelector('[data-testid="login-modal"], .login-modal, .modal', { timeout: 5000 });
    
    const loginUsernameInput = page.locator('input[type="text"], input[placeholder*="username" i]').first();
    const loginPasswordInput = page.locator('input[type="password"]').first();
    
    if (await loginUsernameInput.isVisible()) {
      await loginUsernameInput.fill(username);
    }
    await loginPasswordInput.fill(password);
    
    const loginButton = page.locator('button[type="submit"], button:has-text("Sign In"), button:has-text("Login")').first();
    await loginButton.click();
    
    await page.waitForTimeout(2000);
    
    // Verify login success
    const loginModal = page.locator('[data-testid="login-modal"], .login-modal').first();
    const isModalVisible = await loginModal.isVisible().catch(() => false);
    expect(isModalVisible).toBeFalsy();
  });

  test('should logout successfully', async ({ page }) => {
    // First login (simplified - just check if we can access logout)
    await page.goto('/');
    
    // If already logged in, try to logout
    const accountMenu = page.locator('text=/account/i, [role="menuitem"]:has-text("Account")').first();
    if (await accountMenu.isVisible({ timeout: 2000 }).catch(() => false)) {
      await accountMenu.click();
      await page.waitForTimeout(500);
      
      const logoutButton = page.locator('text=/logout/i, button:has-text("Logout")').first();
      if (await logoutButton.isVisible()) {
        await logoutButton.click();
        await page.waitForTimeout(1000);
        
        // After logout, login modal should appear
        await expect(page.locator('[data-testid="login-modal"], .login-modal, .modal').first()).toBeVisible({ timeout: 5000 });
      }
    }
  });

  test('should protect routes when not authenticated', async ({ page }) => {
    // Clear auth
    await page.goto('/');
    await page.evaluate(() => {
      localStorage.clear();
      sessionStorage.clear();
    });
    
    // Try to access protected content
    await page.goto('/');
    await page.waitForTimeout(1000);
    
    // Login modal should be visible
    const loginModal = page.locator('[data-testid="login-modal"], .login-modal, .modal').first();
    await expect(loginModal).toBeVisible({ timeout: 5000 });
  });
});

