import React, { useState, useEffect } from 'react';
import apiClient from '../../services/apiClient';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Loader2, ArrowUpCircle, ArrowDownCircle, RefreshCcw } from "lucide-react";
import { useToast } from "@/components/ui/use-toast";

const BinanceWidget = () => {
    const [symbol, setSymbol] = useState('BTCUSDT');
    const [ticker, setTicker] = useState(null);
    const [depth, setDepth] = useState(null);
    const [loading, setLoading] = useState(false);
    const [orderSide, setOrderSide] = useState('BUY');
    const [orderQty, setOrderQty] = useState('');
    const { toast } = useToast();

    const fetchData = async () => {
        setLoading(true);
        try {
        try {
            const tickerRes = await apiClient.get(`/binance/ticker/${symbol}`);
            const tickerData = tickerRes.data;
            setTicker(tickerData);

            const depthRes = await apiClient.get(`/binance/depth/${symbol}`, { params: { limit: 5 } });
            const depthData = depthRes.data;
            setDepth(depthData);
        } catch (error) {
            console.error("Error fetching Binance data:", error);
            toast({
                title: "Error",
                description: "Failed to fetch Binance data.",
                variant: "destructive"
            });
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchData();
        const interval = setInterval(fetchData, 5000); // Auto-refresh every 5s
        return () => clearInterval(interval);
    }, [symbol]);

    const handleOrder = async () => {
        if (!orderQty || isNaN(orderQty)) {
            toast({ title: "Invalid Quantity", description: "Please enter a valid number.", variant: "destructive" });
            return;
        }

        try {
            const res = await apiClient.post('/binance/order', {
                symbol: symbol,
                side: orderSide,
                quantity: parseFloat(orderQty)
            });
            const data = res.data;
            
            toast({
                title: "Order Placed",
                description: `Successfully ${data.side} ${data.executedQty} ${data.symbol} @ ${data.price}`,
            });
            fetchData(); // Refresh data
        } catch (error) {
            toast({ title: "Order Failed", description: error.message, variant: "destructive" });
        }
    };

    return (
        <Card className="w-full h-full bg-slate-950 border-slate-800 text-slate-100">
            <CardHeader className="pb-2">
                <div className="flex justify-between items-center">
                    <CardTitle className="flex items-center gap-2">
                        <img src="https://cryptologos.cc/logos/binance-coin-bnb-logo.svg?v=026" className="w-6 h-6" alt="Binance" />
                        Binance Exchange
                    </CardTitle>
                    <div className="flex items-center gap-2">
                        <Input 
                            value={symbol} 
                            onChange={(e) => setSymbol(e.target.value.toUpperCase())} 
                            className="w-24 h-8 bg-slate-900 border-slate-700" 
                        />
                        <Button variant="ghost" size="icon" onClick={fetchData} disabled={loading}>
                            {loading ? <Loader2 className="h-4 w-4 animate-spin" /> : <RefreshCcw className="h-4 w-4" />}
                        </Button>
                    </div>
                </div>
            </CardHeader>
            <CardContent>
                {ticker && (
                    <div className="grid grid-cols-2 gap-4 mb-4">
                        <div className="bg-slate-900 p-3 rounded-lg">
                            <div className="text-xs text-slate-400">Price</div>
                            <div className="text-xl font-bold font-mono">${ticker.lastPrice}</div>
                            <Badge variant={parseFloat(ticker.priceChangePercent) >= 0 ? "default" : "destructive"} className="mt-1">
                                {parseFloat(ticker.priceChangePercent) >= 0 ? '+' : ''}{ticker.priceChangePercent}%
                            </Badge>
                        </div>
                        <div className="bg-slate-900 p-3 rounded-lg">
                            <div className="text-xs text-slate-400">24h Volume</div>
                            <div className="text-lg font-mono">{parseFloat(ticker.volume).toLocaleString()}</div>
                            <div className="text-xs text-slate-500 mt-1">High: {ticker.highPrice}</div>
                        </div>
                    </div>
                )}

                <Tabs defaultValue="order" className="w-full">
                    <TabsList className="grid w-full grid-cols-2 bg-slate-900">
                        <TabsTrigger value="order">Trade</TabsTrigger>
                        <TabsTrigger value="depth">Depth</TabsTrigger>
                    </TabsList>
                    <TabsContent value="order" className="space-y-4 pt-4">
                        <div className="flex gap-2">
                            <Button 
                                variant={orderSide === 'BUY' ? "default" : "outline"} 
                                className={`w-1/2 ${orderSide === 'BUY' ? 'bg-green-600 hover:bg-green-700' : ''}`}
                                onClick={() => setOrderSide('BUY')}
                            >
                                Buy
                            </Button>
                            <Button 
                                variant={orderSide === 'SELL' ? "default" : "outline"} 
                                className={`w-1/2 ${orderSide === 'SELL' ? 'bg-red-600 hover:bg-red-700' : ''}`}
                                onClick={() => setOrderSide('SELL')}
                            >
                                Sell
                            </Button>
                        </div>
                        <div className="space-y-2">
                            <label className="text-xs text-slate-400">Quantity</label>
                            <Input 
                                type="number" 
                                value={orderQty} 
                                onChange={(e) => setOrderQty(e.target.value)} 
                                placeholder="0.00"
                                className="bg-slate-900 border-slate-700"
                            />
                        </div>
                        <Button className="w-full" onClick={handleOrder}>
                            {orderSide} {symbol}
                        </Button>
                    </TabsContent>
                    <TabsContent value="depth" className="pt-2">
                        <div className="space-y-1 font-mono text-xs">
                            {depth?.asks?.slice().reverse().map((ask, i) => (
                                <div key={`ask-${i}`} className="flex justify-between text-red-400">
                                    <span>{ask[0]}</span>
                                    <span>{ask[1]}</span>
                                </div>
                            ))}
                            <div className="h-px bg-slate-700 my-1" />
                            {depth?.bids?.map((bid, i) => (
                                <div key={`bid-${i}`} className="flex justify-between text-green-400">
                                    <span>{bid[0]}</span>
                                    <span>{bid[1]}</span>
                                </div>
                            ))}
                        </div>
                    </TabsContent>
                </Tabs>
            </CardContent>
        </Card>
    );
};

export default BinanceWidget;
