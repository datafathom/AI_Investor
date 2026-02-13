import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import { vi, describe, it, expect } from 'vitest';

/**
 * Admin Navigation Dropdown Test
 *
 * Verifies that the admin dropdown ("Admin Controls") appears in the
 * Routes menu ONLY when the currentUser has role='admin' and username='admin'.
 * This is a critical security and UX regression test.
 */

// Mock dependencies that MenuBar imports
vi.mock('../config/iconRegistry', () => ({
    getIcon: vi.fn(() => () => null)
}));

vi.mock('../services/apiClient', () => ({
    default: { get: vi.fn(() => Promise.resolve([])) }
}));

vi.mock('../components/admin/EnvVarsModal', () => ({
    default: () => <div>EnvVarsModal</div>
}));

import MenuBar from '../components/Navigation/MenuBar';
import { DEPT_REGISTRY } from '../config/departmentRegistry';

/** Helper: renders MenuBar inside a Router context and opens Routes dropdown */
const renderMenuBar = (currentUser) => {
    const defaultProps = {
        onMenuAction: vi.fn(),
        isDarkMode: false,
        widgetVisibility: {},
        onToggleWidget: vi.fn(),
        onTriggerModal: vi.fn(),
        onResetLayout: vi.fn(),
        toggleTheme: vi.fn(),
        onAutoSort: vi.fn(),
        onSaveLayout: vi.fn(),
        onLoadLayout: vi.fn(),
        onToggleLogCenter: vi.fn(),
        showLogCenter: false,
        debugStates: {},
        widgetTitles: {},
        onLogout: vi.fn(),
        onSignin: vi.fn(),
        globalLock: false,
        activeWorkspace: null,
        workspaces: [],
        onLoadWorkspace: vi.fn(),
        onSaveWorkspacePrompt: vi.fn(),
        currentUser,
    };
    return render(
        <MemoryRouter>
            <MenuBar {...defaultProps} />
        </MemoryRouter>
    );
};

describe('Admin Navigation Dropdown Visibility', () => {

    it('shows Admin Controls in Routes dropdown when logged in as admin user', () => {
        renderMenuBar({ id: 1, username: 'admin', role: 'admin', email: 'admin@aiinvestor.com' });

        // Click the Routes menu to open its dropdown
        const routesMenu = screen.getByText('Routes');
        fireEvent.click(routesMenu);

        // Admin Controls should now be visible inside the dropdown
        expect(screen.getByText(/Admin Controls/i)).toBeTruthy();
    });

    it('does NOT show Admin Controls in Routes for non-admin user', () => {
        renderMenuBar({ id: 2, username: 'trader', role: 'user', email: 'trader@test.com' });

        const routesMenu = screen.getByText('Routes');
        fireEvent.click(routesMenu);

        expect(screen.queryByText(/Admin Controls/i)).toBeNull();
    });

    it('does NOT show Admin Controls when no user is logged in', () => {
        renderMenuBar(null);

        const routesMenu = screen.getByText('Routes');
        fireEvent.click(routesMenu);

        expect(screen.queryByText(/Admin Controls/i)).toBeNull();
    });

    it('verifies DEPT_REGISTRY[19] contains the admin department', () => {
        const adminDept = DEPT_REGISTRY[19];
        expect(adminDept).toBeDefined();
        expect(adminDept.slug).toBe('admin');
        expect(adminDept.minRole).toBe('admin');
        expect(adminDept.subModules.length).toBeGreaterThan(0);
    });

    it('admin department has correct sub-modules for dropdown', () => {
        const adminDept = DEPT_REGISTRY[19];
        const subLabels = adminDept.subModules.map(m => m.label);
        expect(subLabels).toContain('System Logs Viewer');
        expect(subLabels).toContain('Event Bus Monitor');
        expect(subLabels).toContain('Storage Manager');
    });
});
