import React from 'react';
import { Card, CardHeader, CardTitle, CardContent, CardFooter } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Users, HardDrive, Layout, Trash2, ArrowUpRight } from 'lucide-react';
import { Progress } from "@/components/ui/progress";

const WorkspaceCard = ({ workspace, onSelect, onDelete }) => {
    const storageUsage = workspace.usage?.storage_gb || 0;
    const storageQuota = workspace.quotas?.storage_gb || 10;
    const storagePct = Math.min((storageUsage / storageQuota) * 100, 100);

    return (
        <Card className="bg-gray-900/40 border-gray-800 hover:border-gray-700 transition-all group">
            <CardHeader className="pb-2">
                <div className="flex justify-between items-start">
                    <div>
                        <CardTitle className="text-white text-lg font-bold">{workspace.name}</CardTitle>
                        <span className="text-[10px] text-gray-500 font-mono tracking-tighter uppercase">{workspace.id}</span>
                    </div>
                    <Badge variant="outline" className="border-gray-700 text-gray-400 capitalize bg-gray-900/50">
                        {workspace.layout?.type || 'Standard'}
                    </Badge>
                </div>
            </CardHeader>
            <CardContent className="space-y-4 pt-2">
                <div className="flex justify-between text-xs">
                    <span className="text-gray-400 flex items-center gap-1.5">
                        <Users className="h-3 w-3" /> Members:
                    </span>
                    <span className="text-white font-medium">{(workspace.users || []).length}</span>
                </div>
                
                <div className="space-y-1.5">
                    <div className="flex justify-between text-[11px] mb-1">
                        <span className="text-gray-500 uppercase tracking-widest flex items-center gap-1">
                            <HardDrive className="h-3 w-3" /> Storage
                        </span>
                        <span className={`font-mono ${storagePct > 90 ? 'text-red-400' : 'text-gray-400'}`}>
                            {storageUsage.toFixed(1)} / {storageQuota}GB
                        </span>
                    </div>
                    <Progress value={storagePct} className="h-1 bg-gray-800" indicatorClassName={storagePct > 90 ? 'bg-red-500' : 'bg-blue-500'} />
                </div>
            </CardContent>
            <CardFooter className="border-t border-gray-800/50 pt-4 flex gap-2">
                <Button variant="outline" size="sm" className="w-full border-gray-800 bg-black/20 hover:bg-gray-800 text-gray-300" onClick={() => onSelect(workspace)}>
                    Manage <ArrowUpRight className="h-3 w-3 ml-1" />
                </Button>
                <Button variant="ghost" size="icon" className="h-8 w-8 text-gray-500 hover:text-red-400 hover:bg-red-950/20" onClick={() => onDelete(workspace.id)}>
                    <Trash2 className="h-4 w-4" />
                </Button>
            </CardFooter>
        </Card>
    );
};

export default WorkspaceCard;
