import React, { useState } from 'react';
import { Search, Info, TrendingUp, TrendingDown, Clock, ChevronDown, ChevronUp, Bell, Zap, Cpu as CpuIcon } from 'lucide-react';
import GlassCard from '../Controls/GlassCard';
import Badge from '../Controls/Badge';
import Button from '../Controls/Button';
import OptionsFlowTable from '../Analytics/OptionsFlowTable';

const CollapsibleSection = ({ title, children, icon: Icon, defaultOpen = true }) => {
    const [isOpen, setIsOpen] = useState(defaultOpen);
    return (
        <div className="border border-[#222] rounded bg-[#0a0a0a] overflow-hidden mb-2">
            <button
                onClick={() => setIsOpen(!isOpen)}
                className="w-full flex items-center justify-between p-2 hover:bg-[#111] transition-colors"
            >
                <div className="flex items-center gap-2">
                    {Icon && <Icon size={14} className="text-cyan-400" />}
                    <span className="text-[10px] font-bold text-slate-300 uppercase tracking-widest">{title}</span>
                </div>
                {isOpen ? <ChevronUp size={14} className="text-slate-500" /> : <ChevronDown size={14} className="text-slate-500" />}
            </button>
            {isOpen && <div className="p-3 border-t border-[#222]">{children}</div>}
        </div>
    );
};

const ResearchWidget = () => {
    const [mockAlerts] = useState([
        { symbol: 'TSLA', type: 'call', strike: '220', expiration: '2026-01-23', volume: '12400', open_interest: '5000', alert_type: 'WHALE_FLOW' },
        { symbol: 'NVDA', type: 'put', strike: '540', expiration: '2026-02-20', volume: '8200', open_interest: '3100', alert_type: 'DARK_POOL' },
    ]);

    return (
        <div className="flex flex-col h-full bg-[#050505] text-white">
            {/* Search Header */}
            <div className="p-3 bg-[#111] border-b border-[#222]">
                <div className="relative">
                    <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500" size={14} />
                    <input
                        type="text"
                        placeholder="SEARCH MARKET INTELLIGENCE..."
                        className="w-full bg-black/40 border border-[#222] rounded py-1.5 pl-9 pr-4 text-[10px] text-white focus:border-cyan-500 outline-none font-mono uppercase tracking-widest"
                    />
                </div>
            </div>

            <div className="flex-1 overflow-y-auto custom-scrollbar p-3">
                <CollapsibleSection title="AI Alpha Alerts" icon={Bell}>
                    <div className="space-y-2">
                        {mockAlerts.map((alert, idx) => (
                            <div key={idx} className="flex flex-col bg-[#0f0f0f] border border-[#222] p-2 rounded hover:border-cyan-500/50 transition-colors">
                                <div className="flex justify-between items-center mb-1">
                                    <span className="font-mono font-bold text-cyan-400 text-xs">{alert.symbol} {alert.type.toUpperCase()}</span>
                                    <span className="text-[8px] bg-amber-500/20 text-amber-500 px-1 rounded font-bold">{alert.alert_type}</span>
                                </div>
                                <div className="text-[10px] text-slate-400 font-mono">
                                    STRIKE: {alert.strike} | EXP: {alert.expiration} | VOL: {alert.volume}
                                </div>
                            </div>
                        ))}
                    </div>
                </CollapsibleSection>

                <CollapsibleSection title="Asset Intelligence" icon={CpuIcon}>
                    <div className="grid grid-cols-2 gap-2">
                        <div className="bg-[#0f0f0f] border border-[#222] p-2 rounded">
                            <span className="block text-[8px] text-slate-500 uppercase mb-1">Correlation Index</span>
                            <span className="font-mono text-white text-xs">0.84</span>
                        </div>
                        <div className="bg-[#0f0f0f] border border-[#222] p-2 rounded">
                            <span className="block text-[8px] text-slate-500 uppercase mb-1">Momentum Score</span>
                            <span className="font-mono text-emerald-400 text-xs">VERY HIGH</span>
                        </div>
                    </div>
                </CollapsibleSection>

                <div className="mt-4">
                    <span className="text-[9px] text-slate-500 font-bold uppercase tracking-widest mb-2 block">Live Options Flow</span>
                    <OptionsFlowTable alerts={mockAlerts} />
                </div>
            </div>
        </div>
    );
};

export default ResearchWidget;
