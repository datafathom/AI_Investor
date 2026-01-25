
import React, { useState, useEffect } from 'react';
import { authService } from '../utils/authService';
import './TenantDashboard.css';
import { Users, Shield, ArrowRightLeft, Plus } from 'lucide-react';

import { Responsive, WidthProvider } from 'react-grid-layout';

const ResponsiveGridLayout = WidthProvider(Responsive);

const TenantDashboard = () => {
    const DEFAULT_LAYOUT = {
        lg: [
            { i: 'tenants', x: 0, y: 0, w: 12, h: 8 }
        ]
    };

    const [tenants, setTenants] = useState([
        { id: 'default', name: 'Primary Portfolio', role: 'admin' },
        { id: 'family_alpha', name: 'Alpha Family Office', role: 'trader' }
    ]);
    const [activeTenant, setActiveTenant] = useState(authService.getTenantId() || 'default');

    const switchTenant = (tenantId) => {
        authService.setTenantId(tenantId);
        setActiveTenant(tenantId);
        window.location.reload(); // Reload to refresh context
    };

    return (
        <div className="full-bleed-page tenant-dashboard">
            <header className="tenant-header mb-8">
                <div className="flex items-center gap-4">
                    <div className="p-3 bg-zinc-800 rounded-xl border border-zinc-700">
                        <Users size={32} className="text-zinc-100" />
                    </div>
                    <div>
                        <h1 className="text-3xl font-bold">Family Office Management</h1>
                        <p className="text-zinc-500">Switch between family accounts and manage access.</p>
                    </div>
                </div>
            </header>

            <div className="scrollable-content-wrapper">
                <ResponsiveGridLayout
                    className="layout"
                    layouts={DEFAULT_LAYOUT}
                    breakpoints={{ lg: 1200, md: 996, sm: 768, xs: 480, xxs: 0 }}
                    cols={{ lg: 12, md: 10, sm: 6, xs: 4, xxs: 2 }}
                    rowHeight={80}
                    isDraggable={true}
                    isResizable={true}
                    draggableHandle=".tenant-card"
                    margin={[16, 16]}
                >
                    <div key="tenants" className="flex flex-wrap gap-6">
                        {tenants.map(tenant => (
                            <div
                                key={tenant.id}
                                className={`tenant-card glass-panel p-6 cursor-pointer transition-all hover:scale-105 ${activeTenant === tenant.id ? 'active ring-2 ring-blue-500 bg-blue-900/10' : 'bg-white/5 hover:bg-white/10'}`}
                                onClick={() => switchTenant(tenant.id)}
                                style={{ width: '300px', borderRadius: '16px' }}
                            >
                                <div className="tenant-info flex justify-between items-start mb-4">
                                    <div>
                                        <h3 className="text-xl font-bold text-white">{tenant.name}</h3>
                                        <span className="role-tag text-[10px] bg-zinc-800 px-2 py-1 rounded text-zinc-400 uppercase font-bold tracking-widest mt-2 inline-block border border-zinc-700">
                                            {tenant.role.toUpperCase()}
                                        </span>
                                    </div>
                                    {activeTenant === tenant.id ? (
                                        <Shield className="text-blue-400" size={24} />
                                    ) : (
                                        <ArrowRightLeft className="text-zinc-600" size={20} />
                                    )}
                                </div>
                                <div className="mt-4 pt-4 border-t border-white/10">
                                    <p className="text-xs text-zinc-500">Switch to this account to view its portfolio and analysis.</p>
                                </div>
                            </div>
                        ))}

                        <div className="tenant-card add-new glass-panel p-6 flex flex-col items-center justify-center border-dashed border-2 border-zinc-800 hover:border-zinc-700 cursor-pointer transition-all bg-transparent" style={{ width: '300px', borderRadius: '16px' }}>
                            <Plus className="text-zinc-500 mb-2" size={32} />
                            <h3 className="text-zinc-500 font-bold">Invite New Member</h3>
                        </div>
                    </div>
                </ResponsiveGridLayout>
                
                {/* Bottom Buffer */}
                <div className="scroll-buffer-100" />
            </div>
        </div>
    );
};

export default TenantDashboard;
