import React from 'react';
import { ChevronLeft, ChevronRight, Zap, Droplet, Heart, Cpu, Landmark } from 'lucide-react';

const SectorCarousel = () => {
    const sectors = [
        { name: 'Tech', icon: <Cpu />, color: 'text-cyan-400', val: '+2.4%' },
        { name: 'Finance', icon: <Landmark />, color: 'text-green-400', val: '+1.1%' },
        { name: 'Energy', icon: <Zap />, color: 'text-yellow-400', val: '-0.5%' },
        { name: 'Health', icon: <Heart />, color: 'text-red-400', val: '-1.2%' }
    ];

    return (
        <div className="flex items-center gap-2 h-full">
            <button className="p-1 hover:bg-slate-800 rounded text-slate-500"><ChevronLeft size={16} /></button>

            <div className="flex-1 flex gap-4 overflow-hidden px-2">
                {sectors.map((s, i) => (
                    <div key={i} className="flex-1 min-w-[80px] bg-slate-800/50 border border-slate-700/50 rounded-lg p-2 flex flex-col items-center justify-center gap-1 cursor-pointer hover:bg-slate-700/80 transition-all hover:scale-105 group interact-hover border-b-2 hover:border-b-cyan-500 shadow-lg">
                        <div className={`transition-all duration-300 group-hover:scale-110 group-hover:animate-neon-pulse ${s.color}`}>
                            {React.cloneElement(s.icon, { size: 18 })}
                        </div>
                        <span className="text-[10px] font-bold text-slate-400 uppercase tracking-widest group-hover:text-white transition-colors">{s.name}</span>
                        <span className={`text-xs font-mono font-bold ${s.val.startsWith('+') ? 'text-green-400' : 'text-red-400'} text-glow-cyan`}>
                            {s.val}
                        </span>
                    </div>
                ))}
            </div>

            <button className="p-1 hover:bg-slate-800 rounded text-slate-500"><ChevronRight size={16} /></button>
        </div>
    );
};

export default SectorCarousel;
