import { create } from 'zustand';

/**
 * Agent mood states based on P&L and volatility
 * @typedef {'happy' | 'neutral' | 'stressed' | 'panic' | 'aggressive'} AgentMood
 */

/**
 * Calculate agent mood based on P&L percentage and volatility
 * @param {number} pnlPercent - P&L as percentage (-100 to +100)
 * @param {number} volatility - Volatility score (0 to 100)
 * @returns {AgentMood}
 */
export const calculateAgentMood = (pnlPercent, volatility) => {
    if (pnlPercent > 5 && volatility < 30) return 'happy';
    if (pnlPercent > 2 && volatility < 50) return 'neutral';
    if (pnlPercent < -5 && volatility > 70) return 'panic';
    if (volatility > 80) return 'aggressive';
    if (pnlPercent < -2 || volatility > 50) return 'stressed';
    return 'neutral';
};

const useTaskbarStore = create((set, get) => ({
    isStartMenuOpen: false,
    activeWorkspace: 'Strategy', // 'Research', 'Strategy', 'Admin'
    killSwitchState: 'inactive', // 'inactive', 'arming', 'active'
    isKillMFAOpen: false,
    isLockedDown: false,
    
    // System Metrics
    systemMetrics: {
        kafkaThroughput: 0,
        cpuUsage: 0,
        memoryUsage: 0
    },
    
    // Agent Moods - Maps agent ID to mood state
    agentMoods: {},
    
    // Pinned Icons - Persistent taskbar icons
    pinnedIcons: ['portfolio', 'terminal', 'agents'],
    
    // Workspace Groupings
    workspaceGroups: {
        Research: ['news-feed', 'analytics', 'watchlist'],
        Strategy: ['strategy-lab', 'portfolio', 'risk-scanner'],
        Admin: ['system-status', 'terminal', 'agent-control']
    },

    toggleStartMenu: () => set((state) => ({ isStartMenuOpen: !state.isStartMenuOpen })),
    closeStartMenu: () => set({ isStartMenuOpen: false }),
    
    setWorkspace: (workspace) => set({ activeWorkspace: workspace }),
    
    // Kill Switch Logic
    startArming: () => set({ killSwitchState: 'arming' }),
    cancelArming: () => set({ killSwitchState: 'inactive' }),
    triggerKillSwitch: () => set({ killSwitchState: 'active', isLockedDown: true }),
    resetKillSwitch: () => set({ killSwitchState: 'inactive', isLockedDown: false }),
    setKillMFAOpen: (isOpen) => set({ isKillMFAOpen: isOpen }),
    toggleLockdown: (locked) => set({ isLockedDown: locked }),
    updateMetrics: (metrics) => set((state) => ({ 
        systemMetrics: { ...state.systemMetrics, ...metrics } 
    })),
    
    // Agent Mood Actions
    updateAgentMood: (agentId, pnlPercent, volatility) => {
        const mood = calculateAgentMood(pnlPercent, volatility);
        set((state) => ({
            agentMoods: { ...state.agentMoods, [agentId]: mood }
        }));
    },
    
    setAgentMood: (agentId, mood) => set((state) => ({
        agentMoods: { ...state.agentMoods, [agentId]: mood }
    })),
    
    // Pinned Icons Actions
    pinIcon: (iconId) => set((state) => ({
        pinnedIcons: state.pinnedIcons.includes(iconId) 
            ? state.pinnedIcons 
            : [...state.pinnedIcons, iconId]
    })),
    
    unpinIcon: (iconId) => set((state) => ({
        pinnedIcons: state.pinnedIcons.filter(id => id !== iconId)
    })),
    
    // Get windows for current workspace
    getWorkspaceWindows: () => {
        const { activeWorkspace, workspaceGroups } = get();
        return workspaceGroups[activeWorkspace] || [];
    }
}));

export default useTaskbarStore;

