import React from 'react';
import { Badge } from "@/components/ui/badge";
import { FileText, CheckCircle2, AlertCircle, Clock } from 'lucide-react';

const JobRunHistory = ({ history = [] }) => {
    if (history.length === 0) {
        return (
            <div className="flex flex-col items-center justify-center py-20 text-gray-500 space-y-3">
                <FileText className="h-10 w-10 opacity-20" />
                <p>No execution history available.</p>
            </div>
        );
    }

    return (
        <div className="space-y-4">
            {history.map((entry) => (
                <div key={entry.execution_id} className="bg-gray-900/30 border border-gray-800/50 rounded-lg p-4 transition-all hover:border-gray-700">
                    <div className="flex justify-between items-start mb-3">
                        <div className="flex gap-3">
                            <div className={`mt-1 h-8 w-8 rounded-full flex items-center justify-center ${
                                entry.status === 'success' ? 'bg-green-950 text-green-400' : 'bg-red-950 text-red-400'
                            }`}>
                                {entry.status === 'success' ? <CheckCircle2 className="h-4 w-4" /> : <AlertCircle className="h-4 w-4" />}
                            </div>
                            <div>
                                <div className="flex items-center gap-2">
                                    <span className="text-white font-semibold">Run {entry.execution_id.split('-').pop()}</span>
                                    <Badge variant={entry.status === 'success' ? 'default' : 'destructive'} 
                                           className={`text-[10px] h-4 ${entry.status === 'success' ? 'bg-green-600' : ''}`}>
                                        {entry.status.toUpperCase()}
                                    </Badge>
                                </div>
                                <div className="flex items-center gap-3 text-xs text-gray-500 mt-1 font-mono">
                                    <span className="flex items-center gap-1"><Clock className="h-3 w-3" /> {new Date(entry.started_at).toLocaleString()}</span>
                                    <span>•</span>
                                    <span>Duration: {entry.duration_ms}ms</span>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <div className="relative">
                        <pre className="text-xs text-gray-400 bg-black/50 p-3 rounded border border-gray-800/50 font-mono overflow-x-auto max-h-40 scrollbar-thin scrollbar-thumb-gray-800">
                            {entry.logs}
                        </pre>
                        <div className="absolute top-2 right-2 flex gap-1">
                             <Badge variant="outline" className="bg-black/80 text-[10px] border-none text-gray-600">STDOUT</Badge>
                        </div>
                    </div>
                </div>
            ))}
        </div>
    );
};

export default JobRunHistory;
