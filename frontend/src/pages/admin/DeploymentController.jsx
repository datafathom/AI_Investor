import React, { useState, useEffect } from 'react';
import apiClient from '../../services/apiClient';
import { ShieldCheck } from 'lucide-react';
import { useToast } from "@/components/ui/use-toast";

// Sub-components
import EnvironmentCard from '@/components/cards/EnvironmentCard';
import TrafficSlider from '@/components/controls/TrafficSlider';
import DeploymentTimeline from '@/components/Admin/DeploymentTimeline';
import RollbackConfirmModal from '@/components/modals/RollbackConfirmModal';

const API_BASE = '/admin/deployments';

const DeploymentController = () => {
    const [status, setStatus] = useState(null);
    const [loading, setLoading] = useState(true);
    const [isRollbackModalOpen, setIsRollbackModalOpen] = useState(false);
    const { toast } = useToast();

    // Fetch full status
    const fetchStatus = async () => {
        try {
            const data = await apiClient.get(`${API_BASE}/status`);
            
            // Inject traffic pct into environment data for easier rendering
            const enrichedData = {
                ...data,
                environments: {
                    blue: { ...data.environments.blue, traffic_pct: data.traffic_split.blue },
                    green: { ...data.environments.green, traffic_pct: data.traffic_split.green }
                }
            };
            setStatus(enrichedData);
        } catch (error) {
            toast({
                title: "Error",
                description: "Could not load deployment status.",
                variant: "destructive"
            });
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchStatus();
        const interval = setInterval(fetchStatus, 5000); // Poll every 5s
        return () => clearInterval(interval);
    }, []);

    // Handlers
    const handleSwitch = async (targetEnv) => {
        try {
            await apiClient.post(`${API_BASE}/switch`, { target_env: targetEnv });
            
            toast({
                title: "Environment Switched",
                description: `Active environment is now ${targetEnv.toUpperCase()}.`,
                variant: "success",
            });
            fetchStatus();
        } catch (error) {
            toast({ title: "Operation Failed", description: error.message, variant: "destructive" });
        }
    };

    const handleTrafficUpdate = async (bluePct) => {
        const greenPct = 100 - bluePct;
        
        // Optimistic UI update
        setStatus(prev => ({
            ...prev,
            traffic_split: { blue: bluePct, green: greenPct },
            environments: {
                blue: { ...prev.environments.blue, traffic_pct: bluePct },
                green: { ...prev.environments.green, traffic_pct: greenPct }
            }
        }));

        try {
            await apiClient.post(`${API_BASE}/traffic`, { blue: bluePct, green: greenPct });
        } catch (error) {
            toast({ title: "Traffic Update Failed", description: error.message, variant: "destructive" });
            fetchStatus(); // Revert on failure
        }
    };

    const handleRollback = async () => {
        setIsRollbackModalOpen(false);
        try {
            await apiClient.post(`${API_BASE}/rollback`);
            toast({ title: "Rollback Complete", description: "Reverted to previous state.", variant: "success" });
            fetchStatus();
        } catch (error) {
           toast({ title: "Rollback Failed", description: error.message, variant: "destructive" });
        }
    };

    if (loading && !status) return (
        <div className="flex flex-col items-center justify-center min-h-[400px] space-y-4">
            <ShieldCheck className="h-12 w-12 text-blue-500 animate-pulse" />
            <div className="text-gray-400 font-medium">Initializing Deployment Control...</div>
        </div>
    );

    return (
        <div className="p-6 max-w-7xl mx-auto space-y-8 animate-in fade-in duration-500">
            <header className="flex flex-col md:flex-row md:items-end justify-between gap-4">
                <div>
                    <h1 className="text-4xl font-extrabold tracking-tight text-white flex items-center gap-3">
                        <ShieldCheck className="h-10 w-10 text-blue-400" />
                        Infrastructure Operations
                    </h1>
                    <p className="text-muted-foreground mt-2 text-lg max-w-2xl">
                        Orchestrate Zero-Downtime deployments via Blue-Green traffic management and canary releases.
                    </p>
                </div>
                <div className="flex gap-3">
                    <button 
                        onClick={() => setIsRollbackModalOpen(true)}
                        className="px-4 py-2 bg-red-900/20 border border-red-800 text-red-400 hover:bg-red-900/40 rounded-md font-bold text-sm transition-all"
                    >
                        EMERGENCY ROLLBACK
                    </button>
                </div>
            </header>

            <div className="grid grid-cols-1 xl:grid-cols-3 gap-8">
                {/* Environment Control Pane */}
                <div className="xl:col-span-2 space-y-8">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <EnvironmentCard 
                            name="blue" 
                            data={status?.environments?.blue} 
                            isActive={status?.active_env === 'blue'}
                            onSwitch={handleSwitch}
                        />
                        <EnvironmentCard 
                            name="green" 
                            data={status?.environments?.green} 
                            isActive={status?.active_env === 'green'}
                            onSwitch={handleSwitch}
                        />
                    </div>

                    <TrafficSlider 
                        bluePct={status?.traffic_split?.blue ?? 50} 
                        onTrafficChange={handleTrafficUpdate} 
                    />
                </div>

                {/* Audit & Timeline Pane */}
                <div className="xl:col-span-1">
                    <DeploymentTimeline history={status?.history} />
                </div>
            </div>

            <RollbackConfirmModal 
                isOpen={isRollbackModalOpen} 
                onClose={() => setIsRollbackModalOpen(false)} 
                onConfirm={handleRollback} 
            />
        </div>
    );
};

export default DeploymentController;
