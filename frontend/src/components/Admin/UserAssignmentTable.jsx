import React from 'react';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { UserMinus, Shield, ShieldCheck, User } from 'lucide-react';

const UserAssignmentTable = ({ users = [], onRemoveUser }) => {
    return (
        <div className="bg-black/20 rounded-lg border border-gray-800">
            <Table>
                <TableHeader>
                    <TableRow className="border-gray-800 hover:bg-transparent">
                        <TableHead className="text-gray-500 uppercase text-[10px] tracking-widest">Identity</TableHead>
                        <TableHead className="text-gray-500 uppercase text-[10px] tracking-widest text-center">Permssions</TableHead>
                        <TableHead className="text-gray-500 uppercase text-[10px] tracking-widest text-right">Access</TableHead>
                    </TableRow>
                </TableHeader>
                <TableBody>
                    {users.map((user) => (
                        <TableRow key={user.user_id} className="border-gray-800 hover:bg-gray-800/20">
                            <TableCell className="py-4">
                                <div className="flex items-center gap-3">
                                    <div className="h-8 w-8 rounded bg-gray-800 flex items-center justify-center border border-gray-700 text-gray-400">
                                        <User className="h-4 w-4" />
                                    </div>
                                    <span className="text-white font-medium">{user.user_id}</span>
                                </div>
                            </TableCell>
                            <TableCell className="text-center">
                                <Badge className={`${
                                    user.role === 'admin' ? 'bg-indigo-900/30 text-indigo-400 border-indigo-500/50' : 'bg-gray-900/30 text-gray-400 border-gray-700'
                                } px-3 py-0.5 gap-1.5`}>
                                    {user.role === 'admin' ? <ShieldCheck className="h-3 w-3" /> : <Shield className="h-3 w-3" />}
                                    {user.role.toUpperCase()}
                                </Badge>
                            </TableCell>
                            <TableCell className="text-right">
                                <Button 
                                    variant="ghost" 
                                    size="sm" 
                                    className="text-gray-500 hover:text-red-400 hover:bg-red-950/20 h-8"
                                    onClick={() => onRemoveUser(user.user_id)}
                                    disabled={user.user_id === 'admin'}
                                >
                                    <UserMinus className="h-4 w-4 mr-2" /> Revoke
                                </Button>
                            </TableCell>
                        </TableRow>
                    ))}
                </TableBody>
            </Table>
        </div>
    );
};

export default UserAssignmentTable;
