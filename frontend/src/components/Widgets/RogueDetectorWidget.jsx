import React, { useState, useEffect } from 'react';
import { agentService } from '../../services/agentService';
import { ShieldAlert, Zap, XOctagon } from 'lucide-react';
import { toast } from 'sonner';

export const RogueDetectorWidget = () => {
    const [history, setHistory] = useState([]);
    const [tpmData, setTpmData] = useState([]); // Mock TPM data for gauge

    useEffect(() => {
        loadHistory();
        // Mock TPM stream
        const interval = setInterval(() => {
            setTpmData(prev => {
                const newVal = Math.floor(Math.random() * 120); // Random TPM
                return [...prev.slice(-19), newVal];
            });
        }, 1000);
        return () => clearInterval(interval);
    }, []);

    const loadHistory = async () => {
        try {
            const res = await agentService.getKillHistory();
            setHistory(res);
        } catch (e) {
            console.error("Failed to load kill history");
        }
    };

    const handleManualKill = async () => {
        const agentId = prompt("ENTER AGENT ID TO TERMINATE:");
        if (!agentId) return;
        
        try {
            await agentService.killAgent(agentId, "Admin Command");
            toast.success(`Agent ${agentId} terminated.`);
            loadHistory();
        } catch (e) {
            toast.error("Termination failed");
        }
    };

    const currentTpm = tpmData[tpmData.length - 1] || 0;
    const isHighTpm = currentTpm > 100;

    return (
        <div className={`border rounded-xl p-4 flex flex-col h-full bg-slate-900 ${isHighTpm ? 'border-red-500/50 shadow-[0_0_15px_rgba(239,68,68,0.2)]' : 'border-slate-800'}`}>
            <div className="flex justify-between items-center mb-4">
                <h3 className="font-bold text-white flex items-center gap-2">
                    <ShieldAlert className={isHighTpm ? "text-red-500 animate-pulse" : "text-cyan-500"} /> 
                    Rogue Detector
                </h3>
                <button 
                    onClick={handleManualKill}
                    className="p-1 px-2 text-[10px] bg-red-500/10 hover:bg-red-500/20 text-red-500 border border-red-500/20 rounded transition-colors font-bold flex items-center gap-1"
                >
                    <XOctagon size={12} /> KILL
                </button>
            </div>

            {/* Mock TPM Gauge */}
            <div className="relative h-24 mb-4 bg-slate-950 rounded border border-slate-800 flex items-end justify-between p-1 overflow-hidden">
                {tpmData.map((val, i) => (
                    <div 
                        key={i} 
                        className={`w-1 rounded-t ${val > 100 ? 'bg-red-500' : 'bg-cyan-500'}`}
                        style={{ height: `${Math.min(val, 100)}%` }}
                    />
                ))}
                <div className="absolute top-2 right-2 text-right">
                    <div className="text-[10px] text-slate-500">AVG TPM</div>
                    <div className={`text-xl font-bold font-mono ${isHighTpm ? 'text-red-500' : 'text-white'}`}>
                        {currentTpm}
                    </div>
                </div>
            </div>

            <div className="flex-1 overflow-y-auto min-h-[100px]">
                <h4 className="text-[10px] font-bold text-slate-500 uppercase tracking-wider mb-2">Kill History</h4>
                <div className="space-y-2">
                    {history.map((event, i) => (
                        <div key={i} className="bg-slate-950 p-2 rounded border border-slate-800 text-xs">
                            <div className="flex justify-between items-start">
                                <span className="font-bold text-red-400">{event.agent_id}</span>
                                <span className="text-[10px] text-slate-600">
                                    {new Date(event.timestamp).toLocaleTimeString()}
                                </span>
                            </div>
                            <div className="text-slate-400 mt-1 flex items-center gap-1">
                                <Zap size={10} className="text-yellow-500" />
                                {event.reason}
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
};
