import React, { useState, useEffect } from 'react';
import apiClient from '../../services/apiClient';
import { Zap, Search, Settings2, AlertTriangle } from 'lucide-react';
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { useToast } from "@/components/ui/use-toast";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogHeader,
    DialogTitle,
    DialogFooter
} from "@/components/ui/dialog";

// Sub-components
import FeatureFlagCard from '@/components/cards/FeatureFlagCard';

const API_BASE = '/api/v1/admin/features';

const FeatureFlagManager = () => {
    const [flags, setFlags] = useState({});
    const [loading, setLoading] = useState(true);
    const [searchTerm, setSearchTerm] = useState('');
    const [editingFlag, setEditingFlag] = useState(null);
    const [editData, setEditData] = useState(null);
    const { toast } = useToast();

    const fetchFlags = async () => {
        try {
            const response = await fetch(API_BASE);
            if (response.ok) {
                setFlags(await response.json());
            }
        } catch (error) {
            console.error("Failed to fetch flags", error);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchFlags();
    }, []);

    const handleToggle = async (name) => {
        try {
            const response = await fetch(`${API_BASE}/${name}/toggle`, { method: 'POST' });
            if (response.ok) {
                toast({ title: "Flag Toggled", description: `Updated ${name} status.`, variant: "success" });
                fetchFlags();
            }
        } catch (error) {
            toast({ title: "Toggle Failed", variant: "destructive" });
        }
    };

    const handleEdit = (name, flag) => {
        setEditingFlag(name);
        setEditData(flag);
    };

    const handleSaveConfig = async () => {
        try {
            const response = await fetch(`${API_BASE}/${editingFlag}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(editData)
            });

            if (response.ok) {
                toast({ title: "Configuration Saved", variant: "success" });
                setEditingFlag(null);
                fetchFlags();
            }
        } catch (error) {
            toast({ title: "Save Failed", variant: "destructive" });
        }
    };

    const filteredFlagNames = Object.keys(flags).filter(name => 
        name.toLowerCase().includes(searchTerm.toLowerCase()) || 
        flags[name].description?.toLowerCase().includes(searchTerm.toLowerCase())
    );

    return (
        <div className="p-6 max-w-7xl mx-auto space-y-8 animate-in fade-in duration-500">
             <header className="flex flex-col md:flex-row md:items-center justify-between gap-6 mb-8">
                <div>
                    <h1 className="text-4xl font-extrabold tracking-tight text-white flex items-center gap-3">
                        <Zap className="h-10 w-10 text-yellow-400 fill-yellow-400" />
                        Feature Containment
                    </h1>
                    <p className="text-muted-foreground mt-2 text-lg">
                        Control real-time availability of system features with percentage rollouts and targeting rules.
                    </p>
                </div>
            </header>

            <div className="flex items-center gap-4 mb-8">
                <div className="relative flex-1 max-w-md">
                    <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-500" />
                    <Input 
                        placeholder="Search flag registry..." 
                        className="pl-10 bg-gray-900/50 border-gray-800 text-white h-11"
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                    />
                </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {loading ? (
                    <div className="col-span-full py-20 text-center text-gray-500">Initializing registry...</div>
                ) : (
                    filteredFlagNames.map(name => (
                        <FeatureFlagCard 
                            key={name}
                            name={name}
                            flag={flags[name]}
                            onToggle={() => handleToggle(name)}
                            onEdit={() => handleEdit(name, flags[name])}
                        />
                    ))
                )}
            </div>
            
            <div className="mt-8 p-4 rounded-lg bg-blue-900/20 border border-blue-900/50 flex items-start gap-3">
                <AlertTriangle className="h-5 w-5 text-blue-400 mt-0.5" />
                <div className="text-sm text-blue-200">
                    <p className="font-semibold mb-1">About Feature Flags</p>
                    <p>Changes take effect immediately for new requests. Some active sessions may require a refresh to see changes.</p>
                </div>
            </div>

            {/* Edit Dialog */}
            <Dialog open={!!editingFlag} onOpenChange={() => setEditingFlag(null)}>
                <DialogContent className="bg-gray-950 border-gray-800 text-white">
                    <DialogHeader>
                        <DialogTitle>Update {editingFlag}</DialogTitle>
                        <DialogDescription>Modify targeting rules and rollout percentage.</DialogDescription>
                    </DialogHeader>
                    {editData && (
                        <div className="space-y-4 py-4">
                            <div className="space-y-2">
                                <label className="text-xs font-bold text-gray-500 uppercase">Rollout Percentage</label>
                                <Input 
                                    type="number" 
                                    value={editData.rollout_pct} 
                                    onChange={(e) => setEditData({...editData, rollout_pct: parseInt(e.target.value)})}
                                    className="bg-gray-900 border-gray-800"
                                />
                            </div>
                        </div>
                    )}
                    <DialogFooter>
                        <Button variant="ghost" onClick={() => setEditingFlag(null)}>Cancel</Button>
                        <Button onClick={handleSaveConfig} className="bg-indigo-600">Save Changes</Button>
                    </DialogFooter>
                </DialogContent>
            </Dialog>
        </div>
    );
};

export default FeatureFlagManager;
