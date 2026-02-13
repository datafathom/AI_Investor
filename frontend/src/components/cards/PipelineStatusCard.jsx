import React from 'react';
import { Play, Clock, Activity, AlertCircle, CheckCircle } from 'lucide-react';

const PipelineStatusCard = ({ pipeline, onTrigger }) => {
  const getStatusColor = (status) => {
    switch (status) {
      case 'running': return 'text-blue-400 border-blue-500/30 bg-blue-500/10';
      case 'error': return 'text-red-400 border-red-500/30 bg-red-500/10';
      case 'idle': return 'text-slate-400 border-slate-700/50 bg-slate-800/50';
      default: return 'text-slate-400 border-slate-700/50';
    }
  };

  return (
    <div className={`p-4 rounded-lg border ${getStatusColor(pipeline.status)} transition-all hover:bg-slate-800/80`}>
      <div className="flex justify-between items-start mb-3">
        <div>
          <h3 className="text-lg font-semibold text-slate-100">{pipeline.name}</h3>
          <p className="text-xs text-slate-400 mt-1">{pipeline.description}</p>
        </div>
        <div className={`px-2 py-1 rounded text-xs font-mono uppercase ${pipeline.status === 'running' ? 'animate-pulse' : ''}`}>
            {pipeline.status}
        </div>
      </div>

      <div className="grid grid-cols-2 gap-2 text-sm text-slate-300 mb-4">
        <div className="flex items-center gap-2">
            <Clock size={14} className="text-slate-500" />
            <span>{pipeline.schedule}</span>
        </div>
        <div className="flex items-center gap-2">
            <Activity size={14} className="text-slate-500" />
            <span>Success Rate: 98%</span>
        </div>
      </div>

      <div className="flex justify-between items-center pt-3 border-t border-slate-700/50">
        <span className="text-xs text-slate-500">
            Last run: {pipeline.last_run ? new Date(pipeline.last_run).toLocaleString() : 'Never'}
        </span>
        <button 
            onClick={() => onTrigger(pipeline.id)}
            disabled={pipeline.status === 'running'}
            className="p-2 rounded-md hover:bg-cyan-500/20 text-cyan-400 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            title="Trigger Manual Run"
        >
            <Play size={16} />
        </button>
      </div>
    </div>
  );
};

export default PipelineStatusCard;
