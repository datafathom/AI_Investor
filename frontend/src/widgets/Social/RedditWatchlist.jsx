import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Loader2, Plus, Trash2, ExternalLink, TrendingUp, TrendingDown } from "lucide-react";
import { useToast } from "@/components/ui/use-toast";

const RedditWatchlist = () => {
    const [users, setUsers] = useState([
        { name: "DeepFuckingValue", sentiment: 0.85, karma: "1.2M", status: "Active" },
        { name: "InverseCramer", sentiment: -0.4, karma: "450k", status: "Active" }
    ]);
    const [newUser, setNewUser] = useState("");
    const [loading, setLoading] = useState(false);
    const { toast } = useToast();

    // TODO: Connect to backend in  execution
    const addUser = () => {
        if (!newUser) return;
        setUsers([...users, { name: newUser, sentiment: 0.0, karma: "???", status: "Pending" }]);
        setNewUser("");
        toast({ title: "User Added", description: `Tracking ${newUser}` });
    };

    const removeUser = (name) => {
        setUsers(users.filter(u => u.name !== name));
    };

    const getSentimentColor = (score) => {
        if (score > 0.3) return "text-green-400";
        if (score < -0.3) return "text-red-400";
        return "text-slate-400";
    };

    return (
        <Card className="w-full h-full bg-slate-950 border-slate-800 text-slate-100">
            <CardHeader className="pb-2">
                <div className="flex justify-between items-center">
                    <CardTitle className="flex items-center gap-2">
                        <span className="text-orange-500 font-bold">r/</span>
                        Reddit Watchlist
                    </CardTitle>
                    <Badge variant="outline" className="border-orange-900 text-orange-400">
                        {users.length} Tracking
                    </Badge>
                </div>
            </CardHeader>
            <CardContent>
                <div className="flex gap-2 mb-4">
                    <Input 
                        placeholder="Add u/username..." 
                        value={newUser}
                        onChange={(e) => setNewUser(e.target.value)}
                        className="bg-slate-900 border-slate-700"
                    />
                    <Button onClick={addUser} size="icon" className="bg-orange-600 hover:bg-orange-700">
                        <Plus className="h-4 w-4" />
                    </Button>
                </div>

                <div className="space-y-3">
                    {users.map((user, i) => (
                        <div key={i} className="flex items-center justify-between bg-slate-900/50 p-3 rounded-lg border border-slate-800">
                            <div className="flex items-center gap-3">
                                <Avatar className="h-8 w-8">
                                    <AvatarImage src={`https://www.redditstatic.com/avatars/avatar_default_${i % 10 + 1}.png`} />
                                    <AvatarFallback>u/</AvatarFallback>
                                </Avatar>
                                <div>
                                    <div className="font-semibold text-sm">u/{user.name}</div>
                                    <div className="text-xs text-slate-500 flex gap-2">
                                        <span>{user.karma} karma</span>
                                        <span>•</span>
                                        <span className={user.status === 'Active' ? 'text-green-500' : 'text-slate-500'}>{user.status}</span>
                                    </div>
                                </div>
                            </div>
                            
                            <div className="flex items-center gap-4">
                                <div className={`flex items-center gap-1 font-mono text-sm ${getSentimentColor(user.sentiment)}`}>
                                    {user.sentiment > 0 ? <TrendingUp className="h-3 w-3" /> : <TrendingDown className="h-3 w-3" />}
                                    {user.sentiment > 0 ? '+' : ''}{user.sentiment}
                                </div>
                                <Button variant="ghost" size="icon" className="h-6 w-6 text-slate-500 hover:text-red-400" onClick={() => removeUser(user.name)}>
                                    <Trash2 className="h-3 w-3" />
                                </Button>
                            </div>
                        </div>
                    ))}
                </div>
            </CardContent>
        </Card>
    );
};

export default RedditWatchlist;
