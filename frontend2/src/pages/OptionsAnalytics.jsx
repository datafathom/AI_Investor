
import React from 'react';
import { Target, BarChart3 } from 'lucide-react';

const OptionsAnalytics = () => {
    return (
        <div className="options-analytics-page glass p-8">
            <div className="header flex items-center gap-4 mb-8">
                <Target size={32} className="text-burgundy" />
                <h1 className="text-3xl font-bold">Options Strategy Analytics</h1>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                <div className="card glass p-6 min-h-[400px] flex items-center justify-center border-dashed border-2 border-gray-400">
                    <div className="text-center opacity-50">
                        <BarChart3 size={48} className="mx-auto mb-4" />
                        <p>Greeks Visualizer (Phase 46)</p>
                    </div>
                </div>
                <div className="card glass p-6 min-h-[400px] flex items-center justify-center border-dashed border-2 border-gray-400">
                    <div className="text-center opacity-50">
                        <Target size={48} className="mx-auto mb-4" />
                        <p>Strategy Modeler (Phase 46)</p>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default OptionsAnalytics;
