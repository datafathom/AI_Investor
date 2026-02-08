import React from 'react';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { TrendingDown, UserMinus, ShieldAlert } from "lucide-react";

const WhaleSellingTable = ({ filings, loading }) => {
    if (loading) return <div className="p-12 text-center text-slate-500 font-mono animate-pulse">Filtering Institutional Distribution Events...</div>;
    
    const sellFilings = filings.filter(f => f.action === 'SELL').sort((a, b) => b.position_value_millions - a.position_value_millions);

    if (sellFilings.length === 0) {
        return (
            <div className="py-12 text-center border border-dashed border-slate-800 rounded-xl bg-slate-950/20">
                <p className="text-slate-500 font-mono uppercase tracking-widest text-xs">No significant distribution events detected in scan range.</p>
            </div>
        );
    }

    return (
        <div className="rounded-xl border border-red-900/30 bg-slate-950/40 overflow-hidden shadow-[0_0_20px_rgba(239,68,68,0.05)]">
            <div className="bg-red-900/10 border-b border-red-900/20 p-4 flex items-center justify-between">
                <div className="flex items-center gap-2">
                    <ShieldAlert className="h-4 w-4 text-red-500" />
                    <span className="text-xs font-black text-red-100 uppercase tracking-[0.2em]">Institutional Exit Scan</span>
                </div>
                <Badge variant="outline" className="text-red-400 border-red-900/50 bg-red-900/20 text-[10px]">
                    {sellFilings.length} ALERTS
                </Badge>
            </div>
            <Table>
                <TableHeader className="bg-slate-900/50">
                    <TableRow className="border-slate-800 hover:bg-transparent">
                        <TableHead className="text-slate-400 font-mono text-[10px] uppercase tracking-widest">Institutional Holder</TableHead>
                        <TableHead className="text-slate-400 font-mono text-[10px] uppercase tracking-widest text-center">Asset</TableHead>
                        <TableHead className="text-slate-400 font-mono text-[10px] uppercase tracking-widest text-right">Shares Exited</TableHead>
                        <TableHead className="text-slate-400 font-mono text-[10px] uppercase tracking-widest text-right">Liquidation Val</TableHead>
                        <TableHead className="text-slate-400 font-mono text-[10px] uppercase tracking-widest text-right">Filing Date</TableHead>
                    </TableRow>
                </TableHeader>
                <TableBody>
                    {sellFilings.map((f, idx) => (
                        <TableRow key={idx} className="border-slate-800 hover:bg-red-950/10 transition-colors group">
                            <TableCell className="font-semibold text-slate-200">
                                <div className="flex items-center gap-2">
                                    <div className="w-1 h-4 bg-red-500/50 rounded-full" />
                                    {f.holder}
                                </div>
                            </TableCell>
                            <TableCell className="text-center font-black text-white font-mono group-hover:text-red-400">
                                <Badge variant="secondary" className="bg-slate-900 text-white border-slate-700">
                                    {f.ticker}
                                </Badge>
                            </TableCell>
                            <TableCell className="text-right font-mono text-red-400/80">
                                {f.shares_changed.toLocaleString()}
                            </TableCell>
                            <TableCell className="text-right font-mono text-white font-bold">
                                ${f.position_value_millions.toLocaleString()}M
                            </TableCell>
                            <TableCell className="text-right font-mono text-slate-500 text-xs">
                                {f.filing_date}
                            </TableCell>
                        </TableRow>
                    ))}
                </TableBody>
            </Table>
        </div>
    );
};

export default WhaleSellingTable;
