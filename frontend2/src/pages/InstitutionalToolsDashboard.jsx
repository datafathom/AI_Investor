import React, { useState, useEffect } from 'react';
import { Network, Activity, Users, Shield, Layout, Settings, PlusCircle } from 'lucide-react';
import { Responsive, WidthProvider } from 'react-grid-layout';
import { PortfolioTreeMap, SentimentHeatmap, StatCard } from '../components/DataViz';
import 'react-grid-layout/css/styles.css';
import 'react-resizable/css/styles.css';

// Institutional Components
import AdvisorOnboardingWizard from '../components/Institutional/AdvisorOnboardingWizard';
import useInstitutionalStore from '../stores/institutionalStore';

// Institutional Widgets
import RevenuePulse from '../components/Institutional/RevenuePulse';
import ClientRetentionAI from '../widgets/Institutional/ClientRetentionAI';
import DocSignaturePulse from '../widgets/Institutional/DocSignaturePulse';
import AssetAllocationWheel from '../widgets/Institutional/AssetAllocationWheel';
import AdvisorCommissionTracker from '../widgets/Institutional/AdvisorCommissionTracker';
import ClientHealthCompass from '../components/Institutional/ClientHealthCompass';

const ResponsiveGridLayout = WidthProvider(Responsive);

const InstitutionalToolsDashboard = () => {
    const { clients, analytics, fetchClients, fetchClientAnalytics, onboardingStep, setOnboardingStep } = useInstitutionalStore();
    const [selectedClientId, setSelectedClientId] = useState(null);
    const [showOnboarding, setShowOnboarding] = useState(false);

    useEffect(() => {
        fetchClients();
    }, [fetchClients]);

    useEffect(() => {
        if (clients.length > 0 && !selectedClientId) {
            setSelectedClientId(clients[0].client_id);
        }
    }, [clients, selectedClientId]);

    useEffect(() => {
        if (selectedClientId) {
            fetchClientAnalytics(selectedClientId);
        }
    }, [selectedClientId, fetchClientAnalytics]);

    const DEFAULT_LAYOUT = {
        lg: [
            { i: 'header', x: 0, y: 0, w: 12, h: 3 },
            { i: 'clients', x: 0, y: 3, w: 3, h: 8 },
            { i: 'fee-forecast', x: 3, y: 3, w: 3, h: 8 },
            { i: 'retention-ai', x: 6, y: 3, w: 3, h: 8 },
            { i: 'risk-gauge', x: 9, y: 3, w: 3, h: 8 },
            { i: 'allocation', x: 0, y: 11, w: 4, h: 8 },
            { i: 'commission', x: 4, y: 11, w: 4, h: 8 },
            { i: 'doc-pulse', x: 8, y: 11, w: 4, h: 8 },
        ]
    };

    const activeAnalytics = selectedClientId ? analytics[selectedClientId] : null;
    const activeClient = clients.find(c => c.client_id === selectedClientId);

    if (showOnboarding) {
        return (
            <div className="min-h-screen p-12 bg-slate-950 flex flex-col items-center justify-center">
                <button 
                    onClick={() => setShowOnboarding(false)}
                    className="absolute top-8 left-8 text-slate-500 hover:text-white font-bold flex items-center gap-2"
                >
                    <Layout size={16} /> BACK TO DASHBOARD
                </button>
                <AdvisorOnboardingWizard />
            </div>
        );
    }

    return (
        <div className="institutional-dashboard min-h-screen p-6 bg-slate-950 font-sans text-slate-200">
            <ResponsiveGridLayout
                className="layout"
                layouts={DEFAULT_LAYOUT}
                breakpoints={{ lg: 1200, md: 996, sm: 768, xs: 480, xxs: 0 }}
                cols={{ lg: 12, md: 10, sm: 6, xs: 4, xxs: 2 }}
                rowHeight={60}
                draggableHandle=".drag-handle"
            >
                {/* Header Section */}
                <div key="header" className="glass-premium p-6 rounded-2xl flex items-center justify-between border border-white/5 drag-handle cursor-move overflow-hidden relative">
                    <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-accent via-primary to-success opacity-50" />
                    <div className="flex items-center gap-6">
                        <div className="w-16 h-16 rounded-2xl bg-primary/20 flex items-center justify-center border border-primary/30 shadow-[0_0_20px_rgba(var(--primary-h),0.3)]">
                            <Shield size={32} className="text-primary" />
                        </div>
                        <div>
                            <h1 className="text-3xl font-black tracking-tighter text-white">
                                INSTITUTIONAL <span className="text-primary-light">ORCHESTRATOR</span>
                            </h1>
                            <div className="flex items-center gap-4 mt-1">
                                <span className="flex items-center gap-1 text-xs font-bold text-success">
                                    <div className="w-2 h-2 rounded-full bg-success animate-pulse" /> SYSTEM NOMINAL
                                </span>
                                <span className="text-xs text-slate-500 font-mono uppercase tracking-widest">Ver: 2.5.0-ADVISOR</span>
                            </div>
                        </div>
                    </div>
                    <div className="flex gap-4">
                        <StatCard 
                            label="Portfolio AUM" 
                            value={`$${(clients.reduce((sum, c) => sum + c.aum, 0)/1000000).toFixed(0)}M`} 
                            trend="+4.2%" 
                            trendUp={true} 
                            small 
                        />
                        <button 
                            onClick={() => setShowOnboarding(true)}
                            className="bg-primary hover:bg-primary-light text-white px-4 py-2 rounded-xl font-bold flex items-center gap-2 transition-all shadow-[0_0_15px_rgba(var(--primary-h),0.3)]"
                        >
                            <PlusCircle size={18} /> NEW CLIENT
                        </button>
                    </div>
                </div>

                {/* Clients Panel */}
                <div key="clients" className="glass-premium p-4 rounded-2xl border border-white/5 overflow-hidden flex flex-col">
                    <h3 className="text-sm font-bold mb-4 flex items-center gap-2 text-primary-light uppercase tracking-widest">
                        <Users size={16} /> Client Roster
                    </h3>
                    <div className="flex-1 overflow-y-auto space-y-2 pr-2">
                        {clients.map(client => (
                            <div 
                                key={client.client_id} 
                                onClick={() => setSelectedClientId(client.client_id)}
                                className={`p-4 rounded-xl border transition-all cursor-pointer ${
                                    selectedClientId === client.client_id 
                                    ? 'bg-primary/10 border-primary/40' 
                                    : 'bg-white/5 border-white/5 hover:bg-white/10'
                                }`}
                            >
                                <div className="flex justify-between items-start mb-1">
                                    <span className="font-bold text-white text-sm">{client.client_name}</span>
                                    <span className={`text-[8px] px-1.5 py-0.5 rounded-full font-bold uppercase ${
                                        client.risk_level === 'Low' ? 'bg-success/20 text-success' :
                                        client.risk_level === 'Moderate' ? 'bg-primary/20 text-primary' :
                                        'bg-danger/20 text-danger'
                                    }`}>
                                        {client.risk_level}
                                    </span>
                                </div>
                                <div className="flex justify-between items-end">
                                    <span className="text-lg font-mono text-slate-300 font-black">${(client.aum/1000000).toFixed(1)}M</span>
                                    <span className="text-[10px] text-slate-500">{client.kyc_status}</span>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>

                {/* Analytical Widgets */}
                <div key="fee-forecast">
                    <RevenuePulse clientId={selectedClientId} />
                </div>

                <div key="retention-ai">
                    <ClientRetentionAI score={activeClient?.retention_score} />
                </div>

                <div key="risk-gauge">
                    <ClientHealthCompass clientId={selectedClientId} />
                </div>

                {/* Lower Row Widgets */}
                <div key="allocation">
                    <AssetAllocationWheel />
                </div>

                <div key="commission">
                    <AdvisorCommissionTracker />
                </div>

                <div key="doc-pulse">
                    <DocSignaturePulse />
                </div>

            </ResponsiveGridLayout>
        </div>
    );
};

export default InstitutionalToolsDashboard;
