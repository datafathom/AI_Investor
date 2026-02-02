import React, { useState, useEffect } from 'react';
import apiClient from '../../services/apiClient';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Loader2, RefreshCcw, DollarSign, ArrowRight } from "lucide-react";
import { useToast } from "@/components/ui/use-toast";

const TaxBitWidget = () => {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(false);
    const { toast } = useToast();

    const fetchAnalysis = async () => {
        setLoading(true);
        try {
        try {
            const response = await apiClient.get('/tax/harvesting/opportunities', { params: { mock: true } });
            const jsonData = response.data;
            setData(jsonData);
        } catch (error) {
            console.error("Error fetching TaxBit data:", error);
            toast({
                title: "Error",
                description: "Failed to load tax analysis.",
                variant: "destructive"
            });
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchAnalysis();
    }, []);

    const formatCurrency = (val) => {
        return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(val);
    };

    return (
        <Card className="w-full h-full bg-slate-950 border-slate-800 text-slate-100">
            <CardHeader className="pb-2">
                <div className="flex justify-between items-center">
                    <div className="flex items-center gap-2">
                        <div className="bg-blue-600 p-1 rounded">
                            <DollarSign className="w-4 h-4 text-white" />
                        </div>
                        <div>
                            <CardTitle>TaxBit Optimizer</CardTitle>
                            <CardDescription className="text-xs text-slate-400">Loss Harvesting & Optimization</CardDescription>
                        </div>
                    </div>
                    <Button variant="ghost" size="icon" onClick={fetchAnalysis} disabled={loading}>
                        {loading ? <Loader2 className="h-4 w-4 animate-spin" /> : <RefreshCcw className="h-4 w-4" />}
                    </Button>
                </div>
            </CardHeader>
            <CardContent>
                {data ? (
                    <div className="space-y-4">
                        <div className="grid grid-cols-2 gap-3">
                            <div className="bg-slate-900 p-3 rounded-lg border border-slate-800">
                                <div className="text-xs text-slate-400 mb-1">Est. Tax Savings</div>
                                <div className="text-xl font-bold text-green-400">
                                    {formatCurrency(data.summary?.estimated_tax_savings || 0)}
                                </div>
                            </div>
                            <div className="bg-slate-900 p-3 rounded-lg border border-slate-800">
                                <div className="text-xs text-slate-400 mb-1">Available Losses</div>
                                <div className="text-lg font-mono">
                                    {formatCurrency((data.summary?.short_term_losses_available || 0) + (data.summary?.long_term_losses_available || 0))}
                                </div>
                            </div>
                        </div>

                        <div className="space-y-2">
                            <div className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Opportunities</div>
                            {data.opportunities?.length > 0 ? (
                                data.opportunities.map((opp, i) => (
                                    <div key={i} className="bg-slate-900/50 p-3 rounded border border-slate-800 hover:border-slate-700 transition-colors">
                                        <div className="flex justify-between items-start mb-2">
                                            <div className="flex items-center gap-2">
                                                <Badge variant="outline" className="font-mono">{opp.asset}</Badge>
                                                <span className="text-sm font-medium">{opp.strategy}</span>
                                            </div>
                                            <Badge className="bg-green-900 text-green-300 hover:bg-green-800 border-0">
                                                + {formatCurrency(opp.unrealized_loss * 0.3)} Tax Credit
                                            </Badge>
                                        </div>
                                        <div className="flex justify-between items-center text-sm text-slate-400">
                                            <span>Loss: {formatCurrency(opp.unrealized_loss)}</span>
                                            <div className="flex items-center gap-1 text-blue-400 hover:text-blue-300 cursor-pointer text-xs">
                                                Execute <ArrowRight className="w-3 h-3" />
                                            </div>
                                        </div>
                                    </div>
                                ))
                            ) : (
                                <div className="text-center py-4 text-slate-500 text-sm">No opportunities found.</div>
                            )}
                        </div>
                    </div>
                ) : (
                    <div className="flex items-center justify-center h-40">
                         {loading ? <span className="text-slate-500 text-sm">Analyzing portfolio...</span> : <Button variant="secondary" onClick={fetchAnalysis}>Load Analysis</Button>}
                    </div>
                )}
            </CardContent>
        </Card>
    );
};

export default TaxBitWidget;
