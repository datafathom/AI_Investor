import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Save, AlertTriangle } from 'lucide-react';

const QuotaSettings = ({ quotas, onUpdate }) => {
    const [localQuotas, setLocalQuotas] = React.useState(quotas || {});

    React.useEffect(() => {
        setLocalQuotas(quotas || {});
    }, [quotas]);

    const handleChange = (key, val) => {
        setLocalQuotas(prev => ({ ...prev, [key]: parseFloat(val) || 0 }));
    };

    return (
        <Card className="bg-black/20 border-gray-800">
            <CardHeader className="pb-4">
                <CardTitle className="text-lg flex items-center gap-2">
                    <AlertTriangle className="h-4 w-4 text-amber-500" />
                    Resource Quota Enforcement
                </CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <div className="space-y-2">
                        <Label className="text-gray-400 text-xs uppercase tracking-widest font-bold">Storage Capacity (GB)</Label>
                        <Input 
                            type="number" 
                            value={localQuotas.storage_gb} 
                            onChange={(e) => handleChange('storage_gb', e.target.value)}
                            className="bg-gray-900 border-gray-700 text-white font-mono"
                        />
                    </div>
                    <div className="space-y-2">
                        <Label className="text-gray-400 text-xs uppercase tracking-widest font-bold">API Operations / Day</Label>
                        <Input 
                            type="number" 
                            value={localQuotas.api_calls_day} 
                            onChange={(e) => handleChange('api_calls_day', e.target.value)}
                            className="bg-gray-900 border-gray-700 text-white font-mono"
                        />
                    </div>
                    <div className="space-y-2">
                        <Label className="text-gray-400 text-xs uppercase tracking-widest font-bold">Max Concurrent Sessions</Label>
                        <Input 
                            type="number" 
                            value={localQuotas.concurrent_sessions} 
                            onChange={(e) => handleChange('concurrent_sessions', e.target.value)}
                            className="bg-gray-900 border-gray-700 text-white font-mono"
                        />
                    </div>
                </div>
                <div className="flex justify-end pt-2">
                    <Button 
                        onClick={() => onUpdate(localQuotas)}
                        className="bg-indigo-600 hover:bg-indigo-500 text-white gap-2 font-bold px-8"
                    >
                        <Save className="h-4 w-4" /> Commit Quota Changes
                    </Button>
                </div>
            </CardContent>
        </Card>
    );
};

export default QuotaSettings;
