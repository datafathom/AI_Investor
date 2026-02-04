import React, { useEffect } from 'react';
import { StorageService } from '../utils/storageService';
import { Responsive, WidthProvider } from 'react-grid-layout';
import DeadMansSwitch from '../widgets/Estate/DeadMansSwitch';
import BeneficiaryMap from '../widgets/Estate/BeneficiaryMap';
import EntityGraph from '../widgets/Estate/EntityGraph';
import '../widgets/Estate/DeadMansSwitch.css';

// New UI/UX Components
import { StatCard, Badge, ProgressBar } from '../components/DataViz';
import { GlassCard } from '../components/Common';

// Zustand Store - Replaces direct service calls
import useEstateStore from '../stores/estateStore';

const ResponsiveGridLayout = WidthProvider(Responsive);

const EstateDashboard = () => {
    const { 
        heartbeatStatus, 
        beneficiaries, 
        entityGraph,
        isLoading, 
        error,
        fetchEstateData 
    } = useEstateStore();

    useEffect(() => {
        fetchEstateData();
    }, [fetchEstateData]);

    // Derive stats from store state
    const estateStats = [
        { 
            label: 'Total Estate Value', 
            value: isLoading ? '...' : (heartbeatStatus?.total_value || 4850000), 
            prefix: '$', 
            status: 'positive' 
        },
        { 
            label: 'Beneficiaries', 
            value: isLoading ? 0 : (beneficiaries?.length || 0), 
            status: 'neutral' 
        },
        { 
            label: 'Trusts Active', 
            value: isLoading ? 0 : (entityGraph?.nodes?.filter(n => n.type === 'TRUST')?.length || 0), 
            status: 'positive' 
        },
        { 
            label: 'Next Check-In', 
            value: isLoading ? '...' : `${heartbeatStatus?.daysUntilTrigger || 30} days`, 
            status: heartbeatStatus?.daysUntilTrigger < 7 ? 'warning' : 'neutral' 
        }
    ];

    const layout = [
        { i: 'stats', x: 0, y: 0, w: 12, h: 2 },
        { i: 'switch', x: 0, y: 2, w: 4, h: 4 },
        { i: 'entity', x: 4, y: 2, w: 8, h: 4 },
        { i: 'beneficiary', x: 0, y: 6, w: 12, h: 4 }
    ];


    return (
        <div className="estate-dashboard-page p-6 h-full overflow-y-auto bg-slate-950">
            <header className="mb-6">
                <div className="flex items-center gap-4">
                    <h1 className="text-3xl font-black text-white tracking-tight uppercase">
                        Estate Planning
                    </h1>
                    <Badge count={heartbeatStatus?.isAlive ? 'Protected' : 'Expired'} variant={heartbeatStatus?.isAlive ? 'success' : 'error'} pulse />
                </div>
                <p className="text-zinc-500 mt-1">Inheritance protocol, beneficiary mapping, and entity structure.</p>
            </header>
            
            <ResponsiveGridLayout
                className="layout"
                layouts={{ lg: layout }}
                breakpoints={{ lg: 1200, md: 996, sm: 768, xs: 480, xxs: 0 }}
                cols={{ lg: 12, md: 10, sm: 6, xs: 4, xxs: 2 }}
                rowHeight={80}
                isDraggable={true}
                isResizable={true}
            >
                <div key="stats" style={{ display: 'flex', gap: '16px' }}>
                    {estateStats.map((stat, idx) => (
                        <div key={idx} style={{ flex: 1 }}>
                            <StatCard {...stat} formatValue={v => typeof v === 'number' && v > 100 ? v.toLocaleString() : v} />
                        </div>
                    ))}
                </div>

                <div key="switch" style={{ borderRadius: '12px', overflow: 'hidden' }}>
                    <GlassCard variant="elevated" status="success" hoverable={false} className="h-full">
                        <div className="flex justify-between items-center mb-3">
                            <h3 className="font-bold text-white">Dead Man's Switch</h3>
                            <Badge count={heartbeatStatus?.isAlive ? 'Armed' : 'Expired'} variant={heartbeatStatus?.isAlive ? 'success' : 'error'} />
                        </div>
                        <DeadMansSwitch />
                    </GlassCard>
                </div>
                <div key="entity" style={{ borderRadius: '12px', overflow: 'hidden' }}>
                    <GlassCard variant="elevated" hoverable={false} className="h-full">
                        <h3 className="font-bold text-white mb-4">Entity Structure</h3>
                        <EntityGraph />
                    </GlassCard>
                </div>
                <div key="beneficiary" style={{ borderRadius: '12px', overflow: 'hidden' }}>
                    <GlassCard variant="default" hoverable={false} className="h-full">
                        <div className="flex justify-between items-center mb-3">
                            <h3 className="font-bold text-white">Beneficiary Map</h3>
                            <Badge count={`${beneficiaries?.length || 0} Verified`} variant="info" />
                        </div>
                        <BeneficiaryMap />
                    </GlassCard>
                </div>
            </ResponsiveGridLayout>
        </div>
    );
};

export default EstateDashboard;
