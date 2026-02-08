import React, { useState, useEffect } from 'react';
import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogHeader,
    DialogTitle,
    DialogTrigger,
    DialogFooter,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Badge } from "@/components/ui/badge";
import { Settings, Eye, EyeOff, Save, Plus, Lock } from "lucide-react";
import { useToast } from "@/components/ui/use-toast";

const EnvVarsModal = ({ open, onOpenChange }) => {
    // const [open, setOpen] = useState(false); // Controlled by parent
    const [envVars, setEnvVars] = useState([]);
    const [loading, setLoading] = useState(false);
    const [searchQuery, setSearchQuery] = useState("");
    const [showSensitive, setShowSensitive] = useState({});
    const { toast } = useToast();

    // Edit/Add State
    const [editMode, setEditMode] = useState(false);
    const [currentKey, setCurrentKey] = useState("");
    const [currentValue, setCurrentValue] = useState("");

    const fetchEnvVars = async () => {
        setLoading(true);
        try {
            const response = await fetch('http://localhost:5050/api/v1/admin/env');
            if (response.ok) {
                const data = await response.json();
                setEnvVars(data);
            }
        } catch (error) {
            console.error("Failed to fetch env vars", error);
            toast({ title: "Error", description: "Failed to load environment variables.", variant: "destructive" });
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        if (open) fetchEnvVars();
    }, [open]);

    const handleSave = async () => {
        if (!currentKey.trim()) return;

        try {
            const response = await fetch('http://localhost:5050/api/v1/admin/env', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ key: currentKey, value: currentValue })
            });

            if (!response.ok) throw new Error("Failed to save variable");

            toast({ title: "Success", description: `Updated ${currentKey}` });
            setEditMode(false);
            setCurrentKey("");
            setCurrentValue("");
            fetchEnvVars();
        } catch (error) {
            toast({ title: "Error", description: error.message, variant: "destructive" });
        }
    };

    const toggleShow = (key) => {
        setShowSensitive(prev => ({ ...prev, [key]: !prev[key] }));
    };

    const filteredVars = envVars.filter(v => 
        v.key.toLowerCase().includes(searchQuery.toLowerCase())
    );

    return (
        <Dialog open={open} onOpenChange={onOpenChange}>
            {/* <DialogTrigger asChild> ... </DialogTrigger> Remove trigger, parent handles opening */}
            <DialogContent className="max-w-4xl max-h-[85vh] bg-gray-950 border-gray-800 text-white flex flex-col">
                <DialogHeader>
                    <DialogTitle>System Environment Variables</DialogTitle>
                    <DialogDescription>
                        Manage server-side configuration. Sensitive values are masked by default.
                    </DialogDescription>
                </DialogHeader>

                <div className="flex justify-between items-center my-4 gap-4">
                    <Input 
                        placeholder="Search variables..." 
                        value={searchQuery}
                        onChange={(e) => setSearchQuery(e.target.value)}
                        className="bg-gray-900 border-gray-700"
                    />
                    <Button onClick={() => { setEditMode(true); setCurrentKey(""); setCurrentValue(""); }}>
                        <Plus className="h-4 w-4 mr-2" /> Add Variable
                    </Button>
                </div>

                {editMode && (
                    <div className="bg-gray-900/50 p-4 rounded border border-blue-900/50 mb-4 animate-in fade-in slide-in-from-top-2">
                        <h4 className="text-sm font-medium mb-3 text-blue-400">Add / Edit Variable</h4>
                        <div className="grid gap-4">
                            <div className="grid grid-cols-2 gap-4">
                                <div className="space-y-2">
                                    <Label>Key</Label>
                                    <Input 
                                        value={currentKey} 
                                        onChange={(e) => setCurrentKey(e.target.value.toUpperCase())}
                                        placeholder="API_KEY"
                                        className="font-mono"
                                    />
                                </div>
                                <div className="space-y-2">
                                    <Label>Value</Label>
                                    <Input 
                                        value={currentValue}
                                        onChange={(e) => setCurrentValue(e.target.value)}
                                        type="password"
                                        placeholder="Value..."
                                    />
                                </div>
                            </div>
                            <div className="flex justify-end gap-2">
                                <Button variant="ghost" size="sm" onClick={() => setEditMode(false)}>Cancel</Button>
                                <Button size="sm" onClick={handleSave} className="bg-blue-600 hover:bg-blue-700">
                                    <Save className="h-4 w-4 mr-2" /> Save
                                </Button>
                            </div>
                        </div>
                    </div>
                )}

                <ScrollArea className="flex-1 rounded border border-gray-800 bg-black/50">
                    <Table>
                        <TableHeader className="bg-gray-900/50">
                            <TableRow>
                                <TableHead className="w-[300px]">Key</TableHead>
                                <TableHead>Value</TableHead>
                                <TableHead className="w-[100px] text-right">Action</TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {loading ? (
                                <TableRow>
                                    <TableCell colSpan={3} className="text-center py-8 text-gray-500">Loading...</TableCell>
                                </TableRow>
                            ) : filteredVars.length === 0 ? (
                                <TableRow>
                                    <TableCell colSpan={3} className="text-center py-8 text-gray-500">No variables found.</TableCell>
                                </TableRow>
                            ) : (
                                filteredVars.map((v) => (
                                    <TableRow key={v.key}>
                                        <TableCell className="font-mono text-xs font-semibold text-blue-300">
                                            {v.key}
                                            {v.is_sensitive && <Lock className="inline-block ml-2 h-3 w-3 text-yellow-500/50" />}
                                        </TableCell>
                                        <TableCell className="font-mono text-xs">
                                            <div className="flex items-center gap-2">
                                                <span className={v.is_sensitive && !showSensitive[v.key] ? "text-gray-600 tracking-widest" : "text-gray-300"}>
                                                    {v.is_sensitive && !showSensitive[v.key] ? "••••••••••••••••" : v.value}
                                                </span>
                                            </div>
                                        </TableCell>
                                        <TableCell className="text-right">
                                            <Button 
                                                variant="ghost" 
                                                size="icon" 
                                                className="h-6 w-6"
                                                onClick={() => {
                                                    setEditMode(true);
                                                    setCurrentKey(v.key);
                                                    setCurrentValue(""); // Don't pre-fill value for security if sensitive, or fetch raw if needed
                                                }}
                                            >
                                                <Settings className="h-3 w-3" />
                                            </Button>
                                        </TableCell>
                                    </TableRow>
                                ))
                            )}
                        </TableBody>
                    </Table>
                </ScrollArea>
            </DialogContent>
        </Dialog>
    );
};

export default EnvVarsModal;
