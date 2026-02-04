import { describe, it, expect, beforeEach, vi } from 'vitest';
import useTimelineStore from '../timelineStore';

describe('TimelineStore', () => {
    beforeEach(() => {
        useTimelineStore.setState({
            currentTime: Date.now(),
            isHistoricalMode: false,
            isPlaying: false,
            playbackSpeed: 1,
            events: [],
            selectionRange: [null, null]
        });
    });

    it('should set current time and enable historical mode', () => {
        const historicalTime = Date.now() - 10000; // 10s ago
        useTimelineStore.getState().setCurrentTime(historicalTime);
        
        expect(useTimelineStore.getState().currentTime).toBe(historicalTime);
        expect(useTimelineStore.getState().isHistoricalMode).toBe(true);
    });

    it('should toggle playback state', () => {
        expect(useTimelineStore.getState().isPlaying).toBe(false);
        useTimelineStore.getState().togglePlayback();
        expect(useTimelineStore.getState().isPlaying).toBe(true);
    });

    it('should add and sort events by timestamp', () => {
        const event1 = { id: 1, timestamp: 200, type: 'trade' };
        const event2 = { id: 2, timestamp: 100, type: 'news' };
        
        useTimelineStore.getState().addEvents([event1, event2]);
        
        const events = useTimelineStore.getState().events;
        expect(events).toHaveLength(2);
        expect(events[0].id).toBe(2); // Sorted by timestamp
        expect(events[1].id).toBe(1);
    });

    it('should reset to live mode', () => {
        useTimelineStore.getState().setCurrentTime(Date.now() - 5000);
        useTimelineStore.getState().togglePlayback();
        
        expect(useTimelineStore.getState().isHistoricalMode).toBe(true);
        
        useTimelineStore.getState().goLive();
        
        expect(useTimelineStore.getState().isHistoricalMode).toBe(false);
        expect(useTimelineStore.getState().isPlaying).toBe(false);
    });
});
