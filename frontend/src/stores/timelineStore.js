import { create } from 'zustand';

/**
 * Timeline Store - Manages the global event scrubber state.
 * Allows "Time Travel" debugging and historical strategy analysis.
 */
const useTimelineStore = create((set, get) => ({
    // State
    currentTime: Date.now(),
    isHistoricalMode: false,
    isPlaying: false,
    playbackSpeed: 1,
    events: [], // { id, timestamp, type: 'trade'|'news'|'risk', data }
    
    // UI State for D3
    zoomLevel: 1,
    selectionRange: [null, null], // [start, end] for scrubbing
    
    // Actions
    setCurrentTime: (time) => set({ 
        currentTime: time,
        isHistoricalMode: Math.abs(Date.now() - time) > 1000 // Enable historical if > 1s from now
    }),
    
    togglePlayback: () => set((state) => ({ isPlaying: !state.isPlaying })),
    
    setPlaybackSpeed: (speed) => set({ playbackSpeed: speed }),
    
    addEvents: (newEvents) => set((state) => ({ 
        events: [...state.events, ...newEvents].sort((a, b) => a.timestamp - b.timestamp) 
    })),
    
    clearEvents: () => set({ events: [] }),
    
    setHistoricalMode: (enabled) => set({ isHistoricalMode: enabled }),
    
    updateSelection: (range) => set({ selectionRange: range }),
    
    // Reset to "Live" mode
    goLive: () => set({ 
        currentTime: Date.now(), 
        isHistoricalMode: false,
        isPlaying: false 
    })
}));

export default useTimelineStore;
