import React from 'react';
import { Responsive, WidthProvider } from 'react-grid-layout';
import DonationRouter from '../widgets/Impact/DonationRouter';
import ESGScores from '../widgets/Impact/ESGScores';
import CarbonScatter from '../widgets/Impact/CarbonScatter';
import { Leaf, Heart, ShieldCheck } from 'lucide-react';

const ResponsiveGridLayout = WidthProvider(Responsive);

const ImpactDashboard = () => {
    const layout = [
        { i: 'donation', x: 0, y: 0, w: 4, h: 6 },
        { i: 'esg', x: 4, y: 0, w: 8, h: 4 },
        { i: 'carbon', x: 4, y: 4, w: 8, h: 4 }
    ];

    return (
        <div className="impact-dashboard-page p-6 h-full overflow-y-auto bg-[#0a0a0a] text-white font-sans">
            <header className="mb-6 flex justify-between items-center">
                <div>
                    <h1 className="text-3xl font-black tracking-tighter uppercase flex items-center gap-3">
                        <Leaf className="text-green-500" /> Philanthropy & Impact
                    </h1>
                    <p className="text-zinc-500 mt-1 text-sm font-medium">Excess Alpha Routing & ESG Telemetry</p>
                </div>
                <div className="flex gap-2">
                     <span className="bg-green-500/10 text-green-400 px-3 py-1 rounded-full text-xs border border-green-500/20 flex items-center gap-2">
                        <Heart size={12} fill="currentColor" /> Active Donor
                     </span>
                     <span className="bg-blue-500/10 text-blue-400 px-3 py-1 rounded-full text-xs border border-blue-500/20 flex items-center gap-2">
                        <ShieldCheck size={12} /> ESG Grade A-
                     </span>
                </div>
            </header>
            
            <ResponsiveGridLayout
                className="layout"
                layouts={{ lg: layout }}
                breakpoints={{ lg: 1200, md: 996, sm: 768, xs: 480, xxs: 0 }}
                cols={{ lg: 12, md: 10, sm: 6, xs: 4, xxs: 2 }}
                rowHeight={100}
                isDraggable={true}
                isResizable={true}
                margin={[16, 16]}
            >
                <div key="donation" className="bg-[#111] border border-white/10 rounded-xl overflow-hidden shadow-2xl">
                    <DonationRouter />
                </div>
                <div key="esg" className="bg-[#111] border border-white/10 rounded-xl overflow-hidden shadow-2xl">
                    <ESGScores />
                </div>
                <div key="carbon" className="bg-[#111] border border-white/10 rounded-xl overflow-hidden shadow-2xl">
                    <CarbonScatter />
                </div>
            </ResponsiveGridLayout>
        </div>
    );
};

export default ImpactDashboard;
