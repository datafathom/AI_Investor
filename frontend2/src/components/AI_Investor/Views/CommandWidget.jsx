import React from 'react';
import BacktestDemo from '../Controls/BacktestDemo';
import { Shield } from 'lucide-react';
import GlassCard from '../Controls/GlassCard';
import Button from '../Controls/Button';

const CommandWidget = () => {
    return (
        <div className="grid grid-cols-1 xl:grid-cols-4 gap-4 h-full">
            <div className="xl:col-span-3 h-full overflow-auto">
                <BacktestDemo standalone={false} />
            </div>

            <div className="space-y-4 overflow-auto">
                <GlassCard title="Agent Override">
                    <div className="space-y-2">
                        <div className="flex items-center justify-between p-2 bg-white/5 rounded border-l-2 border-green-500">
                            <span className="text-xs font-bold">SearcherAgent</span>
                            <Button variant="ghost" className="text-[10px] py-1 px-2 h-auto border-none">ACTIVE</Button>
                        </div>
                        <div className="flex items-center justify-between p-2 bg-white/5 rounded border-l-2 border-purple-500">
                            <span className="text-xs font-bold">ProtectorAgent</span>
                            <Button variant="ghost" className="text-[10px] py-1 px-2 h-auto border-none">NOMINAL</Button>
                        </div>
                        <div className="flex items-center justify-between p-2 bg-white/5 rounded border-l-2 border-red-500 opacity-50">
                            <span className="text-xs font-bold">StackerAgent</span>
                            <Button variant="ghost" className="text-[10px] py-1 px-2 h-auto border-none">IDLE</Button>
                        </div>
                    </div>
                </GlassCard>

                <GlassCard title="Security Protocol" subTitle="Circuit Breaker Status">
                    <div className="flex items-center gap-2 text-dim mb-2">
                        <Shield className="text-cyan-400" size={16} />
                        <span className="text-[10px] uppercase">Drawdown Limit: 3.0%</span>
                    </div>
                    <Button variant="danger" className="w-full text-xs">FORCE KILL SWITCH</Button>
                </GlassCard>

                <GlassCard title="System Logs">
                    <div className="bg-black/40 rounded p-2 h-32 overflow-y-auto font-mono text-[10px] text-green-500/80 space-y-1">
                        <div className="flex gap-2"><span>[11:29:42]</span> <span className="text-cyan-400">INFO:</span> Agent cluster sync complete.</div>
                        <div className="flex gap-2"><span>[11:29:44]</span> <span className="text-cyan-400">INFO:</span> Scanned r/stocks for $TSLA velocity.</div>
                        <div className="flex gap-2"><span>[11:30:01]</span> <span className="text-yellow-400">WARN:</span> High volatility detected in $BTC.</div>
                        <div className="flex gap-2 text-red-500"><span>[11:30:15]</span> <span className="font-bold">ALERT:</span> ProtectorAgent adjusting VaR limit.</div>
                    </div>
                </GlassCard>
            </div>
        </div>
    );
};

export default CommandWidget;
