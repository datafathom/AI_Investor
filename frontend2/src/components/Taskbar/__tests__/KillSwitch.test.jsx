import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen, fireEvent, act } from '@testing-library/react';
import KillSwitch from '../KillSwitch';
import useTaskbarStore from '../../../stores/taskbarStore';

// Mock the taskbar store
vi.mock('../../../stores/taskbarStore', () => ({
    default: vi.fn()
}));

describe('KillSwitch Component', () => {
    const mockStartArming = vi.fn();
    const mockCancelArming = vi.fn();
    const mockTriggerKillSwitch = vi.fn();
    const mockResetKillSwitch = vi.fn();
    const mockSetKillMFAOpen = vi.fn();

    beforeEach(() => {
        vi.clearAllMocks();
        vi.useFakeTimers();
        
        useTaskbarStore.mockReturnValue({
            killSwitchState: 'inactive',
            startArming: mockStartArming,
            cancelArming: mockCancelArming,
            triggerKillSwitch: mockTriggerKillSwitch,
            resetKillSwitch: mockResetKillSwitch,
            setKillMFAOpen: mockSetKillMFAOpen
        });
    });

    afterEach(() => {
        vi.useRealTimers();
    });

    it('should render the kill switch button', () => {
        render(<KillSwitch />);
        const killSwitch = document.querySelector('.kill-switch-container');
        expect(killSwitch).toBeTruthy();
    });

    it('should start arming on mouse down', () => {
        render(<KillSwitch />);
        const killSwitch = document.querySelector('.kill-switch-container');
        
        fireEvent.mouseDown(killSwitch);
        
        expect(mockStartArming).toHaveBeenCalled();
    });

    it('should cancel arming on mouse up before timeout', () => {
        render(<KillSwitch />);
        const killSwitch = document.querySelector('.kill-switch-container');
        
        fireEvent.mouseDown(killSwitch);
        
        // Wait 1 second (before 3s threshold)
        act(() => {
            vi.advanceTimersByTime(1000);
        });
        
        fireEvent.mouseUp(killSwitch);
        
        expect(mockCancelArming).toHaveBeenCalled();
        expect(mockTriggerKillSwitch).not.toHaveBeenCalled();
    });

    it('should trigger MFA request after 3 second hold', () => {
        render(<KillSwitch />);
        const killSwitch = document.querySelector('.kill-switch-container');
        
        fireEvent.mouseDown(killSwitch);
        
        // Wait full 3 seconds
        act(() => {
            vi.advanceTimersByTime(3000);
        });
        
        expect(mockSetKillMFAOpen).toHaveBeenCalledWith(true);
        expect(mockTriggerKillSwitch).not.toHaveBeenCalled();
    });

    it('should cancel arming on mouse leave', () => {
        render(<KillSwitch />);
        const killSwitch = document.querySelector('.kill-switch-container');
        
        fireEvent.mouseDown(killSwitch);
        
        act(() => {
            vi.advanceTimersByTime(500);
        });
        
        fireEvent.mouseLeave(killSwitch);
        
        expect(mockCancelArming).toHaveBeenCalled();
    });

    it('should reset kill switch when clicked in active state', () => {
        useTaskbarStore.mockReturnValue({
            killSwitchState: 'active',
            startArming: mockStartArming,
            cancelArming: mockCancelArming,
            triggerKillSwitch: mockTriggerKillSwitch,
            resetKillSwitch: mockResetKillSwitch
        });

        render(<KillSwitch />);
        const killSwitch = document.querySelector('.kill-switch-container');
        
        fireEvent.mouseDown(killSwitch);
        
        expect(mockResetKillSwitch).toHaveBeenCalled();
        expect(mockStartArming).not.toHaveBeenCalled();
    });

    it('should show skull icon in active state', () => {
        useTaskbarStore.mockReturnValue({
            killSwitchState: 'active',
            startArming: mockStartArming,
            cancelArming: mockCancelArming,
            triggerKillSwitch: mockTriggerKillSwitch,
            resetKillSwitch: mockResetKillSwitch
        });

        render(<KillSwitch />);
        
        // Check that the container has the 'active' class
        const killSwitch = document.querySelector('.kill-switch-container.active');
        expect(killSwitch).toBeTruthy();
    });
});
