import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { BarChart3, Users, AlertCircle } from "lucide-react";
import { motion } from "framer-motion";

const SectorCrowdingGauge = ({ sector }) => {
    if (!sector) return null;

    const { sector: name, crowding_score, status, avg_holder_overlap, top_crowded_tickers } = sector;

    const getStatusColor = (status) => {
        switch (status) {
            case "OVERCROWDED": return "text-red-400 border-red-900 bg-red-900/20";
            case "HIGH": return "text-yellow-400 border-yellow-900 bg-yellow-900/20";
            default: return "text-green-400 border-green-900 bg-green-900/20";
        }
    };

    const getGaugeColor = (score) => {
        if (score > 85) return "bg-red-500 shadow-[0_0_15px_rgba(239,68,68,0.5)]";
        if (score > 70) return "bg-orange-500 shadow-[0_0_10px_rgba(249,115,22,0.3)]";
        return "bg-indigo-500 shadow-[0_0_10px_rgba(99,102,241,0.2)]";
    };

    return (
        <Card className="bg-slate-950/40 border-slate-800 backdrop-blur-md overflow-hidden hover:border-slate-700 transition-all group">
            <div className={`h-1 w-full ${getGaugeColor(crowding_score)}`} />
            <CardHeader className="pb-2">
                <div className="flex justify-between items-start">
                    <div>
                        <CardTitle className="text-lg font-bold text-white group-hover:text-indigo-400 transition-colors uppercase tracking-tight">
                            {name}
                        </CardTitle>
                        <div className="flex items-center gap-1.5 mt-1">
                            <Badge variant="outline" className={`${getStatusColor(status)} text-[10px] uppercase font-mono`}>
                                {status}
                            </Badge>
                        </div>
                    </div>
                    <div className="text-right">
                        <span className="text-2xl font-black text-white font-mono">{crowding_score}</span>
                        <div className="text-[8px] text-slate-500 uppercase tracking-widest leading-none">Crowd Index</div>
                    </div>
                </div>
            </CardHeader>
            <CardContent className="space-y-4">
                <div className="space-y-1.5">
                    <div className="flex justify-between text-[10px] text-slate-500 uppercase font-mono tracking-widest">
                        <span>Holder Overlap</span>
                        <span className="text-slate-300">{(avg_holder_overlap * 100).toFixed(0)}%</span>
                    </div>
                    <div className="w-full bg-slate-900 h-1.5 rounded-full overflow-hidden">
                        <motion.div 
                            initial={{ width: 0 }}
                            animate={{ width: `${avg_holder_overlap * 100}%` }}
                            className={`h-full ${getGaugeColor(crowding_score)}`}
                        />
                    </div>
                </div>

                <div className="pt-2 border-t border-slate-900">
                    <div className="flex items-center gap-2 mb-2 text-[10px] text-slate-500 uppercase tracking-widest font-mono">
                        <AlertCircle className="h-3 w-3" />
                        <span>High Velocity Assets</span>
                    </div>
                    <div className="flex flex-wrap gap-2">
                        {top_crowded_tickers.map(ticker => (
                            <Badge key={ticker} variant="secondary" className="bg-slate-900 text-slate-300 border-slate-800 font-mono text-[10px]">
                                {ticker}
                            </Badge>
                        ))}
                    </div>
                </div>
            </CardContent>
        </Card>
    );
};

export default SectorCrowdingGauge;
