import React from 'react';
import { motion } from 'framer-motion';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

const PassiveConcentrationHeatmap = ({ data }) => {
    if (!data || data.length === 0) return null;

    const getIntensity = (val) => {
        if (val > 70) return "bg-red-500/80 border-red-500";
        if (val > 55) return "bg-orange-500/60 border-orange-500";
        if (val > 40) return "bg-yellow-500/40 border-yellow-500";
        return "bg-indigo-500/20 border-indigo-500/50";
    };

    return (
        <Card className="bg-slate-950/40 border-slate-800 backdrop-blur-md">
            <CardHeader>
                <CardTitle className="text-slate-200">Structural Vulnerability Heatmap</CardTitle>
                <CardDescription>Sector-wide passive concentration vs. aggregate fragility index.</CardDescription>
            </CardHeader>
            <CardContent>
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                    {data.map((sector) => (
                        <motion.div
                            key={sector.sector}
                            whileHover={{ scale: 1.02 }}
                            className={`p-4 rounded-lg border-2 transition-all cursor-default ${getIntensity(sector.total_fragility)}`}
                        >
                            <div className="flex justify-between items-start mb-4">
                                <h4 className="font-bold text-white tracking-tight">{sector.sector.toUpperCase()}</h4>
                                <Badge variant="secondary" className="bg-black/40 text-[10px] text-white border-none">
                                    {sector.ticker_count} ASSETS
                                </Badge>
                            </div>
                            
                            <div className="space-y-3">
                                <div>
                                    <div className="flex justify-between text-[10px] uppercase tracking-widest text-white/60 mb-1">
                                        <span>Passive Concentration</span>
                                        <span className="font-mono">{sector.avg_passive_pct}%</span>
                                    </div>
                                    <div className="w-full bg-black/40 h-1 rounded-full overflow-hidden">
                                        <motion.div 
                                            initial={{ width: 0 }}
                                            animate={{ width: `${sector.avg_passive_pct}%` }}
                                            className="h-full bg-white"
                                        />
                                    </div>
                                </div>
                                
                                <div className="flex justify-between items-end">
                                    <div className="flex flex-col">
                                        <span className="text-[10px] uppercase tracking-widest text-white/60">Fragility Index</span>
                                        <span className="text-2xl font-black text-white font-mono leading-none mt-1">
                                            {sector.total_fragility}
                                        </span>
                                    </div>
                                    {sector.high_risk_count > 0 && (
                                        <div className="flex -space-x-1">
                                            {[...Array(Math.min(3, sector.high_risk_count))].map((_, i) => (
                                                <div key={i} className="w-2 h-2 rounded-full bg-red-400 shadow-[0_0_8px_rgba(248,113,113,0.8)]" />
                                            ))}
                                            {sector.high_risk_count > 3 && (
                                                <span className="text-[8px] text-white font-bold ml-2">+{sector.high_risk_count - 3}</span>
                                            )}
                                        </div>
                                    )}
                                </div>
                            </div>
                        </motion.div>
                    ))}
                </div>
            </CardContent>
        </Card>
    );
};

export default PassiveConcentrationHeatmap;
