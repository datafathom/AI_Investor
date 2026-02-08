import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Shield, Calendar, AlertTriangle, RefreshCcw, Lock, CheckCircle } from "lucide-react";
import { useToast } from "@/components/ui/use-toast";
import { motion } from "framer-motion";

const Rule144CompliancePage = () => {
    const [dashboard, setDashboard] = useState(null);
    const [lockups, setLockups] = useState([]);
    const [loading, setLoading] = useState(true);
    const { toast } = useToast();

    const fetchData = async () => {
        setLoading(true);
        try {
            const [dashRes, lockupsRes] = await Promise.all([
                fetch('http://localhost:5050/api/v1/compliance/144a/dashboard'),
                fetch('http://localhost:5050/api/v1/compliance/144a/lockups')
            ]);
            
            if (dashRes.ok) setDashboard(await dashRes.json());
            if (lockupsRes.ok) setLockups(await lockupsRes.json());
            
        } catch (error) {
            console.error("Failed to fetch compliance data", error);
            toast({ title: "Error", description: "Failed to load compliance data.", variant: "destructive" });
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchData();
    }, []);

    const getImpactColor = (severity) => {
        switch (severity) {
            case "HIGH": return "text-red-400 bg-red-900/20 border-red-900";
            case "MEDIUM": return "text-yellow-400 bg-yellow-900/20 border-yellow-900";
            default: return "text-green-400 bg-green-900/20 border-green-900";
        }
    };

    return (
        <div className="p-6 space-y-6 max-w-7xl mx-auto text-white animate-in fade-in">
            {/* Header */}
            <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
                <div>
                    <h1 className="text-3xl font-bold flex items-center gap-2">
                        <Shield className="h-8 w-8 text-amber-500" />
                        Rule 144A Compliance
                    </h1>
                    <p className="text-gray-400 mt-1">Track holding periods, lockups, and sale eligibility.</p>
                </div>
                <Button onClick={fetchData} variant="outline" className="gap-2" disabled={loading}>
                    <RefreshCcw className={`h-4 w-4 ${loading ? 'animate-spin' : ''}`} /> Refresh
                </Button>
            </div>

            {/* Dashboard Summary Cards */}
            {dashboard && (
                <motion.div 
                    initial={{ opacity: 0, y: 10 }} 
                    animate={{ opacity: 1, y: 0 }}
                    className="grid grid-cols-2 md:grid-cols-4 gap-4"
                >
                    <Card className="bg-gray-900/50 border-gray-800">
                        <CardHeader className="pb-2">
                            <CardDescription className="flex items-center gap-1">
                                <Lock className="h-3 w-3" /> Restricted Positions
                            </CardDescription>
                            <CardTitle className="text-2xl">{dashboard.total_restricted_positions}</CardTitle>
                        </CardHeader>
                    </Card>
                    <Card className="bg-gray-900/50 border-gray-800">
                        <CardHeader className="pb-2">
                            <CardDescription className="flex items-center gap-1">
                                <CheckCircle className="h-3 w-3" /> Eligible This Month
                            </CardDescription>
                            <CardTitle className="text-2xl text-green-400">{dashboard.positions_eligible_this_month}</CardTitle>
                        </CardHeader>
                    </Card>
                    <Card className="bg-gray-900/50 border-gray-800">
                        <CardHeader className="pb-2">
                            <CardDescription className="flex items-center gap-1">
                                <Calendar className="h-3 w-3" /> Upcoming Lockups (30d)
                            </CardDescription>
                            <CardTitle className="text-2xl text-yellow-400">{dashboard.upcoming_lockups_30d}</CardTitle>
                        </CardHeader>
                    </Card>
                    <Card className="bg-gray-900/50 border-gray-800">
                        <CardHeader className="pb-2">
                            <CardDescription>Volume Sold (QTD)</CardDescription>
                            <CardTitle className="text-2xl">
                                {dashboard.volume_sold_this_quarter_pct}%
                                <span className="text-sm text-gray-400 font-normal ml-1">/ 25%</span>
                            </CardTitle>
                        </CardHeader>
                    </Card>
                </motion.div>
            )}

            <Tabs defaultValue="lockups" className="w-full">
                <TabsList className="grid w-full grid-cols-1 mb-4">
                    <TabsTrigger value="lockups">Upcoming Lockup Expirations</TabsTrigger>
                </TabsList>

                <TabsContent value="lockups">
                    <Card className="bg-gray-900/50 border-gray-800">
                        <CardHeader>
                            <CardTitle className="flex items-center gap-2">
                                <Calendar className="h-5 w-5" /> Lockup Expirations (90 Days)
                            </CardTitle>
                        </CardHeader>
                        <CardContent>
                            {loading ? (
                                <div className="text-center py-10 text-gray-500">Loading...</div>
                            ) : (
                                <Table>
                                    <TableHeader>
                                        <TableRow>
                                            <TableHead>Ticker</TableHead>
                                            <TableHead>Expiration</TableHead>
                                            <TableHead>Days</TableHead>
                                            <TableHead>Shares</TableHead>
                                            <TableHead>Holder Type</TableHead>
                                            <TableHead>Impact</TableHead>
                                        </TableRow>
                                    </TableHeader>
                                    <TableBody>
                                        {lockups.map((l, idx) => (
                                            <TableRow key={idx} className="hover:bg-gray-800/50">
                                                <TableCell className="font-mono font-bold">{l.ticker}</TableCell>
                                                <TableCell>{l.expiration_date}</TableCell>
                                                <TableCell className={l.days_remaining <= 7 ? 'text-red-400' : ''}>
                                                    {l.days_remaining}d
                                                </TableCell>
                                                <TableCell>{l.shares_unlocking.toLocaleString()}</TableCell>
                                                <TableCell>
                                                    <Badge variant="outline">{l.holder_type}</Badge>
                                                </TableCell>
                                                <TableCell>
                                                    <Badge variant="outline" className={getImpactColor(l.impact_severity)}>
                                                        {l.impact_severity}
                                                    </Badge>
                                                </TableCell>
                                            </TableRow>
                                        ))}
                                    </TableBody>
                                </Table>
                            )}
                        </CardContent>
                    </Card>
                </TabsContent>
            </Tabs>
        </div>
    );
};

export default Rule144CompliancePage;
