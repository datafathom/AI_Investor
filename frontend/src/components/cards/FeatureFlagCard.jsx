import React from 'react';
import { Card, CardHeader, CardTitle, CardContent, CardFooter } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Switch } from "@/components/ui/switch";
import { Progress } from "@/components/ui/progress";
import { Button } from "@/components/ui/button";
import { Target, Users, Zap, Settings2 } from 'lucide-react';

const FeatureFlagCard = ({ name, flag, onToggle, onEdit }) => {
    return (
        <Card className="bg-gray-900/40 border-gray-800 hover:border-gray-700 transition-all">
            <CardHeader className="pb-2">
                <div className="flex justify-between items-start">
                    <div>
                        <CardTitle className="text-white text-lg font-bold">{name}</CardTitle>
                        <p className="text-[10px] text-gray-500 font-mono mt-1 italic">{flag.description || 'No description provided.'}</p>
                    </div>
                    <Switch 
                        checked={flag.enabled} 
                        onCheckedChange={() => onToggle(name)} 
                        className="data-[state=checked]:bg-green-600"
                    />
                </div>
            </CardHeader>
            <CardContent className="space-y-4 pt-4">
                <div className="space-y-1.5">
                    <div className="flex justify-between text-[11px] mb-1">
                        <span className="text-gray-500 uppercase tracking-widest flex items-center gap-1">
                            <Zap className="h-3 w-3" /> Rollout Percentage
                        </span>
                        <span className="font-mono text-gray-400">{flag.percentage}%</span>
                    </div>
                    <Progress value={flag.percentage} className="h-1 bg-gray-800" indicatorClassName="bg-indigo-500" />
                </div>

                <div className="flex gap-4">
                    <div className="flex items-center gap-1.5 text-[11px]">
                         <Target className="h-3 w-3 text-purple-400" />
                         <span className="text-gray-400">Targeting:</span>
                         <Badge variant="outline" className="h-4 text-[9px] border-gray-700 text-gray-400">
                            {(flag.targeting || []).length} RULES
                         </Badge>
                    </div>
                    <div className="flex items-center gap-1.5 text-[11px]">
                         <Users className="h-3 w-3 text-blue-400" />
                         <span className="text-gray-400">Impact:</span>
                         <span className="text-white">{(flag.percentage > 0 && flag.enabled) ? 'Active' : 'Dormant'}</span>
                    </div>
                </div>
            </CardContent>
            <CardFooter className="border-t border-gray-800/50 pt-4">
                <Button variant="ghost" size="sm" className="w-full text-gray-400 hover:text-white hover:bg-gray-800 h-8 gap-2" onClick={() => onEdit(name, flag)}>
                    <Settings2 className="h-3 w-3" /> Advanced Targeting & Configuration
                </Button>
            </CardFooter>
        </Card>
    );
};

export default FeatureFlagCard;
