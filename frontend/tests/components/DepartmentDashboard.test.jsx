import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen } from '@testing-library/react';
import React from 'react';
import DepartmentDashboard from '../../src/components/Departments/DepartmentDashboard';
import useDepartmentStore from '../../src/stores/departmentStore';
import { DEPT_REGISTRY } from '../../src/config/departmentRegistry';

// Mock the store
vi.mock('../../src/stores/departmentStore', () => ({
  default: vi.fn(),
}));

// Mock react-router-dom
vi.mock('react-router-dom', () => ({
  useParams: () => ({ slug: 'orchestrator' }),
}));

// Mock scrollIntoView for JSDOM
window.HTMLElement.prototype.scrollIntoView = vi.fn();

vi.mock('../../src/components/Common/PageContextPanel', () => ({
  default: ({ title }) => <div data-testid="page-context">{title}</div>,
}));

vi.mock('../../src/components/Departments/DepartmentActivityLog', () => ({
  default: () => <div data-testid="activity-log">Activity Log</div>,
}));

describe('DepartmentDashboard', () => {
  const mockSetActiveDepartment = vi.fn();
  const mockAddLogEntry = vi.fn();
  const mockPulse = {
    systemHealth: 'green',
    threatLevel: 'low',
    netWorth: 1000000,
    liquidityDays: 30,
  };

  const mockDepartments = {
    1: {
      id: 1,
      status: 'active',
      metrics: {
        latency: 120,
        throughput: 450,
      },
      lastUpdate: '2026-02-04T00:00:00Z',
    },
  };

  beforeEach(() => {
    vi.clearAllMocks();
    const state = {
      setActiveDepartment: mockSetActiveDepartment,
      addLogEntry: mockAddLogEntry,
      departments: mockDepartments,
      pulse: mockPulse,
      departmentLogs: { 1: [] },
    };
    
    useDepartmentStore.mockImplementation((selector) => {
      return typeof selector === 'function' ? selector(state) : state;
    });
  });

  it('renders correctly for a valid department', () => {
    render(<DepartmentDashboard deptId={1} />);

    // PageContextPanel is now rendered globally in App.jsx
    // expect(screen.getByTestId('page-context')).toHaveTextContent('The Orchestrator');
    
    // Check for agent fleet panel
    expect(screen.getByText('AGENT FLEET')).toBeInTheDocument();
    
    // Check for primary metric (assuming it's latency in registry for ID 1)
    expect(screen.getByText('SYSTEM LATENCY')).toBeInTheDocument();
    
    // Check for activity log
    expect(screen.getByTestId('activity-log')).toBeInTheDocument();
  });

  it('renders error state for invalid department', () => {
    render(<DepartmentDashboard deptId={999} />);
    expect(screen.getByText('Department 999 Not Found')).toBeInTheDocument();
  });

  it('calls setActiveDepartment on mount', () => {
    render(<DepartmentDashboard deptId={1} />);
    expect(mockSetActiveDepartment).toHaveBeenCalledWith(1);
  });
});
