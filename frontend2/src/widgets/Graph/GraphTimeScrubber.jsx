import React from 'react';
import { Clock, History, Calendar, Zap } from 'lucide-react';
import useTimelineStore from '../../stores/timelineStore';

/**
 * Sprint 6: Graph Time Scrubber
 * Wired to global timelineStore to enable historical graph reconstruction.
 * When scrubbed back, MasterOrchestrator fetches historical snapshot data.
 */
const GraphTimeScrubber = ({ onTimeChange }) => {
    const { 
        currentTime, 
        setCurrentTime, 
        isHistoricalMode,
        goLive 
    } = useTimelineStore();

    // Calculate slider value from currentTime (last 24 hours mapped to 0-100)
    const now = Date.now();
    const dayAgo = now - 24 * 60 * 60 * 1000;
    const sliderValue = Math.max(0, Math.min(100, ((currentTime - dayAgo) / (now - dayAgo)) * 100));

    const handleChange = (e) => {
        const val = parseInt(e.target.value);
        // Convert slider value back to timestamp
        const newTime = dayAgo + ((val / 100) * (now - dayAgo));
        setCurrentTime(newTime);
        
        // Notify parent if callback provided
        if (onTimeChange) {
            const formattedTime = new Date(newTime).toLocaleString();
            onTimeChange(formattedTime);
        }
    };

    const formatTimeLabel = (timestamp) => {
        const date = new Date(timestamp);
        return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    };

    // Time markers for the last 24 hours (6 intervals)
    const markers = [0, 20, 40, 60, 80, 100].map(pct => {
        const timestamp = dayAgo + ((pct / 100) * (now - dayAgo));
        return formatTimeLabel(timestamp);
    });

    return (
        <div className="w-full h-full flex flex-col p-6 items-center justify-center space-y-6">
            <div className="flex items-center gap-4">
                <div className={`p-3 rounded-full ${isHistoricalMode ? 'bg-amber-500/10 border-amber-500/20' : 'bg-blue-500/10 border-blue-500/20'} border`}>
                    <History size={24} className={isHistoricalMode ? 'text-amber-400' : 'text-blue-400'} />
                </div>
                <div>
                    <h4 className="text-white text-sm font-bold">Temporal Graph Engine</h4>
                    <p className="text-zinc-500 text-[10px] uppercase tracking-widest">
                        {isHistoricalMode ? 'HISTORICAL MODE' : 'Live State Reconstruction'}
                    </p>
                </div>
            </div>

            <div className="w-full space-y-4">
                <div className="flex justify-between px-2">
                    {markers.map((label, i) => (
                        <div key={i} className="flex flex-col items-center">
                            <div className={`w-1 h-1 rounded-full mb-2 ${(i * 20) <= sliderValue ? 'bg-blue-400' : 'bg-zinc-800'}`} />
                            <span className={`text-[8px] font-mono tracking-tighter ${(i * 20) <= sliderValue ? 'text-zinc-300' : 'text-zinc-600'}`}>
                                {label}
                            </span>
                        </div>
                    ))}
                </div>
                
                <input 
                    type="range" 
                    min="0" 
                    max="100" 
                    value={sliderValue} 
                    onChange={handleChange}
                    className="w-full h-1 bg-zinc-800 rounded-lg appearance-none cursor-pointer accent-blue-500"
                />
            </div>

            <div className={`flex items-center gap-2 px-4 py-2 ${isHistoricalMode ? 'bg-amber-500/10 border-amber-500/20' : 'bg-blue-500/5 border-blue-500/10'} border rounded-full`}>
                <Calendar size={12} className={isHistoricalMode ? 'text-amber-400' : 'text-blue-400'} />
                <span className={`${isHistoricalMode ? 'text-amber-300' : 'text-blue-300'} text-[10px] font-mono uppercase tracking-widest`}>
                    {isHistoricalMode ? `Viewing: ${new Date(currentTime).toLocaleString()}` : 'LIVE'}
                </span>
                {isHistoricalMode && (
                    <button 
                        onClick={goLive}
                        className="ml-2 flex items-center gap-1 px-2 py-0.5 bg-emerald-500/20 border border-emerald-500/30 rounded-full text-emerald-400 text-[9px] font-bold hover:bg-emerald-500/30 transition-colors"
                    >
                        <Zap size={10} /> GO LIVE
                    </button>
                )}
            </div>
        </div>
    );
};

export default GraphTimeScrubber;

