import { describe, it, expect, beforeEach } from 'vitest';
import useTaskbarStore, { calculateAgentMood } from '../taskbarStore';

describe('taskbarStore', () => {
    beforeEach(() => {
        // Reset store to initial state before each test
        useTaskbarStore.setState({
            isStartMenuOpen: false,
            activeWorkspace: 'Strategy',
            killSwitchState: 'inactive',
            systemMetrics: { kafkaThroughput: 0, cpuUsage: 0, memoryUsage: 0 },
            agentMoods: {},
            pinnedIcons: ['portfolio', 'terminal', 'agents']
        });
    });

    describe('Start Menu', () => {
        it('should toggle start menu open', () => {
            const { toggleStartMenu } = useTaskbarStore.getState();
            expect(useTaskbarStore.getState().isStartMenuOpen).toBe(false);
            
            toggleStartMenu();
            expect(useTaskbarStore.getState().isStartMenuOpen).toBe(true);
            
            toggleStartMenu();
            expect(useTaskbarStore.getState().isStartMenuOpen).toBe(false);
        });

        it('should close start menu', () => {
            useTaskbarStore.setState({ isStartMenuOpen: true });
            const { closeStartMenu } = useTaskbarStore.getState();
            
            closeStartMenu();
            expect(useTaskbarStore.getState().isStartMenuOpen).toBe(false);
        });
    });

    describe('Workspace Management', () => {
        it('should set active workspace', () => {
            const { setWorkspace } = useTaskbarStore.getState();
            
            setWorkspace('Research');
            expect(useTaskbarStore.getState().activeWorkspace).toBe('Research');
            
            setWorkspace('Admin');
            expect(useTaskbarStore.getState().activeWorkspace).toBe('Admin');
        });

        it('should have correct workspace groupings', () => {
            const { workspaceGroups } = useTaskbarStore.getState();
            
            expect(workspaceGroups.Research).toContain('analytics');
            expect(workspaceGroups.Strategy).toContain('portfolio');
            expect(workspaceGroups.Admin).toContain('terminal');
        });

        it('should get windows for current workspace', () => {
            const { getWorkspaceWindows, setWorkspace } = useTaskbarStore.getState();
            
            setWorkspace('Research');
            const researchWindows = useTaskbarStore.getState().getWorkspaceWindows();
            expect(researchWindows).toContain('analytics');
        });
    });

    describe('Kill Switch', () => {
        it('should transition through kill switch states', () => {
            const { startArming, cancelArming, triggerKillSwitch, resetKillSwitch } = useTaskbarStore.getState();
            
            expect(useTaskbarStore.getState().killSwitchState).toBe('inactive');
            
            startArming();
            expect(useTaskbarStore.getState().killSwitchState).toBe('arming');
            
            cancelArming();
            expect(useTaskbarStore.getState().killSwitchState).toBe('inactive');
            
            startArming();
            triggerKillSwitch();
            expect(useTaskbarStore.getState().killSwitchState).toBe('active');
            
            resetKillSwitch();
            expect(useTaskbarStore.getState().killSwitchState).toBe('inactive');
        });
    });

    describe('System Metrics', () => {
        it('should update system metrics', () => {
            const { updateMetrics } = useTaskbarStore.getState();
            
            updateMetrics({ kafkaThroughput: 1500, cpuUsage: 45 });
            
            const { systemMetrics } = useTaskbarStore.getState();
            expect(systemMetrics.kafkaThroughput).toBe(1500);
            expect(systemMetrics.cpuUsage).toBe(45);
            expect(systemMetrics.memoryUsage).toBe(0); // Unchanged
        });

        it('should merge metrics updates', () => {
            const { updateMetrics } = useTaskbarStore.getState();
            
            updateMetrics({ kafkaThroughput: 1000 });
            updateMetrics({ cpuUsage: 50 });
            
            const { systemMetrics } = useTaskbarStore.getState();
            expect(systemMetrics.kafkaThroughput).toBe(1000);
            expect(systemMetrics.cpuUsage).toBe(50);
        });
    });

    describe('Agent Moods', () => {
        it('should set agent mood directly', () => {
            const { setAgentMood } = useTaskbarStore.getState();
            
            setAgentMood('agent-1', 'happy');
            expect(useTaskbarStore.getState().agentMoods['agent-1']).toBe('happy');
            
            setAgentMood('agent-2', 'panic');
            expect(useTaskbarStore.getState().agentMoods['agent-2']).toBe('panic');
        });

        it('should update agent mood based on P&L and volatility', () => {
            const { updateAgentMood } = useTaskbarStore.getState();
            
            // Happy: high P&L, low volatility
            updateAgentMood('agent-1', 10, 20);
            expect(useTaskbarStore.getState().agentMoods['agent-1']).toBe('happy');
            
            // Panic: low P&L, high volatility
            updateAgentMood('agent-2', -10, 80);
            expect(useTaskbarStore.getState().agentMoods['agent-2']).toBe('panic');
        });
    });

    describe('Pinned Icons', () => {
        it('should pin a new icon', () => {
            const { pinIcon } = useTaskbarStore.getState();
            
            pinIcon('watchlist');
            expect(useTaskbarStore.getState().pinnedIcons).toContain('watchlist');
        });

        it('should not duplicate pinned icons', () => {
            const { pinIcon } = useTaskbarStore.getState();
            const initialLength = useTaskbarStore.getState().pinnedIcons.length;
            
            pinIcon('portfolio'); // Already pinned
            expect(useTaskbarStore.getState().pinnedIcons.length).toBe(initialLength);
        });

        it('should unpin an icon', () => {
            const { unpinIcon } = useTaskbarStore.getState();
            
            unpinIcon('terminal');
            expect(useTaskbarStore.getState().pinnedIcons).not.toContain('terminal');
        });
    });
});

describe('calculateAgentMood', () => {
    it('should return happy for high P&L and low volatility', () => {
        expect(calculateAgentMood(10, 20)).toBe('happy');
        expect(calculateAgentMood(6, 25)).toBe('happy');
    });

    it('should return neutral for moderate conditions', () => {
        expect(calculateAgentMood(3, 40)).toBe('neutral');
        expect(calculateAgentMood(0, 30)).toBe('neutral');
    });

    it('should return stressed for moderate losses or volatility', () => {
        expect(calculateAgentMood(-3, 40)).toBe('stressed');
        expect(calculateAgentMood(0, 55)).toBe('stressed');
    });

    it('should return panic for heavy losses and high volatility', () => {
        expect(calculateAgentMood(-10, 80)).toBe('panic');
        expect(calculateAgentMood(-6, 75)).toBe('panic');
    });

    it('should return aggressive for very high volatility', () => {
        expect(calculateAgentMood(0, 85)).toBe('aggressive');
        expect(calculateAgentMood(5, 90)).toBe('aggressive');
    });
});
