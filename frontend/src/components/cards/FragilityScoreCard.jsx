import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { TrendingDown, Info } from "lucide-react";
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip";

const FragilityScoreCard = ({ data }) => {
    if (!data) return null;

    const { ticker, fragility_score, risk_level, passive_pct, float_turnover, spread_volatility } = data;

    const getRiskStyles = (level) => {
        switch (level) {
            case "HIGH": return "text-red-400 border-red-900 bg-red-900/20";
            case "MEDIUM": return "text-yellow-400 border-yellow-900 bg-yellow-900/20";
            default: return "text-green-400 border-green-900 bg-green-900/20";
        }
    };

    return (
        <Card className="bg-slate-950/40 border-slate-800 backdrop-blur-md hover:border-slate-700 transition-all">
            <CardHeader className="flex flex-row items-center justify-between pb-2">
                <div>
                    <CardTitle className="text-xl font-mono text-white flex items-center gap-2">
                        {ticker}
                        <Badge variant="outline" className={getRiskStyles(risk_level)}>
                            {risk_level}
                        </Badge>
                    </CardTitle>
                </div>
                <div className="flex flex-col items-end">
                    <span className="text-2xl font-bold text-white">{fragility_score}</span>
                    <span className="text-[10px] text-slate-500 uppercase tracking-widest">Fragility Score</span>
                </div>
            </CardHeader>
            <CardContent>
                <div className="space-y-4">
                    <div className="grid grid-cols-2 gap-4">
                        <div className="space-y-1">
                            <div className="flex items-center gap-1.5 text-xs text-slate-400">
                                <span>Passive Ownership</span>
                                <TooltipProvider>
                                    <Tooltip>
                                        <TooltipTrigger><Info className="h-3 w-3" /></TooltipTrigger>
                                        <TooltipContent>Percentage of float held by passive ETFs and indexed funds.</TooltipContent>
                                    </Tooltip>
                                </TooltipProvider>
                            </div>
                            <p className="text-lg font-mono text-slate-200">{passive_pct}%</p>
                        </div>
                        <div className="space-y-1 text-right">
                            <div className="flex items-center justify-end gap-1.5 text-xs text-slate-400">
                                <span>Float Turnover</span>
                                <TooltipProvider>
                                    <Tooltip>
                                        <TooltipTrigger><Info className="h-3 w-3" /></TooltipTrigger>
                                        <TooltipContent>Rate at which the stock's float is traded.</TooltipContent>
                                    </Tooltip>
                                </TooltipProvider>
                            </div>
                            <p className="text-lg font-mono text-slate-200">{float_turnover}x</p>
                        </div>
                    </div>
                    
                    <div className="pt-2">
                        <div className="flex justify-between items-center text-xs mb-1.5">
                            <span className="text-slate-500">Spread Volatility</span>
                            <span className="text-slate-300 font-mono">{(spread_volatility * 100).toFixed(2)}%</span>
                        </div>
                        <div className="w-full bg-slate-800 rounded-full h-1.5 overflow-hidden">
                            <div 
                                className={`h-full ${risk_level === 'HIGH' ? 'bg-red-500' : 'bg-indigo-500'}`}
                                style={{ width: `${Math.min(100, spread_volatility * 500)}%` }}
                            />
                        </div>
                    </div>
                </div>
            </CardContent>
        </Card>
    );
};

export default FragilityScoreCard;
