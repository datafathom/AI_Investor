import React from 'react';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Eye, EyeOff, Save, Key, Globe } from 'lucide-react';

const EnvVarTable = ({ variables = [], onUpdate }) => {
    const [editValues, setEditValues] = React.useState({});
    const [showSensitive, setShowSensitive] = React.useState({});

    const toggleMask = (key) => {
        setShowSensitive(prev => ({ ...prev, [key]: !prev[key] }));
    };

    const handleValueChange = (key, val) => {
        setEditValues(prev => ({ ...prev, [key]: val }));
    };

    const handleSave = (key) => {
        if (editValues[key] !== undefined) {
            onUpdate(key, editValues[key]);
            // Clear edit state for this key
            const newEdits = { ...editValues };
            delete newEdits[key];
            setEditValues(newEdits);
        }
    };

    return (
        <div className="rounded-md border border-gray-800 bg-black/40">
            <Table>
                <TableHeader>
                    <TableRow className="border-gray-800 hover:bg-transparent">
                        <TableHead className="text-gray-500 text-[10px] uppercase tracking-widest pl-6">Variable Key</TableHead>
                        <TableHead className="text-gray-500 text-[10px] uppercase tracking-widest">Configured Value</TableHead>
                        <TableHead className="text-gray-500 text-[10px] uppercase tracking-widest text-right pr-6">Management</TableHead>
                    </TableRow>
                </TableHeader>
                <TableBody>
                    {variables.map((v) => (
                        <TableRow key={v.key} className="border-gray-800 hover:bg-gray-800/10">
                            <TableCell className="py-4 pl-6">
                                <div className="flex flex-col">
                                    <span className="text-white font-mono text-sm flex items-center gap-2">
                                        {v.is_sensitive ? <Key className="h-3 w-3 text-amber-500" /> : <Globe className="h-3 w-3 text-blue-400" />}
                                        {v.key}
                                    </span>
                                    <span className="text-[10px] text-gray-500 mt-1">Last Updated: {v.updated_at !== 'Unknown' ? new Date(v.updated_at).toLocaleDateString() : 'Initial'}</span>
                                </div>
                            </TableCell>
                            <TableCell>
                                <div className="flex items-center gap-2 max-w-md">
                                    <Input 
                                        type={v.is_sensitive && !showSensitive[v.key] ? "password" : "text"}
                                        value={editValues[v.key] ?? (v.is_sensitive && !showSensitive[v.key] ? "********" : v.value)}
                                        onChange={(e) => handleValueChange(v.key, e.target.value)}
                                        disabled={v.is_sensitive && !showSensitive[v.key] && editValues[v.key] === undefined}
                                        className="h-8 bg-gray-900/50 border-gray-700 text-gray-300 font-mono text-xs focus:ring-1 focus:ring-indigo-500"
                                    />
                                    {v.is_sensitive && (
                                        <Button variant="ghost" size="icon" className="h-8 w-8 text-gray-500" onClick={() => toggleMask(v.key)}>
                                            {showSensitive[v.key] ? <EyeOff className="h-3 w-3" /> : <Eye className="h-3 w-3" />}
                                        </Button>
                                    )}
                                </div>
                            </TableCell>
                            <TableCell className="text-right pr-6">
                                <Button 
                                    size="sm" 
                                    className="bg-indigo-600/10 text-indigo-400 border border-indigo-500/30 hover:bg-indigo-600 hover:text-white transition-all disabled:opacity-0"
                                    onClick={() => handleSave(v.key)}
                                    disabled={editValues[v.key] === undefined}
                                >
                                    <Save className="h-4 w-4 mr-2" /> Apply
                                </Button>
                            </TableCell>
                        </TableRow>
                    ))}
                </TableBody>
            </Table>
        </div>
    );
};

export default EnvVarTable;
