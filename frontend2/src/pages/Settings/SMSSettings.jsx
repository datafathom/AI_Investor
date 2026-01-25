import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Switch } from "@/components/ui/switch";
import { Badge } from "@/components/ui/badge";
import { Label } from "@/components/ui/label";
import { 
    Phone, 
    ShieldCheck, 
    MessageSquare, 
    Bell, 
    Loader2, 
    CheckCircle2, 
    AlertTriangle,
    ArrowRight
} from "lucide-react";
import { useToast } from "@/components/ui/use-toast";

const SMSSettings = () => {
    const [phoneNumber, setPhoneNumber] = useState('');
    const [verificationCode, setVerificationCode] = useState('');
    const [step, setStep] = useState('input'); // input, verify, active
    const [loading, setLoading] = useState(false);
    const [alerts, setAlerts] = useState({
        margin_call: true,
        liquidation: true,
        trade_fill: false,
        news_flash: false
    });
    const { toast } = useToast();

    const handleSendCode = () => {
        if (phoneNumber.length < 10) {
            toast({ title: "Invalid Number", description: "Please enter a valid phone number.", variant: "destructive" });
            return;
        }
        setLoading(true);
        // Simulate OTP send
        setTimeout(() => {
            setLoading(false);
            setStep('verify');
            toast({ title: "Verification Code Sent", description: "Check your phone for a 6-digit code." });
        }, 1200);
    };

    const handleVerifyCode = () => {
        setLoading(true);
        // Simulate OTP verify
        setTimeout(() => {
            setLoading(false);
            setStep('active');
            toast({ title: "Number Verified", description: "SMS notifications are now active.", className: "bg-blue-900 text-white" });
        }, 1000);
    };

    const toggleAlert = (type) => {
        setAlerts(prev => ({ ...prev, [type]: !prev[type] }));
    };

    return (
        <div className="max-w-4xl mx-auto p-6 space-y-6 bg-slate-950 text-slate-100 min-h-screen font-sans">
            <div className="flex justify-between items-center">
                <div>
                    <h1 className="text-3xl font-bold flex items-center gap-3">
                        <Phone className="h-8 w-8 text-blue-500" />
                        SMS Notifications
                    </h1>
                    <p className="text-slate-400">Critical portfolio alerts delivered directly to your device</p>
                </div>
                {step === 'active' && <Badge className="bg-green-600 px-3 py-1">CONNECTED</Badge>}
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                {/* Configuration Card */}
                <Card className="bg-slate-900 border-slate-800">
                    <CardHeader>
                        <CardTitle className="text-lg">Phone Verification</CardTitle>
                        <CardDescription>Setup your mobile number for real-time alerting</CardDescription>
                    </CardHeader>
                    <CardContent className="space-y-6">
                        {step === 'input' && (
                            <div className="space-y-4">
                                <div className="space-y-2">
                                    <Label className="text-slate-500 uppercase text-[10px] font-bold">Mobile Number</Label>
                                    <Input 
                                        placeholder="+1 (555) 000-0000" 
                                        className="bg-slate-950 border-slate-700"
                                        value={phoneNumber}
                                        onChange={(e) => setPhoneNumber(e.target.value)}
                                    />
                                </div>
                                <Button className="w-full bg-blue-600 hover:bg-blue-700 font-bold" onClick={handleSendCode} disabled={loading}>
                                    {loading ? <Loader2 className="h-4 w-4 animate-spin mr-2" /> : <ShieldCheck className="h-4 w-4 mr-2" />}
                                    SEND VERIFICATION CODE
                                </Button>
                            </div>
                        )}

                        {step === 'verify' && (
                            <div className="space-y-4 animate-in fade-in slide-in-from-right-4">
                                <div className="space-y-2">
                                    <Label className="text-slate-500 uppercase text-[10px] font-bold">Enter 6-Digit Code</Label>
                                    <Input 
                                        placeholder="000000" 
                                        className="bg-slate-950 border-slate-700 font-mono text-center tracking-[0.5em] text-lg"
                                        maxLength={6}
                                        value={verificationCode}
                                        onChange={(e) => setVerificationCode(e.target.value)}
                                    />
                                </div>
                                <div className="flex gap-2">
                                    <Button variant="outline" className="flex-1 border-slate-700" onClick={() => setStep('input')}>BACK</Button>
                                    <Button className="flex-2 bg-green-600 hover:bg-green-700 font-bold" onClick={handleVerifyCode} disabled={loading}>
                                        {loading ? <Loader2 className="h-4 w-4 animate-spin mr-2" /> : <MessageSquare className="h-4 w-4 mr-2" />}
                                        VERIFY & ENABLE
                                    </Button>
                                </div>
                            </div>
                        )}

                        {step === 'active' && (
                            <div className="space-y-4 text-center py-6 animate-in zoom-in-95">
                                <div className="bg-blue-600/20 h-16 w-16 rounded-full flex items-center justify-center mx-auto mb-4 border border-blue-600/50">
                                    <CheckCircle2 className="h-8 w-8 text-blue-500" />
                                </div>
                                <div>
                                    <p className="font-bold text-lg">{phoneNumber}</p>
                                    <p className="text-slate-400 text-sm">Notifications are active and encrypted.</p>
                                </div>
                                <Button variant="ghost" className="text-slate-500 text-xs hover:text-red-400" onClick={() => setStep('input')}>
                                    CHANGE PHONE NUMBER
                                </Button>
                            </div>
                        )}
                    </CardContent>
                </Card>

                {/* Preferences Card */}
                <Card className="bg-slate-900 border-slate-800">
                    <CardHeader>
                        <CardTitle className="text-lg">Alert Preferences</CardTitle>
                        <CardDescription>Select which events trigger an SMS message</CardDescription>
                    </CardHeader>
                    <CardContent className="space-y-6">
                        <div className="space-y-4">
                            {[
                                { id: 'margin_call', label: 'Margin Calls', icon: AlertTriangle, color: 'text-red-500', desc: 'Alert when account margin falls below maintenance.' },
                                { id: 'liquidation', label: 'Liquidation Warnings', icon: Zap, color: 'text-yellow-500', desc: 'Pre-liquidation alerts for leveraged positions.' },
                                { id: 'trade_fill', label: 'Trade Execution', icon: ArrowRight, color: 'text-blue-500', desc: 'Confirmation when major orders are filled.' },
                                { id: 'news_flash', label: 'Market Extremes', icon: Bell, color: 'text-purple-500', desc: 'Alerts for Flash Crashes or 5%+ intraday swings.' }
                            ].map((item) => (
                                <div key={item.id} className="flex items-start justify-between p-3 rounded-lg bg-slate-950/50 border border-slate-800 hover:border-slate-700 transition-colors">
                                    <div className="flex gap-3">
                                        <div className={`mt-1 p-1 rounded ${item.color} bg-slate-900 border border-slate-800`}>
                                            <item.icon className="h-4 w-4" />
                                        </div>
                                        <div>
                                            <Label className="font-bold text-sm cursor-pointer" htmlFor={item.id}>{item.label}</Label>
                                            <p className="text-[10px] text-slate-500 leading-tight mt-0.5">{item.desc}</p>
                                        </div>
                                    </div>
                                    <Switch 
                                        id={item.id} 
                                        checked={alerts[item.id]} 
                                        onCheckedChange={() => toggleAlert(item.id)}
                                        disabled={step !== 'active'}
                                    />
                                </div>
                            ))}
                        </div>
                    </CardContent>
                </Card>
            </div>
            
            <div className="bg-blue-900/10 border border-blue-900/30 p-4 rounded-lg flex items-start gap-4">
                <ShieldCheck className="h-6 w-6 text-blue-500 shrink-0 mt-1" />
                <div>
                    <h4 className="text-sm font-bold text-blue-400">Carrier-Grade Reliability</h4>
                    <p className="text-xs text-blue-300 leading-relaxed italic">
                        SMS alerts are routed via Twilio's Super Network to ensure high delivery rates during market volatility. Carrier fees may apply.
                    </p>
                </div>
            </div>
        </div>
    );
};

export default SMSSettings;
