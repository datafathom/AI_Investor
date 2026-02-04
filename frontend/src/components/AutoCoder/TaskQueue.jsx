import React from 'react';
import { Loader2, CheckCircle, XCircle, Clock } from 'lucide-react';

const TaskQueue = () => {
    const tasks = [
        { id: 101, name: 'Generate Momentum Strategy', status: 'Generating', progress: 65 },
        { id: 102, name: 'Unit Test: Backtester', status: 'Queued', progress: 0 },
        { id: 99, name: 'Refactor Data Pipeline', status: 'Completed', progress: 100 },
        { id: 98, name: 'Fix Neo4j Connection', status: 'Failed', progress: 80 },
    ];

    return (
        <div className="h-full flex flex-col">
            <h3 className="text-xs font-bold text-slate-500 uppercase px-2 mb-2 flex items-center justify-between">
                <span>Task Queue</span>
                <span className="text-cyan-400">2 Active</span>
            </h3>

            <div className="space-y-2 pr-2">
                {tasks.map(task => (
                    <div key={task.id} className="bg-slate-800/40 border border-slate-700 p-2 rounded hover:bg-slate-800 transition-colors">
                        <div className="flex justify-between items-center mb-1">
                            <span className="text-xs font-bold text-slate-300">{task.name}</span>
                            {task.status === 'Generating' && <Loader2 size={12} className="animate-spin text-cyan-400" />}
                            {task.status === 'Completed' && <CheckCircle size={12} className="text-green-400" />}
                            {task.status === 'Failed' && <XCircle size={12} className="text-red-400" />}
                            {task.status === 'Queued' && <Clock size={12} className="text-slate-500" />}
                        </div>

                        <div className="flex justify-between items-center text-[10px] text-slate-500 mb-1">
                            <span>ID: #{task.id}</span>
                            <span>{task.status}</span>
                        </div>

                        {task.status === 'Generating' && (
                            <div className="h-1 w-full bg-slate-700 rounded-full overflow-hidden">
                                <div className="h-full bg-cyan-500 animate-pulse" style={{ width: `${task.progress}%` }}></div>
                            </div>
                        )}
                    </div>
                ))}
            </div>
        </div>
    );
};

export default TaskQueue;
