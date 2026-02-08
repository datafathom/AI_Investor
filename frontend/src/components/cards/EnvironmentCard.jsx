import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { RefreshCw } from 'lucide-react';

const EnvironmentCard = ({ name, data, isActive, onSwitch, isTrafficActive }) => {
    const isHealthy = data?.status === 'healthy' || data?.status === 'active';
    
    return (
        <Card className={`border-l-4 transition-all duration-300 ${
            isActive 
                ? (name === 'blue' ? 'border-l-blue-500 bg-blue-500/10' : 'border-l-green-500 bg-green-500/10') 
                : 'border-l-gray-600 bg-gray-900/50'
        }`}>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className={`text-xl font-bold ${name === 'blue' ? 'text-blue-400' : 'text-green-500'}`}>
                    {name.toUpperCase()} Environment
                </CardTitle>
                {isActive && <Badge className={name === 'blue' ? "bg-blue-600" : "bg-green-600"}>ACTIVE</Badge>}
            </CardHeader>
            <CardContent>
                <div className="space-y-3 mt-4">
                    <div className="flex justify-between">
                        <span className="text-gray-400 text-sm">Version:</span>
                        <span className="font-mono text-sm">{data?.version || 'N/A'}</span>
                    </div>
                    <div className="flex justify-between border-b border-gray-800 pb-2">
                        <span className="text-gray-400 text-sm">Status:</span>
                        <span className={`text-sm font-semibold ${isHealthy ? "text-green-400" : "text-yellow-400"}`}>
                            {data?.status?.toUpperCase() || 'UNKNOWN'}
                        </span>
                    </div>
                    <div className="flex justify-between items-center py-2">
                        <span className="text-gray-400 text-sm">Traffic Exposure:</span>
                        <span className={`text-2xl font-bold ${isActive ? 'text-white' : 'text-gray-500'}`}>
                            {data?.traffic_pct ?? 0}%
                        </span>
                    </div>
                    
                    {!isActive && (
                        <Button 
                            className={`w-full mt-4 flex items-center gap-2 ${
                                name === 'blue' ? 'bg-blue-600 hover:bg-blue-700' : 'bg-green-600 hover:bg-green-700'
                            }`}
                            onClick={() => onSwitch(name)}
                        >
                            <RefreshCw className="h-4 w-4" />
                            Switch to {name.toUpperCase()}
                        </Button>
                    )}
                </div>
            </CardContent>
        </Card>
    );
};

export default EnvironmentCard;
