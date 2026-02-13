import React, { useState, useEffect } from 'react';
import { ingestionService } from '../../services/ingestionService';
import { toast } from 'sonner';
import { ShieldCheck, AlertOctagon, CheckCircle, Clock, RefreshCw, Activity, ArrowUpRight } from 'lucide-react';

const QualityScoreWidget = ({ score, label }) => (
    <div className="relative w-32 h-32 flex items-center justify-center">
        <svg className="w-full h-full transform -rotate-90">
            <circle
                cx="64"
                cy="64"
                r="56"
                stroke="currentColor"
                strokeWidth="8"
                fill="transparent"
                className="text-slate-800"
            />
            <circle
                cx="64"
                cy="64"
                r="56"
                stroke="currentColor"
                strokeWidth="8"
                fill="transparent"
                strokeDasharray={351}
                strokeDashoffset={351 - (351 * score) / 100}
                className={score > 90 ? "text-emerald-500" : score > 70 ? "text-amber-500" : "text-red-500"}
            />
        </svg>
        <div className="absolute flex flex-col items-center">
            <span className="text-2xl font-bold text-white">{score}</span>
            <span className="text-[10px] text-slate-400 uppercase tracking-wider">{label}</span>
        </div>
    </div>
);

const DataQualityDashboard = () => {
  const [summary, setSummary] = useState(null);
  const [issues, setIssues] = useState([]);
  const [loading, setLoading] = useState(true);

  const loadData = async () => {
    try {
      setLoading(true);
      const [sum, iss] = await Promise.all([
        ingestionService.getQualitySummary(),
        ingestionService.listQualityIssues()
      ]);
      setSummary(sum);
      setIssues(iss);
    } catch (error) {
      toast.error("Failed to load quality data");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleResolve = async (id) => {
      try {
          await ingestionService.resolveIssue(id);
          toast.success("Issue resolved");
          loadData();
      } catch (e) {
          toast.error("Failed to resolve issue");
      }
  };

  return (
    <div className="p-8 h-full overflow-y-auto bg-slate-950 text-slate-200">
        <div className="flex justify-between items-center mb-8">
            <div>
                <h1 className="text-3xl font-bold text-white flex items-center gap-3">
                    <ShieldCheck className="text-emerald-500" /> Data Quality Dashboard
                </h1>
                <p className="text-slate-400 mt-2">Monitor data integrity, freshness, and accuracy across all pipelines.</p>
            </div>
             <button 
                onClick={loadData}
                className="p-2 bg-slate-800 hover:bg-slate-700 rounded-md border border-slate-700 text-slate-400 hover:text-white transition-colors"
            >
                <RefreshCw size={20} className={loading ? "animate-spin" : ""} />
            </button>
        </div>

        {/* Score Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
            <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 flex items-center justify-between">
                <div>
                     <div className="text-slate-400 text-xs uppercase mb-1">Overall Score</div>
                     <div className="text-3xl font-bold text-white">{summary?.score || 0}/100</div>
                </div>
               <QualityScoreWidget score={summary?.score || 0} label="Quality" />
            </div>

            <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                <div className="flex items-center gap-3 mb-2">
                    <Activity className="text-blue-400" size={20} />
                    <span className="text-slate-300 font-medium">Completeness</span>
                </div>
                <div className="text-2xl font-bold text-white mb-1">{summary?.completeness_pct || 0}%</div>
                <div className="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
                    <div className="h-full bg-blue-500" style={{width: `${summary?.completeness_pct || 0}%`}}></div>
                </div>
            </div>

             <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                <div className="flex items-center gap-3 mb-2">
                    <CheckCircle className="text-emerald-400" size={20} />
                    <span className="text-slate-300 font-medium">Accuracy</span>
                </div>
                <div className="text-2xl font-bold text-white mb-1">{summary?.accuracy_pct || 0}%</div>
                 <div className="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
                    <div className="h-full bg-emerald-500" style={{width: `${summary?.accuracy_pct || 0}%`}}></div>
                </div>
            </div>

             <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                <div className="flex items-center gap-3 mb-2">
                    <Clock className="text-purple-400" size={20} />
                    <span className="text-slate-300 font-medium">Freshness</span>
                </div>
                <div className="text-2xl font-bold text-white mb-1">{summary?.freshness_hours || 0}h</div>
                <div className="text-xs text-slate-500">Avg. latency</div>
            </div>
        </div>

        {/* Issues List */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden">
            <div className="p-6 border-b border-slate-800 flex justify-between items-center">
                <h3 className="text-lg font-semibold text-white">Active Quality Issues</h3>
                <span className="bg-red-500/10 text-red-400 px-3 py-1 rounded-full text-xs font-medium border border-red-500/20">
                    {summary?.open_issues || 0} Open
                </span>
            </div>
            
            <div className="divide-y divide-slate-800">
                {issues.map(issue => (
                    <div key={issue.id} className="p-4 hover:bg-slate-800/50 transition-colors flex items-start justify-between">
                        <div className="flex gap-4">
                            <div className="mt-1">
                                {issue.severity === 'critical' ? <AlertOctagon className="text-red-500" /> : 
                                 issue.severity === 'high' ? <AlertOctagon className="text-orange-500" /> :
                                 <AlertOctagon className="text-yellow-500" />}
                            </div>
                            <div>
                                <h4 className="font-medium text-slate-200">{issue.description}</h4>
                                <div className="text-sm text-slate-400 mt-1 flex gap-4">
                                    <span className="flex items-center gap-1"><span className="text-slate-600">Table:</span> {issue.table}</span>
                                    <span className="flex items-center gap-1"><span className="text-slate-600">Rule:</span> {issue.rule_id}</span>
                                </div>
                            </div>
                        </div>
                        <div className="flex items-center gap-4">
                            <span className={`px-2 py-1 rounded text-xs uppercase font-bold tracking-wide ${
                                issue.status === 'open' ? 'bg-red-500/10 text-red-500' : 'bg-green-500/10 text-green-500'
                            }`}>
                                {issue.status}
                            </span>
                            {issue.status === 'open' && (
                                <button 
                                    onClick={() => handleResolve(issue.id)}
                                    className="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs rounded border border-slate-700 transition-colors"
                                >
                                    Resolve
                                </button>
                            )}
                        </div>
                    </div>
                ))}
                {issues.length === 0 && !loading && (
                    <div className="p-8 text-center text-slate-500">No active quality issues found. Good job!</div>
                )}
            </div>
        </div>
    </div>
  );
};

export default DataQualityDashboard;
