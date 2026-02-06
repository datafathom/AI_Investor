import React, { useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
import { DEPT_REGISTRY, PARENT_ROLES } from '../config/departmentRegistry';
import { getIcon } from '../config/iconRegistry';
import { Shield, Target, Zap, Cpu, Layout, BarChart, Bell, Scale, Search, Users, Crosshair, Atom, Home } from 'lucide-react';
import './MissionsOverview.css';

const ROLE_ICONS = {
    'Orchestrator': Cpu,
    'Architect': Layout,
    'Data Scientist': Zap,
    'Strategist': BarChart,
    'Trader': Target,
    'Guardian': Shield,
    'Lawyer': Scale,
    'Auditor': Search,
    'Envoy': Users,
    'Hunter': Crosshair,
    'Sentry': Shield,
    'Physicist': Atom,
    'Steward': Home
};

const MissionsOverview = () => {
    const navigate = useNavigate();

    const roleGroups = useMemo(() => {
        return Object.values(PARENT_ROLES).map(role => {
            const departments = Object.values(DEPT_REGISTRY).filter(d => d.parentRole === role);
            return {
                name: role,
                icon: ROLE_ICONS[role] || Target,
                departments
            };
        });
    }, []);

    return (
        <div className="missions-overview-container">
            <header className="missions-header">
                <h1 className="text-4xl font-black tracking-tighter text-white uppercase italic">
                    Strategic <span className="text-cyan-400">Missions</span>
                </h1>
                <p className="text-slate-500 font-mono text-sm mt-2">
                    INTEGRATED AGENTIC HIERARCHY /// DIRECTIVE OVERVIEW
                </p>
            </header>

            <div className="missions-grid">
                {roleGroups.map((group, idx) => {
                    const Icon = group.icon;
                    return (
                        <div key={idx} className="mission-card active">
                            <div className="mission-title">
                                <div className="p-2 bg-cyan-500/10 rounded-lg">
                                    <Icon size={24} className="text-cyan-400" />
                                </div>
                                <h2>{group.name}</h2>
                                <span className="mission-status font-mono">NOMINAL</span>
                            </div>

                            <div className="child-missions-list">
                                {group.departments.map(dept => {
                                    const DeptIcon = getIcon(dept.icon);
                                    return (
                                        <div 
                                            key={dept.id} 
                                            className="child-mission-item group"
                                        >
                                            <div className="flex items-center gap-3 w-full cursor-pointer" onClick={() => navigate(dept.route)}>
                                                <div className="child-mission-icon">
                                                    <DeptIcon size={18} style={{ color: dept.color }} />
                                                </div>
                                                <div className="child-mission-info">
                                                    <div className="child-mission-name">{dept.shortName}</div>
                                                    <div className="child-mission-desc">DEPT_{dept.id} // {dept.parentRole}</div>
                                                </div>
                                            </div>

                                            {/* Sub-Modules Workstations */}
                                            {dept.subModules && dept.subModules.length > 0 && (
                                                <div className="workstation-sublinks">
                                                    {dept.subModules.map((sub, sIdx) => (
                                                        <button 
                                                            key={sIdx}
                                                            className="sub-workstation-btn"
                                                            onClick={(e) => {
                                                                e.stopPropagation();
                                                                navigate(sub.path);
                                                            }}
                                                        >
                                                            {sub.label}
                                                        </button>
                                                    ))}
                                                </div>
                                            )}
                                        </div>
                                    );
                                })}
                            </div>
                        </div>
                    );
                })}
            </div>

            <footer className="mission-footer">
                <p>ROLES_HMT_V1.0 // SYSTEM_OBJECTIVE: MAXIMIZE_ROL</p>
            </footer>
        </div>
    );
};

export default MissionsOverview;
