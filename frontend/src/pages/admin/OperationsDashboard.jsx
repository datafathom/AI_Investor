import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Activity, RefreshCw } from 'lucide-react';
import { useToast } from "@/components/ui/use-toast";
import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogHeader,
    DialogTitle,
} from "@/components/ui/dialog";

// Sub-components
import JobScheduleTable from '@/components/admin/JobScheduleTable';
import JobRunHistory from '@/components/admin/JobRunHistory';

const API_BASE = '/api/v1/admin/ops';

const OperationsDashboard = () => {
    const [jobs, setJobs] = useState([]);
    const [loading, setLoading] = useState(true);
    const [logsOpen, setLogsOpen] = useState(false);
    const [selectedJob, setSelectedJob] = useState(null);
    const [jobHistory, setJobHistory] = useState([]);
    const { toast } = useToast();

    // Fetch initial data
    const fetchJobs = async () => {
        try {
            const response = await fetch(`${API_BASE}/jobs`);
            if (response.ok) {
                const data = await response.json();
                setJobs(data);
            }
        } catch (error) {
            console.error("Failed to fetch jobs", error);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchJobs();
        const interval = setInterval(fetchJobs, 10000); 
        return () => clearInterval(interval);
    }, []);

    const handleTriggerJob = async (jobId) => {
        try {
            toast({ title: "Triggering Job...", description: `Starting job ${jobId}` });
            const response = await fetch(`${API_BASE}/jobs/${jobId}/trigger`, {
                method: 'POST'
            });
            
            if (!response.ok) throw new Error("Failed to trigger job");
            
            const result = await response.json();
            
            toast({
                title: result.status === 'success' ? "Job Completed" : "Job Failed",
                description: `Execution ID: ${result.execution_id}`,
                variant: result.status === 'success' ? "success" : "destructive"
            });
            fetchJobs();
        } catch (error) {
            toast({ title: "Error", description: error.message, variant: "destructive" });
        }
    };

    const handleViewLogs = async (jobId) => {
        const job = jobs.find(j => j.id === jobId);
        setSelectedJob(job);
        setLogsOpen(true);
        try {
             const response = await fetch(`${API_BASE}/jobs/${jobId}/runs`);
             if (response.ok) {
                 const data = await response.json();
                 setJobHistory(data);
             }
        } catch (error) {
            toast({ title: "Error fetching logs", variant: "destructive" });
        }
    };

    const handleEditSchedule = (job) => {
        toast({ title: "Edit Schedule", description: `Updating schedule for ${job.id} (Feature Coming Soon)` });
    };

    return (
        <div className="p-6 max-w-7xl mx-auto space-y-6 animate-in fade-in duration-500">
            <header className="flex flex-col md:flex-row md:items-center justify-between gap-6 mb-8">
                <div>
                    <h1 className="text-4xl font-extrabold tracking-tight text-white flex items-center gap-3">
                        <Activity className="h-10 w-10 text-purple-400" />
                        Infrastructure Operations
                    </h1>
                    <p className="text-muted-foreground mt-2 text-lg">
                        Orchestrate background workers, scheduled pipelines, and automated intelligence tasks.
                    </p>
                </div>
                <div className="flex gap-2">
                    <Button variant="outline" className="border-gray-800" onClick={fetchJobs} disabled={loading}>
                        <RefreshCw className={`h-4 w-4 mr-2 ${loading ? 'animate-spin' : ''}`} />
                        Refresh State
                    </Button>
                </div>
            </header>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
                 {/* Summary Stats */}
                 <Card className="bg-gray-900/50 border-gray-800">
                    <CardHeader className="pb-2">
                        <CardTitle className="text-sm font-medium text-gray-400 uppercase tracking-wider">Total Registered Jobs</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="text-3xl font-bold text-white">{jobs.length}</div>
                    </CardContent>
                 </Card>
                 <Card className="bg-gray-900/50 border-gray-800">
                    <CardHeader className="pb-2">
                        <CardTitle className="text-sm font-medium text-gray-400 uppercase tracking-wider">Active Workers</CardTitle>
                    </CardHeader>
                    <CardContent>
                         <div className="text-3xl font-bold text-green-400">
                            {jobs.filter(j => j.status === 'running').length}
                         </div>
                    </CardContent>
                 </Card>
                 <Card className="bg-gray-900/50 border-gray-800">
                    <CardHeader className="pb-2">
                        <CardTitle className="text-sm font-medium text-gray-400 uppercase tracking-wider">Critical Failures (24h)</CardTitle>
                    </CardHeader>
                    <CardContent>
                         <div className="text-3xl font-bold text-red-500">
                            {jobs.filter(j => j.status === 'failed').length}
                         </div>
                    </CardContent>
                 </Card>
            </div>

            <Card className="bg-gray-900/40 border-gray-800">
                <CardHeader className="border-b border-gray-800/50 pb-4">
                    <div className="flex justify-between items-center">
                        <div>
                            <CardTitle className="text-xl">Job Registry</CardTitle>
                            <CardDescription>Managed automated tasks and system crons.</CardDescription>
                        </div>
                        <Badge variant="outline" className="bg-purple-900/10 text-purple-400 border-purple-500/30">
                            SCHEDULER: ACTIVE
                        </Badge>
                    </div>
                </CardHeader>
                <CardContent className="pt-6">
                    <JobScheduleTable 
                        jobs={jobs} 
                        onTrigger={handleTriggerJob} 
                        onViewLogs={handleViewLogs}
                        onEditSchedule={handleEditSchedule}
                    />
                </CardContent>
            </Card>

            {/* Logs Dialog */}
            <Dialog open={logsOpen} onOpenChange={setLogsOpen}>
                <DialogContent className="max-w-4xl max-h-[85vh] bg-gray-950 border-gray-800 text-white overflow-hidden flex flex-col p-0">
                    <DialogHeader className="p-6 border-b border-gray-800">
                        <div className="flex justify-between items-center">
                            <div>
                                <DialogTitle className="text-2xl font-bold flex items-center gap-2">
                                    <Activity className="h-6 w-6 text-purple-400" />
                                    {selectedJob?.name}
                                </DialogTitle>
                                <DialogDescription className="text-gray-400 mt-1 font-mono text-xs italic">
                                    UUID: {selectedJob?.id}
                                </DialogDescription>
                            </div>
                        </div>
                    </DialogHeader>
                    
                    <div className="flex-1 overflow-hidden">
                        <ScrollArea className="h-full max-h-[60vh] p-6 pt-2">
                            <JobRunHistory history={jobHistory} />
                        </ScrollArea>
                    </div>
                    
                    <div className="p-4 border-t border-gray-800 bg-gray-900/20 flex justify-between items-center">
                        <div className="text-xs text-gray-500">Showing last 10 execution cycles.</div>
                        <Button variant="ghost" size="sm" onClick={() => setLogsOpen(false)}>Close Inspector</Button>
                    </div>
                </DialogContent>
            </Dialog>
        </div>
    );
};

export default OperationsDashboard;
