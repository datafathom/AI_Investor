import React, { useEffect, useState } from 'react';
import { Zap } from 'lucide-react';

const ReflexivityEcho = ({ activeShock }) => {
    const [ripples, setRipples] = useState([]);

    useEffect(() => {
        if (activeShock) {
            const newRipple = {
                id: Date.now(),
                asset: activeShock.asset_id,
                time: new Date().toLocaleTimeString(),
                velocity: activeShock.contagion_velocity
            };
            setRipples(prev => [newRipple, ...prev].slice(0, 5));
        }
    }, [activeShock]);

    return (
        <div className="w-full h-full flex flex-col p-4 relative overflow-hidden">
            <div className="space-y-3">
                {ripples.map((ripple) => (
                    <div key={ripple.id} className="p-3 bg-zinc-900/80 border border-yellow-500/20 rounded-lg animate-in fade-in slide-in-from-right-4 duration-500">
                        <div className="flex justify-between items-start mb-2">
                            <div className="flex items-center gap-2">
                                <Zap size={14} className="text-yellow-400 animate-pulse" />
                                <span className="text-yellow-400 text-[10px] font-black uppercase tracking-widest">Shock Ripple</span>
                            </div>
                            <span className="text-zinc-600 text-[9px] font-mono">{ripple.time}</span>
                        </div>
                        <div className="text-zinc-100 text-xs font-bold mb-1">{ripple.asset}</div>
                        <div className="flex items-center gap-2">
                            <span className="text-zinc-500 text-[10px]">Velocity:</span>
                            <div className="flex-1 h-1 bg-zinc-800 rounded-full overflow-hidden">
                                <div 
                                    className="h-full bg-yellow-400"
                                    style={{ width: `${ripple.velocity * 100}%` }}
                                />
                            </div>
                            <span className="text-white text-[10px]">{Math.round(ripple.velocity * 100)}%</span>
                        </div>
                    </div>
                ))}
                {ripples.length === 0 && (
                    <div className="h-full flex items-center justify-center">
                        <p className="text-zinc-600 text-[10px] uppercase tracking-tighter italic">Waiting for Graph Shock Event...</p>
                    </div>
                )}
            </div>
        </div>
    );
};

export default ReflexivityEcho;
