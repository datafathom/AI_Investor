
import React, { useState, useEffect } from 'react';
import { authService } from '../utils/authService';
import './TenantDashboard.css';
import { Users, Shield, ArrowRightLeft, Plus } from 'lucide-react';

const TenantDashboard = () => {
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
        <div className="tenant-dashboard glass">
            <header className="tenant-header">
                <Users className="icon-header" />
                <h1>Family Office Management</h1>
                <p>Switch between family accounts and manage access.</p>
            </header>

            <div className="tenant-grid">
                {tenants.map(tenant => (
                    <div
                        key={tenant.id}
                        className={`tenant-card ${activeTenant === tenant.id ? 'active' : ''}`}
                        onClick={() => switchTenant(tenant.id)}
                    >
                        <div className="tenant-info">
                            <h3>{tenant.name}</h3>
                            <span className="role-tag">{tenant.role.toUpperCase()}</span>
                        </div>
                        {activeTenant === tenant.id ? (
                            <Shield className="status-icon active" />
                        ) : (
                            <ArrowRightLeft className="status-icon" />
                        )}
                    </div>
                ))}

                <div className="tenant-card add-new">
                    <Plus className="icon-add" />
                    <h3>Invite New Member</h3>
                </div>
            </div>
        </div>
    );
};

export default TenantDashboard;
