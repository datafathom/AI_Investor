import React, { useState, useEffect } from 'react';
import apiClient from '../../services/apiClient';
import { Card, CardContent, CardHeader, CardTitle, CardDescription, CardFooter } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { LayoutGrid, Save, Trash2, Upload, Plus, Monitor, ChevronLeft, ShieldAlert, Search } from 'lucide-react';
import { useToast } from "@/components/ui/use-toast";
import { useWidgetLayout } from '../../hooks/useWidgetLayout';
import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogHeader,
    DialogTitle,
    DialogFooter,
} from "@/components/ui/dialog";

const API_BASE = '/admin/workspaces';

const WorkspaceManager = () => {
    const [workspaces, setWorkspaces] = useState([]);
    const [loading, setLoading] = useState(true);
    const [searchTerm, setSearchTerm] = useState("");
    const [createDialogOpen, setCreateDialogOpen] = useState(false);
    const [selectedWorkspace, setSelectedWorkspace] = useState(null);
    const [newWorkspaceName, setNewWorkspaceName] = useState("");
    const { toast } = useToast();
    
    // Access layout hook to get current layout and load function
    const { saveWorkspace, loadWorkspace, activeWorkspace } = useWidgetLayout();

    // Fetch workspaces
    const fetchWorkspaces = async () => {
        try {
            const data = await apiClient.get(API_BASE);
            setWorkspaces(data);
        } catch (error) {
            console.error("Failed to fetch workspaces", error);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchWorkspaces();
    }, []);

    const handleCreateWorkspace = async () => {
        if (!newWorkspaceName.trim()) return;
        
        try {
            await apiClient.post(API_BASE, { name: newWorkspaceName });
            toast({ title: "Workspace Created", description: "Successfully provisioned new workspace.", variant: "success" });
            setCreateDialogOpen(false);
            setNewWorkspaceName("");
            fetchWorkspaces();
        } catch (error) {
            toast({ title: "Creation Failed", variant: "destructive" });
        }
    };

    const handleDelete = async (id) => {
        if (!confirm("Are you sure you want to decommission this workspace? This cannot be undone.")) return;
        try {
            await apiClient.delete(`${API_BASE}/${id}`);
            toast({ title: "Workspace Deleted" });
            if (selectedWorkspace?.id === id) setSelectedWorkspace(null);
            fetchWorkspaces();
        } catch (error) {
            toast({ title: "Deletion Failed", variant: "destructive" });
        }
    };

    const filteredWorkspaces = workspaces.filter(ws => 
        ws.name?.toLowerCase().includes(searchTerm.toLowerCase()) || 
        ws.id?.toLowerCase().includes(searchTerm.toLowerCase())
    );

    if (selectedWorkspace) {
        return (
            <div className="p-6 max-w-7xl mx-auto animate-in slide-in-from-right duration-300">
                <Button 
                    variant="ghost" 
                    className="mb-8 text-gray-400 hover:text-white pl-0" 
                    onClick={() => setSelectedWorkspace(null)}
                >
                    <ChevronLeft className="h-4 w-4 mr-2" /> Back to Workspace Grid
                </Button>

                <div className="flex flex-col md:flex-row md:items-end justify-between gap-6 mb-12">
                     <div>
                        <div className="flex items-center gap-3 mb-2">
                             <h1 className="text-4xl font-extrabold text-white">{selectedWorkspace.name}</h1>
                             <Badge variant="outline" className="bg-indigo-900/10 text-indigo-400 border-indigo-500/30 font-mono text-xs">
                                {selectedWorkspace.id}
                             </Badge>
                        </div>
                        <p className="text-gray-400 text-lg">Infrastructure management for current localized environment.</p>
                     </div>
                     <div className="flex gap-3">
                        <Button variant="outline" className="border-gray-800 text-gray-400">View Audit Logs</Button>
                        <Button variant="destructive" className="bg-red-900/20 text-red-500 border-red-500/50 hover:bg-red-900/40" onClick={() => handleDelete(selectedWorkspace.id)}>
                            Decommission Environment
                        </Button>
                     </div>
                </div>
            </div>
        );
    }

    return (
        <div className="p-6 max-w-7xl mx-auto animate-in fade-in duration-500">
            <header className="flex flex-col md:flex-row md:items-center justify-between gap-6 mb-12">
                <div>
                    <h1 className="text-4xl font-extrabold tracking-tight text-white flex items-center gap-3">
                        <LayoutGrid className="h-10 w-10 text-indigo-400" />
                        Workspace Orchestration
                    </h1>
                    <p className="text-muted-foreground mt-2 text-lg">
                        Manage isolated environments, resource allocation, and team containment policies.
                    </p>
                </div>
                <Button onClick={() => setCreateDialogOpen(true)} className="bg-indigo-600 hover:bg-indigo-500 text-white font-bold h-12 px-6 gap-2 shadow-lg shadow-indigo-900/20">
                    <Plus className="h-5 w-5" /> Initialize Workspace
                </Button>
            </header>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {loading ? (
                    <div className="col-span-full text-center py-20 text-gray-500">Scanning environments...</div>
                ) : (
                    filteredWorkspaces.map(ws => (
                        <Card key={ws.id} className="bg-gray-900/40 border-gray-800 hover:border-indigo-500/50 transition-all group">
                            <CardHeader>
                                <div className="flex justify-between items-start">
                                    <CardTitle className="text-white group-hover:text-indigo-400 transition-colors">{ws.name}</CardTitle>
                                    <Badge variant="outline" className="font-mono text-[10px] opacity-60">{ws.id.slice(0, 8)}</Badge>
                                </div>
                                <CardDescription>Provisioned: {new Date(ws.created_at).toLocaleDateString()}</CardDescription>
                            </CardHeader>
                            <CardFooter>
                                <Button variant="secondary" className="w-full" onClick={() => setSelectedWorkspace(ws)}>Manage Resources</Button>
                            </CardFooter>
                        </Card>
                    ))
                )}
            </div>

            <Dialog open={createDialogOpen} onOpenChange={setCreateDialogOpen}>
                <DialogContent className="bg-gray-950 border-gray-800 text-white">
                    <DialogHeader>
                        <DialogTitle>Provision Workspace</DialogTitle>
                        <DialogDescription>
                            Create a new isolated environment for team collaboration.
                        </DialogDescription>
                    </DialogHeader>
                    <div className="grid gap-4 py-4">
                        <div className="grid grid-cols-4 items-center gap-4">
                            <Label htmlFor="name" className="text-right">Name</Label>
                            <Input 
                                id="name" 
                                value={newWorkspaceName} 
                                onChange={(e) => setNewWorkspaceName(e.target.value)}
                                className="col-span-3 bg-gray-900 border-gray-700" 
                                placeholder="e.g., Alpha Quant Lab"
                            />
                        </div>
                    </div>
                    <DialogFooter>
                        <Button variant="outline" onClick={() => setCreateDialogOpen(false)}>Cancel</Button>
                        <Button onClick={handleCreateWorkspace}>Create Workspace</Button>
                    </DialogFooter>
                </DialogContent>
            </Dialog>
        </div>
    );
};

export default WorkspaceManager;
