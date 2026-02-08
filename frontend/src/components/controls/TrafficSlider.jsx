import React from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Slider } from "@/components/ui/slider";
import { ArrowRightLeft } from 'lucide-react';

const TrafficSlider = ({ bluePct, onTrafficChange }) => {
    const greenPct = 100 - bluePct;

    return (
        <Card className="bg-gray-900/40 border-gray-800">
            <CardHeader>
                <CardTitle className="flex items-center gap-2 text-lg">
                    <ArrowRightLeft className="h-5 w-5 text-purple-400" />
                    Traffic Distribution
                </CardTitle>
                <CardDescription>
                    Shift production traffic between environments gradually for canary deployments.
                </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
                <div className="flex justify-between mb-2">
                    <div className="flex flex-col">
                        <span className="text-xs text-gray-500 uppercase font-semibold">Blue Exposure</span>
                        <span className="text-blue-400 font-bold text-xl">{bluePct}%</span>
                    </div>
                    <div className="flex flex-col items-end">
                        <span className="text-xs text-gray-500 uppercase font-semibold">Green Exposure</span>
                        <span className="text-green-400 font-bold text-xl">{greenPct}%</span>
                    </div>
                </div>
                
                <Slider
                    defaultValue={[50]}
                    value={[bluePct]}
                    max={100}
                    step={1}
                    onValueChange={(val) => onTrafficChange(val[0])}
                    className="py-4 cursor-pointer"
                />
                
                <div className="flex justify-between text-[10px] text-gray-600 font-mono">
                    <span>100% BLUE</span>
                    <span>50/50 SPLIT</span>
                    <span>100% GREEN</span>
                </div>
            </CardContent>
        </Card>
    );
};

export default TrafficSlider;
