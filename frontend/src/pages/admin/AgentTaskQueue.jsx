import React, { useState, useEffect } from 'react';
import { agentTaskService } from '../../services/agentTaskService';
import { Play, Pause, RotateCcw, XCircle, CheckCircle, Clock, AlertCircle } from 'lucide-react';
import { toast } from 'sonner';

const StatusBadge = ({ status }) => {
    const styles = {
        pending: 'bg-slate-800 text-slate-400 border-slate-700',
        running: 'bg-blue-500/20 text-blue-400 border-blue-500/30 animate-pulse',
        completed: 'bg-emerald-500/20 text-emerald-400 border-emerald-500/30',
        failed: 'bg-red-500/20 text-red-400 border-red-500/30',
        cancelled: 'bg-slate-700 text-slate-500 border-slate-600',
    };
    return (
        <span className={`px-2 py-1 rounded text-xs font-bold border ${styles[status.toLowerCase()] || styles.pending}`}>
            {status.toUpperCase()}
        </span>
    );
};

const AgentTaskQueue = () => {
    const [tasks, setTasks] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        loadTasks();
        const interval = setInterval(loadTasks, 5000);
        return () => clearInterval(interval);
    }, []);

    const loadTasks = async () => {
        try {
            const res = await agentTaskService.getTasks();
            setTasks(res);
            setLoading(false);
        } catch (e) {
            console.error("Failed to load tasks");
        }
    };

    const handleCancel = async (taskId) => {
        try {
            await agentTaskService.cancelTask(taskId);
            toast.success("Task cancelled");
            loadTasks();
        } catch (e) {
            toast.error("Failed to cancel task");
        }
    };

    const handleRetry = async (taskId) => {
        try {
            await agentTaskService.retryTask(taskId);
            toast.success("Task retried");
            loadTasks();
        } catch (e) {
            toast.error("Failed to retry task");
        }
    };

    return (
        <div className="h-full bg-slate-950 p-6 text-slate-200 overflow-y-auto">
            <h1 className="text-2xl font-bold text-white mb-6 flex items-center gap-2">
                <Clock className="text-cyan-500" /> Task Queue
            </h1>

            <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden">
                <table className="w-full text-left text-sm">
                    <thead className="bg-slate-950 text-slate-500 uppercase font-bold text-xs">
                        <tr>
                            <th className="p-4">Task Name</th>
                            <th className="p-4">Assigned Agent</th>
                            <th className="p-4">Priority</th>
                            <th className="p-4">Status</th>
                            <th className="p-4">Created At</th>
                            <th className="p-4 text-right">Actions</th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-800">
                        {loading && tasks.length === 0 ? (
                             <tr><td colSpan="6" className="p-8 text-center"><div className="animate-spin rounded-full h-8 w-8 border-b-2 border-cyan-500 mx-auto"></div></td></tr>
                        ) : tasks.length === 0 ? (
                            <tr><td colSpan="6" className="p-8 text-center text-slate-500">No tasks in queue</td></tr>
                        ) : tasks.map(task => (
                            <tr key={task.id} className="hover:bg-slate-800/50 transition-colors">
                                <td className="p-4 font-bold text-white">{task.name}</td>
                                <td className="p-4 font-mono text-cyan-400">{task.assigned_agent}</td>
                                <td className="p-4">
                                    <span className={`text-xs font-bold ${task.priority === 'CRITICAL' ? 'text-red-500' : task.priority === 'HIGH' ? 'text-orange-400' : 'text-slate-400'}`}>
                                        {task.priority}
                                    </span>
                                </td>
                                <td className="p-4"><StatusBadge status={task.status} /></td>
                                <td className="p-4 text-slate-500 font-mono text-xs">{new Date(task.created_at).toLocaleTimeString()}</td>
                                <td className="p-4 text-right flex justify-end gap-2">
                                    {['pending', 'running'].includes(task.status) && (
                                        <button onClick={() => handleCancel(task.id)} className="p-1 hover:bg-slate-700 rounded text-red-400" title="Cancel">
                                            <XCircle size={16} />
                                        </button>
                                    )}
                                    {['failed', 'cancelled'].includes(task.status) && (
                                        <button onClick={() => handleRetry(task.id)} className="p-1 hover:bg-slate-700 rounded text-emerald-400" title="Retry">
                                            <RotateCcw size={16} />
                                        </button>
                                    )}
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default AgentTaskQueue;
