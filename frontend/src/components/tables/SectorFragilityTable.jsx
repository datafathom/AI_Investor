import React from 'react';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { Zap, LayoutGrid } from "lucide-react";

const SectorFragilityTable = ({ data, loading }) => {
    if (loading) return <div className="p-8 text-center text-slate-500 font-mono animate-pulse">Scanning Industrial Segments...</div>;
    if (!data || data.length === 0) return null;

    return (
        <div className="rounded-lg border border-slate-800 bg-slate-950/40 overflow-hidden">
            <Table>
                <TableHeader className="bg-slate-900/50">
                    <TableRow className="border-slate-800 hover:bg-transparent">
                        <TableHead className="text-slate-400 font-mono text-xs uppercase tracking-wider">Sector</TableHead>
                        <TableHead className="text-slate-400 font-mono text-xs uppercase tracking-wider text-right">Tickers</TableHead>
                        <TableHead className="text-slate-400 font-mono text-xs uppercase tracking-wider text-right">Avg Passive %</TableHead>
                        <TableHead className="text-slate-400 font-mono text-xs uppercase tracking-wider text-right">Fragility Index</TableHead>
                        <TableHead className="text-slate-400 font-mono text-xs uppercase tracking-wider text-right">Risk Pulse</TableHead>
                    </TableRow>
                </TableHeader>
                <TableBody>
                    {data.map((sector) => (
                        <TableRow key={sector.sector} className="border-slate-800 hover:bg-slate-800/20 transition-colors">
                            <TableCell className="font-semibold text-slate-200">
                                <div className="flex items-center gap-2">
                                    <LayoutGrid className="h-4 w-4 text-indigo-500/50" />
                                    {sector.sector}
                                </div>
                            </TableCell>
                            <TableCell className="text-right font-mono text-slate-400">{sector.ticker_count}</TableCell>
                            <TableCell className="text-right font-mono text-slate-300">{sector.avg_passive_pct}%</TableCell>
                            <TableCell className="text-right">
                                <span className={`font-mono font-bold ${sector.total_fragility > 60 ? 'text-red-400' : 'text-slate-200'}`}>
                                    {sector.total_fragility}
                                </span>
                            </TableCell>
                            <TableCell className="text-right">
                                {sector.high_risk_count > 0 ? (
                                    <Badge variant="destructive" className="bg-red-500/20 text-red-400 border-red-900/50 animate-pulse">
                                        <Zap className="h-3 w-3 mr-1 fill-current" /> {sector.high_risk_count} CRITICAL
                                    </Badge>
                                ) : (
                                    <Badge variant="outline" className="text-green-500 border-green-900/50 bg-green-950/20 text-[10px]">
                                        NOMINAL
                                    </Badge>
                                )}
                            </TableCell>
                        </TableRow>
                    ))}
                </TableBody>
            </Table>
        </div>
    );
};

export default SectorFragilityTable;
