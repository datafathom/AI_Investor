import React, { useState, useEffect } from 'react';
import { Settings, ShieldAlert, History, Key, Info } from 'lucide-react';
import { Button } from "@/components/ui/button";
import { useToast } from "@/components/ui/use-toast";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";

// Sub-components
import EnvVarTable from '@/components/admin/EnvVarTable';
import EnvHistoryLog from '@/components/admin/EnvHistoryLog';

const API_BASE = '/api/v1/admin/env';

const EnvironmentSettings = () => {
    const [variables, setVariables] = useState([]);
    const [history, setHistory] = useState([]);
    const [loading, setLoading] = useState(true);
    const { toast } = useToast();

    const fetchData = async () => {
        try {
            const [varsRes, histRes] = await Promise.all([
                fetch(API_BASE),
                fetch(`${API_BASE}/history`)
            ]);

            if (varsRes.ok) setVariables(await varsRes.json());
            if (histRes.ok) setHistory(await histRes.json());
        } catch (error) {
            console.error("Failed to fetch environment data", error);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchData();
    }, []);

    const handleUpdateVar = async (key, value) => {
        try {
            const response = await fetch(API_BASE, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ key, value })
            });

            if (response.ok) {
                toast({ title: "Configuration Updated", description: `Changed value for ${key}.`, variant: "success" });
                fetchData();
            } else {
                throw new Error("Update failed");
            }
        } catch (error) {
            toast({ title: "Update Failed", description: "Verify backend permissions.", variant: "destructive" });
        }
    };

    return (
        <div className="p-6 max-w-7xl mx-auto space-y-8 animate-in fade-in duration-500">
             <header className="flex flex-col md:flex-row md:items-center justify-between gap-6 mb-8">
                <div>
                    <h1 className="text-4xl font-extrabold tracking-tight text-white flex items-center gap-3">
                        <Settings className="h-10 w-10 text-blue-400" />
                        System Configuration
                    </h1>
                    <p className="text-muted-foreground mt-2 text-lg">
                        Manage environment variables, secrets, and global runtime parameters.
                    </p>
                </div>
            </header>

            <Alert className="bg-amber-950/20 border-amber-900/50 text-amber-500">
                <ShieldAlert className="h-4 w-4" />
                <AlertTitle className="font-bold">Production Sovereignty Warning</AlertTitle>
                <AlertDescription className="text-xs opacity-90">
                    Modifying environment variables may require a service restart to take full effect. 
                    Sensitive keys are masked by default and encrypted at rest.
                </AlertDescription>
            </Alert>

            <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
                <div className="lg:col-span-3 space-y-6">
                    <div className="flex justify-between items-center mb-2">
                        <h3 className="text-xl font-bold text-white flex items-center gap-2">
                            <Key className="h-5 w-5 text-indigo-400" /> Environment Registry
                        </h3>
                        <div className="flex gap-2">
                            <Button variant="outline" size="sm" className="border-gray-800 h-8 text-xs" onClick={fetchData}>
                                Refresh Registry
                            </Button>
                        </div>
                    </div>

                    {loading ? (
                         <div className="space-y-3">
                            {[1, 2, 3, 4, 5].map(i => (
                                <div key={i} className="h-16 bg-gray-900/20 rounded border border-gray-800 animate-pulse" />
                            ))}
                         </div>
                    ) : (
                        <EnvVarTable variables={variables} onUpdate={handleUpdateVar} />
                    )}
                </div>

                <div className="space-y-8">
                    <div className="space-y-4">
                        <h3 className="text-lg font-bold text-white flex items-center gap-2">
                            <History className="h-4 w-4 text-gray-400" /> Audit Log
                        </h3>
                        <EnvHistoryLog history={history} />
                    </div>

                    <div className="bg-blue-950/10 border border-blue-900/30 rounded-lg p-5 space-y-3">
                        <div className="flex items-center gap-2">
                            <Info className="h-4 w-4 text-blue-400" />
                            <h4 className="text-sm font-bold text-blue-200 uppercase tracking-widest">Help</h4>
                        </div>
                        <p className="text-xs text-blue-400/80 leading-relaxed">
                            Changes made here update the project's root <code className="bg-blue-950 px-1 rounded">.env</code> file directly. 
                            If you are in a Docker container, ensure the file is mapped as a volume for persistence.
                        </p>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default EnvironmentSettings;
