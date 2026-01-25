import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Slider } from "@/components/ui/slider";
import { Loader2, ArrowRightLeft, ShieldCheck, AlertTriangle } from "lucide-react";
import { useToast } from "@/components/ui/use-toast";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription, DialogFooter } from "@/components/ui/dialog";

const TradeTicket = () => {
    const [symbol, setSymbol] = useState('');
    const [side, setSide] = useState('buy');
    const [qty, setQty] = useState('');
    const [orderType, setOrderType] = useState('market');
    const [limitPrice, setLimitPrice] = useState('');
    const [stopPrice, setStopPrice] = useState('');
    const [loading, setLoading] = useState(false);
    const [confirmOpen, setConfirmOpen] = useState(false);
    const { toast } = useToast();

    // Mock price fetch
    const [marketPrice, setMarketPrice] = useState(null);

    useEffect(() => {
        if (symbol.length >= 2) {
            // Mock price updates
            const mockPrice = (Math.random() * 100 + 100).toFixed(2);
            setMarketPrice(mockPrice);
        }
    }, [symbol]);

    const handleReview = () => {
        if (!symbol || !qty) {
            toast({ title: "Validation Error", description: "Symbol and Quantity are required.", variant: "destructive" });
            return;
        }
        setConfirmOpen(true);
    };

    const submitOrder = async () => {
        setLoading(true);
        setConfirmOpen(false);
        try {
            // Simulate API call to AlpacaClient via backend
            await new Promise(r => setTimeout(r, 1000));
            
            toast({
                title: "Order Placed",
                description: `${side.toUpperCase()} ${qty} ${symbol} @ ${orderType === 'market' ? 'MKT' : limitPrice || stopPrice}`,
                className: "bg-green-900 border-green-800 text-white"
            });
            
            // Reset form
            setQty('');
        } catch (error) {
            toast({ title: "Order Failed", description: "Could not place order.", variant: "destructive" });
        } finally {
            setLoading(false);
        }
    };

    const estTotal = marketPrice && qty ? (parseFloat(marketPrice) * parseFloat(qty)).toFixed(2) : '0.00';

    return (
        <Card className="w-full h-full bg-slate-950 border-slate-800 text-slate-100 flex flex-col">
            <CardHeader className="pb-4 border-b border-slate-800 bg-slate-900/50">
                <div className="flex justify-between items-start">
                    <div>
                        <CardTitle className="flex items-center gap-2">
                            <ArrowRightLeft className="w-5 h-5 text-blue-400" />
                            Trade Execution
                        </CardTitle>
                        <CardDescription className="text-xs">Alpaca Markets (Paper Trading)</CardDescription>
                    </div>
                    <Badge variant="outline" className="bg-yellow-900/30 text-yellow-500 border-yellow-700">Paper Mode</Badge>
                </div>
            </CardHeader>
            <CardContent className="flex-1 pt-6 overflow-y-auto">
                <div className="space-y-4">
                    
                    {/* Symbol & Side */}
                    <div className="flex gap-3">
                        <div className="flex-1">
                            <label className="text-xs text-slate-400 font-medium ml-1">Symbol</label>
                            <Input 
                                placeholder="AAPL" 
                                value={symbol} 
                                onChange={(e) => setSymbol(e.target.value.toUpperCase())}
                                className="bg-slate-900 border-slate-700 font-mono"
                            />
                        </div>
                        <div className="w-1/3">
                            <label className="text-xs text-slate-400 font-medium ml-1">Action</label>
                            <Select value={side} onValueChange={setSide}>
                                <SelectTrigger className={`bg-slate-900 border-slate-700 ${side === 'buy' ? 'text-green-400' : 'text-red-400'}`}>
                                    <SelectValue />
                                </SelectTrigger>
                                <SelectContent>
                                    <SelectItem value="buy">BUY</SelectItem>
                                    <SelectItem value="sell">SELL</SelectItem>
                                </SelectContent>
                            </Select>
                        </div>
                    </div>

                    {/* Order Type */}
                    <div>
                         <label className="text-xs text-slate-400 font-medium ml-1">Order Type</label>
                         <Tabs value={orderType} onValueChange={setOrderType} className="w-full">
                            <TabsList className="grid w-full grid-cols-3 bg-slate-900">
                                <TabsTrigger value="market">Market</TabsTrigger>
                                <TabsTrigger value="limit">Limit</TabsTrigger>
                                <TabsTrigger value="stop">Stop</TabsTrigger>
                            </TabsList>
                        </Tabs>
                    </div>

                    {/* Quantity */}
                    <div>
                        <label className="text-xs text-slate-400 font-medium ml-1">Quantity (Shares)</label>
                        <Input 
                            type="number" 
                            placeholder="0" 
                            value={qty} 
                            onChange={(e) => setQty(e.target.value)}
                            className="bg-slate-900 border-slate-700"
                        />
                    </div>

                    {/* Conditional Inputs */}
                    {orderType === 'limit' && (
                        <div>
                            <label className="text-xs text-slate-400 font-medium ml-1">Limit Price</label>
                            <div className="relative">
                                <span className="absolute left-3 top-2.5 text-slate-500">$</span>
                                <Input 
                                    type="number" 
                                    placeholder="0.00" 
                                    value={limitPrice} 
                                    onChange={(e) => setLimitPrice(e.target.value)}
                                    className="bg-slate-900 border-slate-700 pl-7"
                                />
                            </div>
                        </div>
                    )}

                    {/* Summary Card */}
                    <div className="bg-slate-900 rounded p-4 space-y-2 text-sm border border-slate-800">
                         <div className="flex justify-between">
                             <span className="text-slate-400">Market Price</span>
                             <span className="font-mono">{marketPrice ? `$${marketPrice}` : '--'}</span>
                         </div>
                         <div className="flex justify-between font-semibold border-t border-slate-800 pt-2">
                             <span className="text-slate-300">Est. Total</span>
                             <span className="font-mono text-blue-300 text-lg">${estTotal}</span>
                         </div>
                    </div>

                    <Button 
                        size="lg" 
                        className={`w-full font-bold text-md ${side === 'buy' ? 'bg-green-600 hover:bg-green-700' : 'bg-red-600 hover:bg-red-700'}`}
                        onClick={handleReview}
                        disabled={loading}
                    >
                        {loading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
                        Review {side.toUpperCase()} Order
                    </Button>
                </div>
            </CardContent>

            {/* Confirmation Dialog */}
            <Dialog open={confirmOpen} onOpenChange={setConfirmOpen}>
                <DialogContent className="bg-slate-950 border-slate-800 text-slate-100">
                    <DialogHeader>
                        <DialogTitle>Confirm Order</DialogTitle>
                        <DialogDescription>
                            Please review your order details before submitting.
                        </DialogDescription>
                    </DialogHeader>
                    <div className="py-4 space-y-2">
                        <div className="flex justify-between items-center bg-slate-900 p-3 rounded">
                            <span className="text-slate-400">Symbol</span>
                            <span className="font-bold text-lg">{symbol}</span>
                        </div>
                        <div className="flex justify-between items-center bg-slate-900 p-3 rounded">
                            <span className="text-slate-400">Action</span>
                            <span className={`font-bold ${side === 'buy' ? 'text-green-400' : 'text-red-400'}`}>{side.toUpperCase()}</span>
                        </div>
                        <div className="flex justify-between items-center bg-slate-900 p-3 rounded">
                            <span className="text-slate-400">Quantity</span>
                            <span className="font-mono">{qty}</span>
                        </div>
                        <div className="flex justify-between items-center bg-slate-900 p-3 rounded">
                            <span className="text-slate-400">Type</span>
                            <span className="uppercase">{orderType}</span>
                        </div>
                        <div className="flex items-center gap-2 text-yellow-500 text-sm mt-4 bg-yellow-900/20 p-2 rounded border border-yellow-900/50">
                            <AlertTriangle className="h-4 w-4" />
                            <span>This is a PAPER TRADING order. No real funds will be used.</span>
                        </div>
                    </div>
                    <DialogFooter>
                        <Button variant="outline" onClick={() => setConfirmOpen(false)}>Cancel</Button>
                        <Button onClick={submitOrder} className="bg-blue-600 hover:bg-blue-700">Submit Order</Button>
                    </DialogFooter>
                </DialogContent>
            </Dialog>
        </Card>
    );
};

export default TradeTicket;
