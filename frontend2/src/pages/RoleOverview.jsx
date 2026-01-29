import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { getOverviewForPath } from '../data/overviewContent';
import { 
  ChevronRight, 
  Layout, 
  Cpu, 
  Search, 
  PieChart, 
  Shield, 
  Activity, 
  HardDrive, 
  Globe 
} from 'lucide-react';

import RoleGlimpseCard from '../components/Navigation/RoleGlimpseCard';

const ICON_MAP = {
  Layout,
  Cpu,
  Search,
  PieChart,
  Shield,
  Activity,
  HardDrive,
  Globe
};

const RoleOverview = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const content = getOverviewForPath(location.pathname);

  if (!content) {
    return (
      <div className="flex items-center justify-center h-full text-zinc-500">
        <div className="text-center">
            <h2 className="text-2xl font-bold mb-2">Namespace Not Found</h2>
            <p>We couldn't find a mapping for this breadcrumb segment.</p>
        </div>
      </div>
    );
  }

  const IconComponent = ICON_MAP[content.icon] || Layout;

  return (
    <div className="role-overview-dashboard glass-panel p-8 animate-fade-in">
      <header className="mb-10">
        <div className="flex items-center justify-between mb-6">
            <div className="flex items-center gap-4">
                <div className="p-3 bg-cyan-500/10 rounded-2xl text-cyan-400 border border-cyan-500/20 shadow-[0_0_15px_rgba(6,182,212,0.1)]">
                    <IconComponent size={28} />
                </div>
                <div>
                    <h1 className="text-4xl font-black text-white tracking-tight uppercase">
                        {content.title}
                    </h1>
                    <p className="text-zinc-500 font-medium">Namespace Controller Ready</p>
                </div>
            </div>
            <div className="flex gap-2">
                <span className="px-3 py-1 bg-zinc-900 border border-zinc-800 rounded-lg text-[10px] font-bold text-zinc-500 uppercase tracking-widest">
                    V3.2.0-STABLE
                </span>
                <span className="px-3 py-1 bg-cyan-500/10 border border-cyan-500/20 rounded-lg text-[10px] font-bold text-cyan-400 uppercase tracking-widest">
                    Role Auth: Verified
                </span>
            </div>
        </div>
        <p className="text-lg text-zinc-400 max-w-3xl leading-relaxed">
          {content.description}
        </p>
      </header>

      {/* Hero Stats Section */}
      <section className="mb-12">
        <h4 className="text-zinc-600 uppercase text-[10px] font-black tracking-[0.2em] mb-4">Live Namespace Glimpses</h4>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {content.glimpses.map((g, idx) => (
                <RoleGlimpseCard key={idx} {...g} />
            ))}
        </div>
      </section>

      {/* Capabilities Section */}
      <section>
        <h4 className="text-zinc-600 uppercase text-[10px] font-black tracking-[0.2em] mb-4">Operational Capabilities</h4>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 pb-20">
            {content.children.map((child) => (
            <div 
                key={child.path}
                onClick={() => navigate(child.path)}
                className="group relative bg-zinc-900/40 border border-zinc-800 p-6 rounded-2xl cursor-pointer hover:border-cyan-500/40 hover:bg-cyan-500/5 transition-all duration-300 overflow-hidden"
            >
                <div className="flex justify-between items-start mb-4">
                <h3 className="text-lg font-bold text-white group-hover:text-cyan-400 transition-colors uppercase tracking-tight">
                    {child.label}
                </h3>
                <ChevronRight size={18} className="text-zinc-700 group-hover:text-cyan-400 transform group-hover:translate-x-1 transition-all" />
                </div>
                <p className="text-zinc-500 leading-relaxed text-sm">
                {child.description}
                </p>
                
                {/* Visual accent */}
                <div className="absolute bottom-0 left-0 h-1 w-0 bg-cyan-500 transition-all duration-500 group-hover:w-full opacity-50" />
            </div>
            ))}
        </div>
      </section>

      <style>{`
        .role-overview-dashboard {
          background: radial-gradient(circle at 10% 10%, rgba(6, 182, 212, 0.08), transparent 600px),
                      radial-gradient(circle at 90% 90%, rgba(99, 102, 241, 0.05), transparent 600px);
        }
        .role-overview-dashboard::-webkit-scrollbar {
          width: 6px;
        }
        .role-overview-dashboard::-webkit-scrollbar-track {
          background: transparent;
        }
        .role-overview-dashboard::-webkit-scrollbar-thumb {
          background: rgba(255, 255, 255, 0.1);
          border-radius: 10px;
        }
        .role-overview-dashboard::-webkit-scrollbar-thumb:hover {
          background: rgba(6, 182, 212, 0.2);
        }
      `}</style>
    </div>
  );
};

export default RoleOverview;
