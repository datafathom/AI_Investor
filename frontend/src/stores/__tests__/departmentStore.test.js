/**
 * Department Store Tests
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';
import useDepartmentStore from '../departmentStore';
import apiClient from '../../services/apiClient';
import presenceService from '../../services/presenceService';

// Mock apiClient
vi.mock('../../services/apiClient', () => ({
  default: {
    get: vi.fn(),
    post: vi.fn(),
  },
}));

// Mock presenceService
vi.mock('../../services/presenceService', () => ({
  default: {
    on: vi.fn(),
    off: vi.fn(),
    emit: vi.fn(),
  },
}));

// Capture initial state for resetting
const initialState = useDepartmentStore.getState();

describe('departmentStore', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    // Reset store state to initial
    useDepartmentStore.setState({
      activeDepartment: null,
      vennIntersection: null,
      departmentLogs: {},
      error: null,
      isLoading: false,
      // We don't reset 'departments' fully here as it's a large static-ish object,
      // but if a test modifies it, it should be careful.
      // However, for total isolation:
      departments: initialState.departments
    });
  });

  it('should initialize with 18 departments', () => {
    const state = useDepartmentStore.getState();
    expect(Object.keys(state.departments)).toHaveLength(18);
    expect(state.departments[1].name).toBe('Orchestrator');
    expect(state.departments[18].name).toBe('Banker');
  });

  it('should set active department', () => {
    useDepartmentStore.getState().setActiveDepartment(5);
    expect(useDepartmentStore.getState().activeDepartment).toBe(5);
    expect(useDepartmentStore.getState().vennIntersection).toBeNull();
  });

  it('should warn and not set invalid department ID', () => {
    const consoleSpy = vi.spyOn(console, 'warn').mockImplementation(() => {});
    useDepartmentStore.getState().setActiveDepartment(999);
    expect(useDepartmentStore.getState().activeDepartment).toBeNull();
    expect(consoleSpy).toHaveBeenCalled();
    consoleSpy.mockRestore();
  });

  it('should add and cap log entries', () => {
    const deptId = 1;
    const store = useDepartmentStore.getState();
    
    // Add 60 logs
    for (let i = 0; i < 60; i++) {
        useDepartmentStore.getState().addLogEntry(deptId, { message: `Log ${i}` });
    }
    
    const logs = useDepartmentStore.getState().departmentLogs[deptId];
    expect(logs).toHaveLength(50);
    expect(logs[0].message).toBe('Log 59'); // Last added should be first due to unshift-like behavior
  });

  it('should clear logs', () => {
    const deptId = 1;
    useDepartmentStore.getState().addLogEntry(deptId, { message: 'Test' });
    expect(useDepartmentStore.getState().departmentLogs[deptId]).toHaveLength(1);
    
    useDepartmentStore.getState().clearLogs(deptId);
    expect(useDepartmentStore.getState().departmentLogs[deptId]).toHaveLength(0);
  });

  it('should trigger Venn mode with blend color', () => {
    const dept1 = 1; // Orchestrator (#00f2ff)
    const dept2 = 5; // Trader (#22c55e)
    
    useDepartmentStore.getState().triggerVennMode(dept1, dept2);
    
    const venn = useDepartmentStore.getState().vennIntersection;
    expect(venn.dept1).toBe(dept1);
    expect(venn.dept2).toBe(dept2);
    expect(venn.blendColor).toBeDefined();
    expect(venn.blendColor).toMatch(/^#[0-9a-f]{6}$/);
    expect(useDepartmentStore.getState().activeDepartment).toBeNull();
  });

  it('should exit Venn mode', () => {
    useDepartmentStore.getState().triggerVennMode(1, 5);
    useDepartmentStore.getState().exitVennMode();
    expect(useDepartmentStore.getState().vennIntersection).toBeNull();
  });

  it('should update department metrics', () => {
    const deptId = 1;
    const newMetrics = { systemLatency: 42 };
    
    useDepartmentStore.getState().updateDepartmentMetrics(deptId, newMetrics);
    
    const dept = useDepartmentStore.getState().departments[deptId];
    expect(dept.metrics.systemLatency).toBe(42);
    expect(dept.lastUpdate).toBeDefined();
  });

  it('should fetch departments successfully', async () => {
    const mockDepts = [
        { id: 1, status: 'busy', metrics: { systemLatency: 100 } },
        { id: 2, status: 'active', metrics: { onTrackPercent: 95 } }
    ];
    apiClient.get.mockResolvedValueOnce(mockDepts);
    
    await useDepartmentStore.getState().fetchDepartments();
    
    expect(apiClient.get).toHaveBeenCalledWith('/departments');
    expect(useDepartmentStore.getState().departments[1].status).toBe('busy');
    expect(useDepartmentStore.getState().departments[1].metrics.systemLatency).toBe(100);
    expect(useDepartmentStore.getState().departments[1].name).toBe('Orchestrator'); // Static data preserved
  });

  it('should handle fetch error', async () => {
    apiClient.get.mockRejectedValueOnce(new Error('Network error'));
    
    await useDepartmentStore.getState().fetchDepartments();
    
    expect(useDepartmentStore.getState().error).toBe('Network error');
    expect(useDepartmentStore.getState().isLoading).toBe(false);
  });

  it('should invoke agent and add logs', async () => {
    const deptId = 1;
    const agentId = 'agent-001';
    const payload = { task: 'test' };
    const mockResponse = { response: 'Hello' };
    
    apiClient.post.mockResolvedValueOnce(mockResponse);
    
    await useDepartmentStore.getState().invokeAgent(deptId, agentId, payload);
    
    expect(apiClient.post).toHaveBeenCalled();
    const logs = useDepartmentStore.getState().departmentLogs[deptId];
    expect(logs.some(l => l.type === 'agent_call')).toBe(true);
    expect(logs.some(l => l.message === 'Hello')).toBe(true);
  });

  it('should filter departments by quadrant', () => {
    const attackDepts = useDepartmentStore.getState().getDepartmentsByQuadrant('ATTACK');
    expect(attackDepts.every(d => d.quadrant === 'ATTACK')).toBe(true);
    expect(attackDepts.length).toBeGreaterThan(0);
  });
});
