import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Switch } from "@/components/ui/switch";
import { Badge } from "@/components/ui/badge";
import { 
    Loader2, 
    BellRing, 
    Hash, 
    Settings, 
    Send, 
    CheckCircle2, 
    AlertCircle, 
    ShieldAlert 
} from "lucide-react";
import { useToast } from "@/components/ui/use-toast";

const DiscordSettings = () => {
    const [webhookUrl, setWebhookUrl] = useState('');
    const [isConfigured, setIsConfigured] = useState(false);
    const [monitorAlpha, setMonitorAlpha] = useState(true);
    const [testLoading, setTestLoading] = useState(false);
    const { toast } = useToast();

    const handleSave = () => {
        if (!webhookUrl.includes('discord.com/api/webhooks/')) {
            toast({
                title: "Invalid URL",
                description: "This does not look like a valid Discord webhook URL.",
                variant: "destructive"
            });
            return;
        }
        setIsConfigured(true);
        toast({ title: "Settings Saved", description: "Webhook endpoint successfully registered." });
    };

    const runTest = async () => {
        setTestLoading(true);
        // Simulate test dispatch
        setTimeout(() => {
            setTestLoading(false);
            toast({
                title: "Test Alert Sent",
                description: "Check your Discord channel for the test embed.",
                className: "bg-green-900 border-green-800 text-white"
            });
        }, 1200);
    };

    return (
        <div className="max-w-4xl mx-auto p-6 space-y-6 bg-slate-950 text-slate-100 min-h-screen font-sans">
            <div className="flex justify-between items-center mb-6">
                <div>
                    <h1 className="text-3xl font-bold flex items-center gap-3">
                        <Settings className="h-8 w-8 text-blue-500" />
                        Discord Integration
                    </h1>
                    <p className="text-slate-400">Configure community monitoring and outbound alerts</p>
                </div>
                <Badge variant={isConfigured ? "default" : "outline"} className={isConfigured ? "bg-green-600" : "text-yellow-500 border-yellow-900"}>
                    {isConfigured ? "ACTIVE" : "PENDING CONFIG"}
                </Badge>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {/* Outbound Webhooks */}
                <Card className="md:col-span-2 bg-slate-900 border-slate-800">
                    <CardHeader>
                        <CardTitle className="flex items-center gap-2">
                             <BellRing className="h-5 w-5 text-blue-400" />
                             Alert Webhook
                        </CardTitle>
                        <CardDescription>Direct trade signals and news summaries to your Discord servers</CardDescription>
                    </CardHeader>
                    <CardContent className="space-y-4">
                        <div className="space-y-2">
                            <label className="text-xs font-bold text-slate-500 uppercase">Webhook URL</label>
                            <Input 
                                placeholder="https://discord.com/api/webhooks/..." 
                                value={webhookUrl}
                                onChange={(e) => setWebhookUrl(e.target.value)}
                                className="bg-slate-950 border-slate-700 font-mono text-xs"
                            />
                        </div>
                        <div className="flex gap-2">
                            <Button className="flex-1 bg-blue-600 hover:bg-blue-700 font-bold" onClick={handleSave}>
                                SAVE ENDPOINT
                            </Button>
                            <Button variant="outline" className="flex-1 border-slate-700 hover:bg-slate-800 font-bold" onClick={runTest} disabled={!isConfigured || testLoading}>
                                {testLoading ? <Loader2 className="h-4 w-4 animate-spin" /> : <Send className="h-4 w-4 mr-2" />}
                                TEST ALERT
                            </Button>
                        </div>
                    </CardContent>
                </Card>

                {/* Status Column */}
                <div className="space-y-6">
                    <Card className="bg-slate-900 border-slate-800">
                         <CardHeader className="pb-2">
                             <CardTitle className="text-sm font-bold flex items-center gap-2 uppercase tracking-widest text-slate-500">
                                 <ShieldAlert className="h-4 w-4" />
                                 Bot Status
                             </CardTitle>
                         </CardHeader>
                         <CardContent className="space-y-4">
                             <div className="flex justify-between items-center">
                                 <span className="text-xs text-slate-400">Alpha Monitoring</span>
                                 <Switch checked={monitorAlpha} onCheckedChange={setMonitorAlpha} />
                             </div>
                             <div className="pt-2">
                                 <div className="text-[10px] text-slate-500 uppercase font-bold mb-2">Connected Channels</div>
                                 <div className="space-y-1">
                                     <div className="text-xs flex items-center gap-2 text-slate-300">
                                         <Hash className="h-3 w-3 text-blue-400" />
                                         trading-floor
                                     </div>
                                     <div className="text-xs flex items-center gap-2 text-slate-300">
                                         <Hash className="h-3 w-3 text-blue-400" />
                                         alpha-sigs
                                     </div>
                                 </div>
                             </div>
                         </CardContent>
                    </Card>

                    <div className="bg-blue-900/10 border border-blue-900/30 p-4 rounded-lg">
                        <h4 className="text-xs font-bold text-blue-400 uppercase mb-1">PRO TIP</h4>
                        <p className="text-[10px] text-blue-300 italic leading-relaxed">
                            Connect multiple webhooks to separate "Macro News" from "Execution Alerts" in different channels.
                        </p>
                    </div>
                </div>
            </div>

            {/* Verification Mock Log */}
            <Card className="bg-slate-950 border-slate-800 font-mono mt-6">
                 <CardHeader className="py-2 border-b border-slate-800">
                     <div className="text-[10px] text-slate-500 font-bold uppercase">System Event Log (Mock)</div>
                 </CardHeader>
                 <CardContent className="p-4 h-32 overflow-y-auto text-[10px] space-y-1 text-green-500/80">
                      <div>[SYSTEM] Discord Bot Service initialized...</div>
                      <div>[SYSTEM] Listening to websocket gateway...</div>
                      <div>[MOCK] Event received: New mention of $BTC in #alpha-sigs</div>
                      <div>[MOCK] Dispatched trade alert to configured webhook...</div>
                      <div className="animate-pulse">_</div>
                 </CardContent>
            </Card>
        </div>
    );
};

export default DiscordSettings;
