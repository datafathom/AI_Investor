import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Badge } from "@/components/ui/badge";
import { History, GitBranch, Terminal } from 'lucide-react';

const DeploymentTimeline = ({ history = [] }) => {
    return (
        <Card className="bg-gray-900/40 border-gray-800">
            <CardHeader>
                <CardTitle className="flex items-center gap-2 text-lg">
                    <History className="h-5 w-5 text-blue-400" />
                    Deployment History
                </CardTitle>
            </CardHeader>
            <CardContent>
                <ScrollArea className="h-[300px] pr-4">
                    <div className="space-y-6 relative before:absolute before:inset-0 before:ml-5 before:-translate-x-px before:h-full before:w-0.5 before:bg-gradient-to-b before:from-transparent before:via-gray-800 before:to-transparent">
                        {history.length === 0 ? (
                            <div className="text-center py-10 text-gray-500 italic">No historical data available.</div>
                        ) : (
                            history.map((event, idx) => (
                                <div key={idx} className="relative flex items-start group">
                                    <div className={`mt-1 flex h-10 w-10 shrink-0 items-center justify-center rounded-full border border-gray-800 bg-gray-950 shadow-sm z-10 ${
                                        event.action === 'rollback' ? 'border-red-900' : 'border-blue-900'
                                    }`}>
                                        {event.action === 'rollback' ? (
                                            <Terminal className="h-5 w-5 text-red-500" />
                                        ) : (
                                            <GitBranch className="h-5 w-5 text-blue-400" />
                                        )}
                                    </div>
                                    <div className="ml-4 flex-1 pb-4">
                                        <div className="flex items-center justify-between">
                                            <p className="text-sm font-semibold capitalize text-gray-200">
                                                {event.action.replace('_', ' ')}
                                            </p>
                                            <time className="text-xs text-gray-500">
                                                {new Date(event.timestamp).toLocaleString([], { hour: '2-digit', minute: '2-digit', month: 'short', day: 'numeric' })}
                                            </time>
                                        </div>
                                        <div className="mt-1 text-xs text-gray-400">
                                            {event.action === 'switch' && (
                                                <span>Migrated traffic from <b>{event.from}</b> to <b>{event.to}</b>.</span>
                                            )}
                                            {event.action === 'traffic_update' && (
                                                <span>Adjusted split: Blue: {event.split.blue}% / Green: {event.split.green}%.</span>
                                            )}
                                            {event.action === 'rollback' && (
                                                <span className="text-red-400/80">Emergency rollback initiated to stable state.</span>
                                            )}
                                        </div>
                                    </div>
                                </div>
                            ))
                        )}
                    </div>
                </ScrollArea>
            </CardContent>
        </Card>
    );
};

export default DeploymentTimeline;
