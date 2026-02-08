import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription, CardFooter } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Layout, Save, Trash2, Upload, Plus, Monitor } from 'lucide-react';
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

const WorkspaceManager = () => {
    const [workspaces, setWorkspaces] = useState([]);
    const [loading, setLoading] = useState(true);
    const [createDialogOpen, setCreateDialogOpen] = useState(false);
    const [newWorkspaceName, setNewWorkspaceName] = useState("");
    const { toast } = useToast();
    
    // Access layout hook to get current layout and load function
    const { saveWorkspace, loadWorkspace, activeWorkspace } = useWidgetLayout();

    // Fetch workspaces
    const fetchWorkspaces = async () => {
        try {
            const response = await fetch('http://localhost:5050/api/v1/admin/workspaces');
            if (response.ok) {
                const data = await response.json();
                setWorkspaces(data);
            }
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
        
        // In a real app, we'd capture the *actual* current layout state here via the hook or store
        // For this demo, we'll assume the backend or hook handles the actual layout capture, 
        // OR we send a dummy layout if just creating the metadata.
        // Let's assume we want to save the "current" layout configuration.
        // Since `saveWorkspace` in the hook likely saves to localStorage, we'll simulate the API call here 
        // to persist it to our new backend.
        
        const currentLayoutMock = {
    const handleCreate = async (workspaceData) => {
        try {
            const response = await fetch(API_BASE, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(workspaceData)
            });
            if (response.ok) {
                toast({ title: "Workspace Created", description: "Successfully provisioned new workspace.", variant: "success" });
                fetchWorkspaces();
            }
        } catch (error) {
            toast({ title: "Creation Failed", variant: "destructive" });
        }
    };

    const handleDelete = async (id) => {
        if (!confirm("Are you sure you want to decommission this workspace? This cannot be undone.")) return;
        try {
            const response = await fetch(`${API_BASE}/${id}`, { method: 'DELETE' });
            if (response.ok) {
                toast({ title: "Workspace Deleted" });
                if (selectedWorkspace?.id === id) setSelectedWorkspace(null);
                fetchWorkspaces();
            }
        } catch (error) {
            toast({ title: "Deletion Failed", variant: "destructive" });
        }
    };

    const handleUpdateQuotas = async (updatedQuotas) => {
        try {
            const response = await fetch(`${API_BASE}/${selectedWorkspace.id}/quotas`, {
                method: 'PATCH',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(updatedQuotas)
            });
            if (response.ok) {
                toast({ title: "Quotas Updated", description: "Resource limits applied successfully.", variant: "success" });
                fetchWorkspaces();
            }
        } catch (error) {
            toast({ title: "Update Failed", variant: "destructive" });
        }
    };

    const handleRemoveUser = async (userId) => {
        try {
            const response = await fetch(`${API_BASE}/${selectedWorkspace.id}/users/${userId}`, { method: 'DELETE' });
            if (response.ok) {
                toast({ title: "User Removed", description: `Revoked access for ${userId}.` });
                fetchWorkspaces();
            }
        } catch (error) {
            toast({ title: "Revocation Failed", variant: "destructive" });
        }
    };

    const filteredWorkspaces = workspaces.filter(ws => 
        ws.name.toLowerCase().includes(searchTerm.toLowerCase()) || 
        ws.id.toLowerCase().includes(searchTerm.toLowerCase())
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

                <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                    <div className="lg:col-span-2 space-y-8">
                        <div className="space-y-4">
                            <h3 className="text-lg font-bold text-white flex items-center gap-2">
                                <Search className="h-4 w-4 text-indigo-400" /> Authorized Identities
                            </h3>
                            <UserAssignmentTable users={selectedWorkspace.users} onRemoveUser={handleRemoveUser} />
                            <div className="flex justify-start">
                                <Button size="sm" variant="outline" className="border-gray-800 text-indigo-400 hover:bg-indigo-900/10 border-dashed">
                                    <Plus className="h-4 w-4 mr-2" /> Invite Service Provider / User
                                </Button>
                            </div>
                        </div>
                    </div>

                    <div className="space-y-8">
                         <QuotaSettings quotas={selectedWorkspace.quotas} onUpdate={handleUpdateQuotas} />
                         
                         <div className="bg-amber-950/20 border border-amber-900/50 rounded-lg p-4">
                             <div className="flex gap-3">
                                <ShieldAlert className="h-5 w-5 text-amber-500 mt-0.5" />
                                <div>
                                    <p className="text-amber-200 text-sm font-bold">Policy Enforcement</p>
                                    <p className="text-amber-500/80 text-xs mt-1 leading-relaxed">
                                        Isolation is enforced at the network level. Users without valid tokens for this workspace will be automatically rejected.
                                    </p>
                                </div>
                             </div>
                         </div>
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
                <Button onClick={() => setIsCreateModalOpen(true)} className="bg-indigo-600 hover:bg-indigo-500 text-white font-bold h-12 px-6 gap-2 shadow-lg shadow-indigo-900/20">
                    <Plus className="h-5 w-5" /> Initialize Workspace
                </Button>
            </header>

                            </Button>
                        </CardFooter>
                    </Card>
                ))}
            </div>

            <Dialog open={createDialogOpen} onOpenChange={setCreateDialogOpen}>
                <DialogContent className="bg-gray-950 border-gray-800 text-white">
                    <DialogHeader>
                        <DialogTitle>Save Workspace</DialogTitle>
                        <DialogDescription>
                            Name your current layout configuration to access it later.
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
                                placeholder="e.g., Morning Focus"
                            />
                        </div>
                    </div>
                    <DialogFooter>
                        <Button variant="outline" onClick={() => setCreateDialogOpen(false)}>Cancel</Button>
                        <Button onClick={handleCreateWorkspace}>Save Workspace</Button>
                    </DialogFooter>
                </DialogContent>
            </Dialog>
        </div>
    );
};

export default WorkspaceManager;
