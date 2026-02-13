import React, { useState, useEffect, useCallback } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Shield, AlertTriangle, CheckCircle, RefreshCw, Activity, Database } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import apiClient from '@/services/apiClient';

const DataQualityWidget = () => {
    const [summary, setSummary] = useState(null);
    const [issues, setIssues] = useState([]);
    const [loading, setLoading] = useState(true);

    const fetchData = useCallback(async (silent = false) => {
        if (!silent) setLoading(true);
        try {
            const [summaryRes, issuesRes] = await Promise.all([
                apiClient.get('/ingestion/quality/summary'),
                apiClient.get('/ingestion/quality/issues')
            ]);
            setSummary(summaryRes.data);
            setIssues(issuesRes.data || []);
        } catch (error) {
            console.error("Failed to fetch quality data", error);
        } finally {
            if (!silent) setLoading(false);
        }
    }, []);

    useEffect(() => {
        fetchData();
        const interval = setInterval(() => fetchData(true), 30000);
        return () => clearInterval(interval);
    }, [fetchData]);

    const resolveIssue = async (id) => {
        try {
            await apiClient.post(`/ingestion/quality/issues/${id}/resolve`);
            fetchData(true);
        } catch (error) {
            console.error("Failed to resolve issue", error);
        }
    };

    const getScoreColor = (score) => {
        if (score >= 90) return "text-emerald-500";
        if (score >= 70) return "text-amber-500";
        return "text-red-500";
    };

    return (
        <Card className="bg-slate-950/60 border-slate-800 backdrop-blur-xl h-full flex flex-col shadow-2xl">
            <CardHeader className="p-4 border-b border-slate-900 bg-slate-900/20">
                <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                        <Shield className="h-4 w-4 text-emerald-500" />
                        <CardTitle className="text-xs font-black uppercase tracking-[0.2em] text-white">Data_Quality_Sentinel</CardTitle>
                    </div>
                    {loading && <RefreshCw className="h-3 w-3 animate-spin text-slate-600" />}
                </div>
            </CardHeader>
            <CardContent className="p-4 flex-1 flex flex-col gap-6">
                {summary ? (
                    <div className="space-y-6">
                        {/* Score Section */}
                        <div className="text-center relative py-4">
                            <div className="text-[10px] uppercase font-mono text-slate-500 tracking-[0.3em] mb-2">Overall_Integrity</div>
                            <div className={`text-5xl font-black italic tracking-tighter ${getScoreColor(summary.score)}`}>
                                {summary.score}
                            </div>
                            <div className="flex justify-center gap-4 mt-2">
                                <div className="text-[10px] font-mono text-slate-400">
                                    <span className="text-emerald-500">{summary.accuracy_pct}%</span> ACCURACY
                                </div>
                                <div className="text-[10px] font-mono text-slate-400">
                                    <span className="text-blue-500">{summary.completeness_pct}%</span> COMPLETENESS
                                </div>
                            </div>
                        </div>

                        {/* Recent Issues List */}
                        <div className="flex-1 overflow-y-auto max-h-[200px] space-y-2 pr-1 custom-scrollbar">
                            <div className="text-[10px] font-black uppercase tracking-[0.2em] text-slate-500 sticky top-0 bg-slate-950/90 pb-2 backdrop-blur">
                                Detected_Anomalies ({issues.length})
                            </div>
                            <AnimatePresence>
                                {issues.length === 0 ? (
                                    <div className="text-center py-8 border border-dashed border-slate-800 rounded-lg">
                                        <CheckCircle className="h-6 w-6 text-emerald-500/50 mx-auto mb-2" />
                                        <p className="text-[10px] uppercase text-slate-600">No active integrity violations</p>
                                    </div>
                                ) : (
                                    issues.map((issue) => (
                                        <motion.div
                                            key={issue.id}
                                            initial={{ opacity: 0, x: -10 }}
                                            animate={{ opacity: 1, x: 0 }}
                                            exit={{ opacity: 0, height: 0 }}
                                            className="p-3 rounded border border-slate-800 bg-slate-900/30 group hover:border-slate-700 transition-colors"
                                        >
                                            <div className="flex justify-between items-start gap-2">
                                                <div className="space-y-1">
                                                    <div className="flex items-center gap-2">
                                                        <Badge variant="outline" className={`h-4 text-[8px] border-none bg-slate-900 ${
                                                            issue.severity === 'critical' ? 'text-red-400' : 'text-amber-400'
                                                        }`}>
                                                            {issue.type.toUpperCase()}
                                                        </Badge>
                                                        <span className="text-[10px] font-mono text-slate-500">{new Date(issue.detected_at).toLocaleTimeString()}</span>
                                                    </div>
                                                    <p className="text-xs text-slate-300 line-clamp-2">{issue.description}</p>
                                                    <div className="text-[10px] font-mono text-slate-600">SRC: {issue.source}</div>
                                                </div>
                                                <button 
                                                    onClick={() => resolveIssue(issue.id)}
                                                    className="p-1 rounded opacity-0 group-hover:opacity-100 hover:bg-emerald-500/20 text-emerald-500 transition-all"
                                                    title="Mark Resolved"
                                                >
                                                    <CheckCircle className="h-4 w-4" />
                                                </button>
                                            </div>
                                        </motion.div>
                                    ))
                                )}
                            </AnimatePresence>
                        </div>
                    </div>
                ) : (
                    <div className="flex items-center justify-center h-full">
                        <RefreshCw className="h-8 w-8 text-slate-800 animate-spin" />
                    </div>
                )}
            </CardContent>
            <div className="p-2 border-t border-slate-900 bg-slate-900/30 flex justify-between items-center text-[8px] font-mono text-slate-500">
                <div className="flex items-center gap-1">
                    <Database className="h-3 w-3" />
                    <span>LATEST_SYNC: {summary?.freshness_hours || 0}h AGO</span>
                </div>
                <div className="flex items-center gap-1">
                    <Activity className="h-3 w-3 text-emerald-500" />
                    <span>MONITOR_ACTIVE</span>
                </div>
            </div>
        </Card>
    );
};

export default DataQualityWidget;
