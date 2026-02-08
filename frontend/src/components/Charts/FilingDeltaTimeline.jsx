import React from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { TrendingUp, TrendingDown, Clock } from "lucide-react";
import { motion } from "framer-motion";

const FilingDeltaTimeline = ({ history }) => {
    if (!history || history.length === 0) return null;

    const maxScore = Math.max(...history.map(h => h.score));

    return (
        <Card className="bg-slate-950/40 border-slate-800 backdrop-blur-md">
            <CardHeader className="pb-4">
                <div className="flex items-center justify-between">
                    <div>
                        <CardTitle className="text-white flex items-center gap-2">
                            <Clock className="h-5 w-5 text-indigo-500" />
                            Flow Velocity Timeline
                        </CardTitle>
                        <CardDescription>Aggregate institutional position delta over the last 12 weeks.</CardDescription>
                    </div>
                </div>
            </CardHeader>
            <CardContent>
                <div className="h-48 flex items-end gap-1 px-2 pt-4">
                    {history.map((point, idx) => (
                        <div key={idx} className="flex-1 group relative flex flex-col items-center">
                            {/* Tooltip */}
                            <div className="absolute -top-8 left-1/2 -translate-x-1/2 bg-slate-800 text-white text-[10px] px-2 py-1 rounded opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none whitespace-nowrap z-10 border border-slate-700 font-mono">
                                {point.date}: {point.score}
                            </div>
                            
                            {/* Bar */}
                            <motion.div 
                                initial={{ height: 0 }}
                                animate={{ height: `${(point.score / maxScore) * 100}%` }}
                                className={`w-full rounded-t ${point.score > 80 ? 'bg-red-500/60 group-hover:bg-red-500' : 'bg-indigo-500/40 group-hover:bg-indigo-500'} transition-colors border-t border-x border-white/10`}
                            />
                            
                            {/* Date Label (Every 4 weeks) */}
                            {idx % 4 === 0 && (
                                <span className="text-[8px] text-slate-500 font-mono absolute -bottom-6 rotate-45 origin-left whitespace-nowrap">
                                    {point.date.split('-').slice(1).join('/')}
                                </span>
                            )}
                        </div>
                    ))}
                </div>
                {/* Legend */}
                <div className="mt-10 flex items-center justify-end gap-6 text-[10px] font-mono text-slate-500 uppercase tracking-widest border-t border-slate-900 pt-4">
                    <div className="flex items-center gap-2">
                        <div className="w-2 h-2 rounded-full bg-indigo-500" />
                        <span>Accumulation</span>
                    </div>
                    <div className="flex items-center gap-2">
                        <div className="w-2 h-2 rounded-full bg-red-500" />
                        <span>Distribution</span>
                    </div>
                </div>
            </CardContent>
        </Card>
    );
};

export default FilingDeltaTimeline;
