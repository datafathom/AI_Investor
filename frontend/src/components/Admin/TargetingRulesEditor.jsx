import React from 'react';
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { Slider } from "@/components/ui/slider";
import { Button } from "@/components/ui/button";
import { Plus, Trash2, Target, AlertCircle } from 'lucide-react';
import { Badge } from "@/components/ui/badge";

const TargetingRulesEditor = ({ flag, onUpdate }) => {
    const [percentage, setPercentage] = React.useState(flag.percentage || 0);
    const [rules, setRules] = React.useState(flag.targeting || []);

    const handlePercentageChange = (val) => {
        setPercentage(val[0]);
        onUpdate({ ...flag, percentage: val[0], targeting: rules });
    };

    const addRule = () => {
        const newRule = { attribute: 'user_id', operator: 'in', values: [] };
        const newRules = [...rules, newRule];
        setRules(newRules);
        onUpdate({ ...flag, percentage, targeting: newRules });
    };

    const removeRule = (idx) => {
        const newRules = rules.filter((_, i) => i !== idx);
        setRules(newRules);
        onUpdate({ ...flag, percentage, targeting: newRules });
    };

    return (
        <div className="space-y-8 py-4">
             <div className="space-y-4">
                <div className="flex justify-between items-center">
                    <Label className="text-gray-400 uppercase text-[10px] font-bold tracking-widest">Traffic Exposure</Label>
                    <span className="text-indigo-400 font-mono font-bold">{percentage}%</span>
                </div>
                <Slider 
                    value={[percentage]} 
                    max={100} 
                    step={1} 
                    onValueChange={handlePercentageChange}
                    className="py-4"
                />
                <p className="text-[10px] text-gray-500 italic">Determines the percentage of users (randomly or by bucket) who will see this feature enabled.</p>
            </div>

            <div className="space-y-4">
                <div className="flex justify-between items-center">
                    <Label className="text-gray-400 uppercase text-[10px] font-bold tracking-widest">Segment Targeting</Label>
                    <Button variant="ghost" size="sm" className="h-6 text-[10px] text-indigo-400 hover:text-indigo-300" onClick={addRule}>
                        <Plus className="h-3 w-3 mr-1" /> Add Rule
                    </Button>
                </div>
                
                <div className="space-y-3">
                    {rules.map((rule, idx) => (
                        <div key={idx} className="bg-gray-900/50 border border-gray-800 rounded p-3 flex items-center gap-3">
                            <Target className="h-4 w-4 text-purple-400" />
                            <div className="flex-1 grid grid-cols-3 gap-2">
                                <code className="bg-black px-2 py-1 rounded text-[10px] text-gray-400">{rule.attribute}</code>
                                <span className="text-[10px] text-center font-bold text-gray-600 uppercase pt-1">{rule.operator}</span>
                                <div className="flex flex-wrap gap-1">
                                    {rule.values.map((v, vidx) => (
                                        <Badge key={vidx} variant="outline" className="text-[9px] h-5 border-gray-800 bg-black">{v}</Badge>
                                    ))}
                                    {rule.values.length === 0 && <span className="text-gray-700 text-[10px] pt-1 italic">No values</span>}
                                </div>
                            </div>
                            <Button variant="ghost" size="icon" className="h-6 w-6 text-gray-600 hover:text-red-400" onClick={() => removeRule(idx)}>
                                <Trash2 className="h-3 w-3" />
                            </Button>
                        </div>
                    ))}
                    {rules.length === 0 && (
                        <div className="text-center py-6 border border-dashed border-gray-900 rounded bg-gray-950/20">
                            <p className="text-gray-600 text-xs">No targeting rules. Flag applies to all traffic per percentage.</p>
                        </div>
                    )}
                </div>
            </div>

            <div className="bg-blue-950/10 border border-blue-900/30 rounded p-4 flex gap-3">
                <AlertCircle className="h-5 w-5 text-blue-500 mt-0.5" />
                <p className="text-[11px] text-blue-400 leading-relaxed italic">
                    Targeting rules are evaluated before percentage rollouts. A user must match ALL rules to be eligible for the percentage bucket.
                </p>
            </div>
        </div>
    );
};

export default TargetingRulesEditor;
