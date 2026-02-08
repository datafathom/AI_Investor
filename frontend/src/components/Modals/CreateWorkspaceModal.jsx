import React from 'react';
import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogHeader,
    DialogTitle,
    DialogFooter
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";

const CreateWorkspaceModal = ({ isOpen, onClose, onCreate }) => {
    const [name, setName] = React.useState('');
    const [layout, setLayout] = React.useState('default');

    const handleCreate = () => {
        if (!name) return;
        onCreate({ name, layout: { type: layout } });
        setName('');
        onClose();
    };

    return (
        <Dialog open={isOpen} onOpenChange={onClose}>
            <DialogContent className="bg-gray-950 border-gray-800 text-white border-2">
                <DialogHeader>
                    <DialogTitle className="text-2xl font-bold">Initialize New Workspace</DialogTitle>
                    <DialogDescription className="text-gray-400 mt-2">
                        Create an isolated environment for specific trading teams or departments.
                    </DialogDescription>
                </DialogHeader>
                <div className="space-y-6 py-6 border-y border-gray-900 my-4">
                    <div className="space-y-2">
                        <Label className="text-indigo-400 uppercase text-[10px] font-bold tracking-[0.2em]">Workspace Identity</Label>
                        <Input 
                            placeholder="e.g. Asia High-Freq Desk" 
                            value={name}
                            onChange={(e) => setName(e.target.value)}
                            className="bg-black/50 border-gray-800 focus:border-indigo-500 h-12"
                        />
                    </div>
                    <div className="space-y-2">
                        <Label className="text-indigo-400 uppercase text-[10px] font-bold tracking-[0.2em]">Interface Configuration</Label>
                        <Select value={layout} onValueChange={setLayout}>
                            <SelectTrigger className="bg-black/50 border-gray-800 h-12">
                                <SelectValue placeholder="Select Layout" />
                            </SelectTrigger>
                            <SelectContent className="bg-gray-900 border-gray-800 text-white">
                                <SelectItem value="default">Standard Dashboard</SelectItem>
                                <SelectItem value="grid">Multi-View Grid</SelectItem>
                                <SelectItem value="terminal">Low-Latency Terminal</SelectItem>
                            </SelectContent>
                        </Select>
                    </div>
                </div>
                <DialogFooter className="gap-2 sm:gap-0">
                    <Button variant="ghost" onClick={onClose} className="text-gray-500 hover:text-white">Abort</Button>
                    <Button onClick={handleCreate} className="bg-indigo-600 hover:bg-indigo-500 font-bold px-8" disabled={!name}>
                        Provision Workspace
                    </Button>
                </DialogFooter>
            </DialogContent>
        </Dialog>
    );
};

export default CreateWorkspaceModal;
