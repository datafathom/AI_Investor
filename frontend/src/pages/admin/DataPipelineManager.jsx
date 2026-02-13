import React, { useState, useEffect } from 'react';
import { ingestionService } from '../../services/ingestionService';
import PipelineStatusCard from '../../components/cards/PipelineStatusCard';
import PipelineDAG from '../../components/charts/PipelineDAG';
import { RefreshCw, Plus, Activity } from 'lucide-react';
import { toast } from 'sonner';

const DataPipelineManager = () => {
  const [pipelines, setPipelines] = useState([]);
  const [selectedPipeline, setSelectedPipeline] = useState(null);
  const [loading, setLoading] = useState(true);

  const fetchPipelines = async () => {
    try {
      setLoading(true);
      const data = await ingestionService.listPipelines();
      setPipelines(data);
      if (!selectedPipeline && data.length > 0) {
        setSelectedPipeline(data[0]);
      }
    } catch (error) {
      toast.error("Failed to load pipelines");
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPipelines();
    const interval = setInterval(fetchPipelines, 30000); // Audit every 30s
    return () => clearInterval(interval);
  }, []);

  const handleTrigger = async (id) => {
    try {
      toast.info("Triggering pipeline...");
      await ingestionService.triggerPipeline(id);
      toast.success("Pipeline triggered successfully");
      fetchPipelines();
    } catch (error) {
      toast.error("Failed to trigger pipeline");
    }
  };

  return (
    <div className="p-6 h-full overflow-y-auto bg-slate-950 text-slate-200">
      <div className="flex justify-between items-center mb-8">
        <div>
            <h1 className="text-3xl font-bold bg-gradient-to-r from-cyan-400 to-blue-500 bg-clip-text text-transparent">
                Data Pipeline Manager
            </h1>
            <p className="text-slate-400 mt-2">Orchestrate and monitor data ingestion flows.</p>
        </div>
        <div className="flex gap-3">
             <button 
                onClick={fetchPipelines}
                className="p-2 bg-slate-800 hover:bg-slate-700 rounded-md border border-slate-700 transition-colors"
            >
                <RefreshCw size={20} className={loading ? "animate-spin" : ""} />
            </button>
            <button className="flex items-center gap-2 px-4 py-2 bg-cyan-600 hover:bg-cyan-500 text-white rounded-md font-medium transition-colors">
                <Plus size={18} /> New Pipeline
            </button>
        </div>
      </div>

      <div className="grid grid-cols-12 gap-6">
        {/* Left Column: Pipeline List */}
        <div className="col-span-12 lg:col-span-4 space-y-4">
            <h2 className="text-xl font-mono text-slate-400 flex items-center gap-2">
                <Activity size={20} /> Active Pipelines
            </h2>
            <div className="grid gap-4">
                {pipelines.map(pipeline => (
                    <div 
                        key={pipeline.id} 
                        onClick={() => setSelectedPipeline(pipeline)}
                        className={`cursor-pointer ring-2 ${selectedPipeline?.id === pipeline.id ? 'ring-cyan-500' : 'ring-transparent'} rounded-lg transition-all`}
                    >
                        <PipelineStatusCard 
                            pipeline={pipeline} 
                            onTrigger={handleTrigger} 
                        />
                    </div>
                ))}
            </div>
        </div>

        {/* Right Column: Details & DAG */}
        <div className="col-span-12 lg:col-span-8 flex flex-col gap-6">
            {selectedPipeline ? (
                <>
                    <div className="bg-slate-900/50 p-6 rounded-xl border border-slate-800">
                        <div className="flex justify-between items-center mb-6">
                            <h2 className="text-2xl font-bold text-white">{selectedPipeline.name}</h2>
                            <span className="px-3 py-1 bg-slate-800 rounded-full text-xs font-mono text-slate-400">ID: {selectedPipeline.id}</span>
                        </div>
                        <PipelineDAG pipeline={selectedPipeline} />
                    </div>

                    <div className="bg-slate-900/50 p-6 rounded-xl border border-slate-800 flex-1">
                        <h3 className="text-lg font-semibold mb-4 text-slate-300">Recent Runs</h3>
                        <div className="space-y-2">
                            {/* Placeholder for run history component */}
                            <div className="p-3 bg-slate-900 border border-slate-700/50 rounded flex justify-between items-center">
                                <div className="flex items-center gap-3">
                                    <div className="w-2 h-2 bg-emerald-500 rounded-full"></div>
                                    <span className="text-sm font-mono text-slate-300">Run #4928</span>
                                </div>
                                <span className="text-xs text-slate-500">2 mins ago</span>
                            </div>
                            <div className="p-3 bg-slate-900 border border-slate-700/50 rounded flex justify-between items-center">
                                <div className="flex items-center gap-3">
                                    <div className="w-2 h-2 bg-red-500 rounded-full"></div>
                                    <span className="text-sm font-mono text-slate-300">Run #4927</span>
                                </div>
                                <span className="text-xs text-slate-500">1 hour ago</span>
                            </div>
                        </div>
                    </div>
                </>
            ) : (
                <div className="h-full flex items-center justify-center text-slate-500">
                    Select a pipeline to view details
                </div>
            )}
        </div>
      </div>
    </div>
  );
};

export default DataPipelineManager;
