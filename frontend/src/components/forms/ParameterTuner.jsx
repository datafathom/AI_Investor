import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Settings2, RefreshCcw, Save } from "lucide-react";

const ParameterTuner = ({ indicator, onCalculate }) => {
    const [params, setParams] = useState({});

    useEffect(() => {
        if (indicator && indicator.default_params) {
            setParams(indicator.default_params);
        } else {
            setParams({});
        }
    }, [indicator]);

    const handleChange = (key, value) => {
        setParams(prev => ({
            ...prev,
            [key]: isNaN(value) ? value : Number(value)
        }));
    };

    if (!indicator) {
        return (
            <div className="h-full flex items-center justify-center border-2 border-dashed border-slate-800 rounded-xl bg-slate-950/20 p-8">
                <p className="text-slate-500 font-mono text-xs uppercase tracking-[0.2em] text-center">
                    Select an analytical node to initialize parameter tuning.
                </p>
            </div>
        );
    }

    return (
        <Card className="bg-slate-950/40 border-slate-800 backdrop-blur-md">
            <CardHeader className="p-4 border-b border-slate-900">
                <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                        <Settings2 className="h-4 w-4 text-indigo-400" />
                        <CardTitle className="text-xs font-black uppercase tracking-widest text-white">
                            Tuning_Module: {indicator.id.toUpperCase()}
                        </CardTitle>
                    </div>
                </div>
            </CardHeader>
            <CardContent className="p-4 space-y-6">
                <div className="grid grid-cols-1 gap-4">
                    {Object.entries(params).length > 0 ? (
                        Object.entries(params).map(([key, value]) => (
                            <div key={key} className="space-y-1.5">
                                <Label className="text-[10px] uppercase font-mono text-slate-500 tracking-wider flex justify-between">
                                    {key.replace(/_/g, ' ')}
                                    <span className="text-indigo-400">{value}</span>
                                </Label>
                                <Input 
                                    type={typeof value === 'number' ? 'number' : 'text'}
                                    value={value}
                                    onChange={(e) => handleChange(key, e.target.value)}
                                    className="bg-slate-900 border-slate-800 font-mono text-xs h-9 uppercase"
                                />
                            </div>
                        ))
                    ) : (
                        <p className="text-[10px] text-slate-600 font-mono italic">No tunable parameters found for this asset.</p>
                    )}
                </div>

                <div className="pt-4 border-t border-slate-900 flex gap-2">
                    <Button 
                        onClick={() => onCalculate(indicator.id, params)}
                        className="flex-1 bg-indigo-600 hover:bg-indigo-500 font-mono text-[10px] uppercase tracking-widest h-9"
                    >
                        <Save className="h-3 w-3 mr-2" />
                        Apply_Logic
                    </Button>
                    <Button 
                        variant="outline"
                        onClick={() => setParams(indicator.default_params || {})}
                        className="border-slate-800 bg-slate-950 text-slate-400 hover:bg-slate-900 h-9"
                    >
                        <RefreshCcw className="h-3 w-3" />
                    </Button>
                </div>
            </CardContent>
            <div className="p-2 bg-slate-900/50 flex items-center justify-between text-[8px] font-mono text-slate-600 uppercase tracking-widest">
                <span>Calc_Latency: 14ms</span>
                <span>Node: EXT_QUANT_LIB</span>
            </div>
        </Card>
    );
};

export default ParameterTuner;
