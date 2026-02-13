import React, { useState, useEffect } from 'react';
import { externalDataService } from '../../services/externalDataService';
import { toast } from 'sonner';
import { Server, Activity, AlertTriangle, Shield, RefreshCw, Power } from 'lucide-react';

const ExternalDataSources = () => {
  const [sources, setSources] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  const loadData = async () => {
    try {
      setLoading(true);
      const [src, st] = await Promise.all([
        externalDataService.getSources(),
        externalDataService.getStats()
      ]);
      setSources(src);
      setStats(st);
    } catch (error) {
      console.error(error);
      toast.error("Failed to load data sources");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
    const interval = setInterval(loadData, 15000); // Poll every 15s
    return () => clearInterval(interval);
  }, []);

  const handleToggle = async (id) => {
    try {
      await externalDataService.toggleSource(id);
      toast.success("Source status updated");
      loadData();
    } catch (e) {
        toast.error("Failed to toggle source");
    }
  };

  return (
    <div className="p-8 h-full overflow-y-auto bg-slate-950 text-slate-200">
        <div className="flex justify-between items-center mb-8">
            <div>
                <h1 className="text-3xl font-bold text-white flex items-center gap-3">
                    <Server className="text-emerald-500" /> External Data Sources
                </h1>
                <p className="text-slate-400 mt-2">Monitor data quotas, health, and connectivity.</p>
            </div>
             <button 
                onClick={loadData}
                className="p-2 bg-slate-800 hover:bg-slate-700 rounded-md border border-slate-700 text-slate-400 hover:text-white transition-colors"
            >
                <RefreshCw size={20} className={loading ? "animate-spin" : ""} />
            </button>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
            <div className="bg-slate-900 border border-slate-800 p-4 rounded-lg">
                <div className="text-slate-400 text-xs uppercase mb-1">Total Sources</div>
                <div className="text-2xl font-bold text-white">{stats?.total_sources || 0}</div>
            </div>
            <div className="bg-slate-900 border border-slate-800 p-4 rounded-lg">
                <div className="text-slate-400 text-xs uppercase mb-1">Active</div>
                <div className="text-2xl font-bold text-emerald-400">{stats?.active_sources || 0}</div>
            </div>
            <div className="bg-slate-900 border border-slate-800 p-4 rounded-lg">
                <div className="text-slate-400 text-xs uppercase mb-1">Errors</div>
                <div className="text-2xl font-bold text-red-400">{stats?.error_sources || 0}</div>
            </div>
            <div className="bg-slate-900 border border-slate-800 p-4 rounded-lg">
                <div className="text-slate-400 text-xs uppercase mb-1">Overall Health</div>
                <div className="text-2xl font-bold text-blue-400">{stats?.overall_health}%</div>
            </div>
        </div>

        {/* Sources List */}
        <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
            {sources.map(source => (
                <div key={source.id} className="bg-slate-900 border border-slate-800 rounded-xl p-6 relative overflow-hidden group hover:border-slate-700 transition-all">
                    {/* Status Indicator */}
                    <div className={`absolute top-0 right-0 w-24 h-24 bg-gradient-to-br from-transparent to-white/5 rounded-bl-full pointer-events-none transition-all ${
                         source.status === 'active' ? 'to-emerald-500/10' : 
                         source.status === 'error' ? 'to-red-500/10' : 
                         'to-slate-500/10'
                    }`} />

                    <div className="flex justify-between items-start mb-4 relative z-10">
                        <div>
                            <div className="flex items-center gap-2 mb-1">
                                <h3 className="font-semibold text-lg text-white">{source.name}</h3>
                            </div>
                            <span className="text-xs bg-slate-800 px-2 py-0.5 rounded text-slate-400">{source.category}</span>
                        </div>
                        <button 
                            onClick={() => handleToggle(source.id)}
                            className={`p-2 rounded-full transition-colors ${
                                source.status === 'active' ? 'bg-emerald-500/20 text-emerald-400 hover:bg-emerald-500/30' : 
                                'bg-slate-800 text-slate-400 hover:bg-slate-700'
                            }`}
                            title="Toggle Status"
                        >
                            <Power size={18} />
                        </button>
                    </div>

                    <div className="space-y-4 relative z-10">
                        <div>
                            <div className="flex justify-between text-xs text-slate-400 mb-1">
                                <span>Quota Usage</span>
                                <span>{source.quota_used.toLocaleString()} / {source.quota_limit > 0 ? source.quota_limit.toLocaleString() : '∞'}</span>
                            </div>
                            <div className="h-2 bg-slate-800 rounded-full overflow-hidden">
                                <div 
                                    className={`h-full rounded-full transition-all duration-500 ${
                                        source.usage_pct > 90 ? 'bg-red-500' :
                                        source.usage_pct > 75 ? 'bg-amber-500' :
                                        'bg-blue-500'
                                    }`}
                                    style={{ width: `${source.quota_limit > 0 ? source.usage_pct : 0}%` }}
                                />
                            </div>
                        </div>

                        <div className="flex items-center justify-between pt-4 border-t border-slate-800/50">
                            <div className="flex items-center gap-2 text-xs text-slate-500">
                                <Activity size={14} />
                                <span>Updated: {new Date(source.last_updated).toLocaleTimeString()}</span>
                            </div>
                            {source.status === 'error' && (
                                <div className="flex items-center gap-1 text-xs text-red-400">
                                    <AlertTriangle size={14} /> Connection Error
                                </div>
                            )}
                        </div>
                    </div>
                </div>
            ))}
        </div>
    </div>
  );
};

export default ExternalDataSources;
