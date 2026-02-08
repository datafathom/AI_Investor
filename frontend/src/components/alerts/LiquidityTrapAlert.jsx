import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { AlertTriangle, Zap, ArrowRight } from 'lucide-react';
import { Badge } from "@/components/ui/badge";

const LiquidityTrapAlert = ({ traps }) => {
    if (!traps || traps.length === 0) return null;

    const getSeverityStyles = (severity) => {
        switch (severity) {
            case "CRITICAL": return "bg-red-500/20 border-red-500 text-red-500";
            case "SEVERE": return "bg-orange-500/20 border-orange-500 text-orange-500";
            default: return "bg-yellow-500/20 border-yellow-500 text-yellow-500";
        }
    };

    return (
        <AnimatePresence>
            <div className="space-y-3">
                {traps.map((trap, idx) => (
                    <motion.div
                        key={`${trap.ticker}-${idx}`}
                        initial={{ opacity: 0, x: 20 }}
                        animate={{ opacity: 1, x: 0 }}
                        exit={{ opacity: 0, x: -20 }}
                        className={`p-4 rounded-lg border-l-4 flex items-center justify-between backdrop-blur-md ${getSeverityStyles(trap.severity)} bg-opacity-10 border-opacity-50`}
                    >
                        <div className="flex items-center gap-4">
                            <div className={`p-2 rounded-full ${trap.severity === 'CRITICAL' ? 'bg-red-500' : 'bg-yellow-500'} bg-opacity-20 animate-pulse`}>
                                <AlertTriangle className="h-5 w-5" />
                            </div>
                            <div>
                                <h4 className="font-bold flex items-center gap-2">
                                    LIQUIDITY TRAP: {trap.ticker}
                                    <Badge variant="outline" className={`${getSeverityStyles(trap.severity)} text-[10px] h-4 px-1`}>
                                        {trap.severity}
                                    </Badge>
                                </h4>
                                <p className="text-sm opacity-80">
                                    Passive selling pressure detected. Spread expanded by <span className="font-mono font-bold">{trap.spread_expansion}x</span>
                                </p>
                            </div>
                        </div>
                        <div className="hidden md:flex items-center gap-2 text-xs font-mono opacity-60">
                            <span>{new Date(trap.timestamp).toLocaleTimeString()}</span>
                            <ArrowRight className="h-3 w-3" />
                        </div>
                    </motion.div>
                ))}
            </div>
        </AnimatePresence>
    );
};

export default LiquidityTrapAlert;
