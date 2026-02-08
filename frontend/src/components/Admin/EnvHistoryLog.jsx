import React from 'react';
import { ScrollArea } from "@/components/ui/scroll-area";
import { Clock, User, ArrowRight } from 'lucide-react';

const EnvHistoryLog = ({ history = [] }) => {
    return (
        <div className="bg-black/30 border border-gray-800 rounded-lg overflow-hidden">
            <div className="bg-gray-900/50 px-4 py-2 border-b border-gray-800 flex justify-between items-center">
                <span className="text-[10px] uppercase tracking-widest font-bold text-gray-500">Change Audit History</span>
                <Clock className="h-3 w-3 text-gray-600" />
            </div>
            <ScrollArea className="h-[300px]">
                <div className="p-0">
                    {history.map((entry, idx) => (
                        <div key={idx} className="p-3 border-b border-gray-800/50 last:border-0 hover:bg-gray-800/10 transition-colors">
                            <div className="flex justify-between items-start mb-1">
                                <div className="flex items-center gap-2">
                                    <span className="bg-indigo-950 text-indigo-400 text-[9px] px-1.5 py-0.5 rounded font-bold uppercase tracking-tighter">
                                        {entry.action}
                                    </span>
                                    <code className="text-white text-[11px] font-mono">{entry.key}</code>
                                </div>
                                <span className="text-[10px] text-gray-500">{new Date(entry.timestamp).toLocaleTimeString()}</span>
                            </div>
                            <div className="flex items-center justify-between text-[10px] text-gray-600">
                                <span className="flex items-center gap-1.5"><User className="h-2.5 w-2.5" /> {entry.user}</span>
                                <span>{new Date(entry.timestamp).toLocaleDateString()}</span>
                            </div>
                        </div>
                    ))}
                    {history.length === 0 && (
                        <div className="py-12 text-center text-gray-600 text-xs italic">
                            No modifications logged in recent session.
                        </div>
                    )}
                </div>
            </ScrollArea>
        </div>
    );
};

export default EnvHistoryLog;
