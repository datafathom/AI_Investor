import React from 'react';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { PlayCircle, Clock, Activity, FileText, Settings2 } from 'lucide-react';

const JobScheduleTable = ({ jobs, onTrigger, onViewLogs, onEditSchedule }) => {
    return (
        <Table>
            <TableHeader>
                <TableRow className="border-gray-800 hover:bg-transparent">
                    <TableHead className="text-gray-400">Job Reference</TableHead>
                    <TableHead className="text-gray-400">Schedule</TableHead>
                    <TableHead className="text-gray-400">Last Execution</TableHead>
                    <TableHead className="text-gray-400">Status</TableHead>
                    <TableHead className="text-right text-gray-400">Control</TableHead>
                </TableRow>
            </TableHeader>
            <TableBody>
                {jobs.map((job) => (
                    <TableRow key={job.id} className="border-gray-800 hover:bg-gray-900/40 transition-colors">
                        <TableCell className="font-medium">
                            <div className="flex flex-col">
                                <span className="text-white flex items-center gap-2">
                                    {job.type === 'system' ? <Clock className="h-4 w-4 text-blue-400"/> : <Activity className="h-4 w-4 text-purple-400"/>}
                                    {job.name}
                                </span>
                                <span className="text-[10px] text-gray-500 font-mono mt-1">{job.id}</span>
                            </div>
                        </TableCell>
                        <TableCell>
                            <div className="flex items-center gap-2">
                                <code className="bg-black px-1.5 py-0.5 rounded text-xs text-green-400 font-mono">
                                    {job.schedule}
                                </code>
                                <Button variant="ghost" size="icon" className="h-6 w-6 text-gray-500 hover:text-white" onClick={() => onEditSchedule(job)}>
                                    <Settings2 className="h-3 w-3" />
                                </Button>
                            </div>
                        </TableCell>
                        <TableCell className="text-gray-400 text-sm">
                            {job.last_run ? new Date(job.last_run).toLocaleString([], { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' }) : 'Never'}
                        </TableCell>
                        <TableCell>
                            {job.status === 'running' && (
                                <Badge className="bg-blue-500/20 text-blue-400 border-blue-500/50 animate-pulse">
                                    RUNNING
                                </Badge>
                            )}
                            {job.status === 'idle' && (
                                <Badge variant="outline" className="text-gray-500 border-gray-800">
                                    IDLE
                                </Badge>
                            )}
                            {job.status === 'failed' && (
                                <Badge variant="destructive" className="bg-red-900/20 text-red-400 border-red-500/50">
                                    FAILED
                                </Badge>
                            )}
                        </TableCell>
                        <TableCell className="text-right space-x-1">
                            <Button 
                                variant="ghost" 
                                size="sm" 
                                className="text-gray-400 hover:text-white" 
                                onClick={() => onViewLogs(job.id)}
                            >
                                <FileText className="h-4 w-4" />
                            </Button>
                            <Button 
                                size="sm" 
                                variant="outline"
                                className="border-green-900/50 hover:bg-green-900/20 text-green-400 h-8 gap-1"
                                onClick={() => onTrigger(job.id)}
                                disabled={job.status === 'running'}
                            >
                                <PlayCircle className="h-4 w-4" /> Run
                            </Button>
                        </TableCell>
                    </TableRow>
                ))}
            </TableBody>
        </Table>
    );
};

export default JobScheduleTable;
