import React from 'react';
import { Cpu, Activity, PlusCircle, MinusCircle, RefreshCw } from 'lucide-react';
import useSystemHealthStore from '../../stores/systemHealthStore';
import './AgentLoadBalancer.css';

const AgentLoadBalancer = () => {
    const { agentLoad } = useSystemHealthStore();

    return (
        <div className="agent-load-balancer-widget">
            <div className="widget-header">
                <h3><Cpu size={18} className="text-purple-400" /> Agent 'Brain' Load Balancer</h3>
                <div className="balancer-actions">
                    <button className="scale-btn scale-up"><PlusCircle size={14}/> Scale Stacker</button>
                    <button className="scale-btn scale-down"><MinusCircle size={14}/> Reduce</button>
                </div>
            </div>

            <div className="process-tree">
                <div className="tree-header">
                    <span>Process / Agent</span>
                    <span>PID</span>
                    <span>CPU</span>
                    <span>RAM</span>
                    <span>Status</span>
                </div>
                
                {agentLoad.length > 0 ? agentLoad.map((agent, idx) => (
                    <div key={agent.pid || idx} className={`tree-item ${agent.is_root ? 'root' : 'child'} ${agent.status === 'error' ? 'error' : ''}`}>
                        <div className="col name">
                            {agent.is_root ? (
                                <><span className="expander">-</span> {agent.name}</>
                            ) : (
                                <>├── {agent.name}</>
                            )}
                        </div>
                        <div className="col pid">{agent.pid || 'N/A'}</div>
                        <div className="col cpu">{agent.cpu_usage}%</div>
                        <div className="col ram">{agent.ram_usage}MB</div>
                        <div className="col status" style={{ color: agent.status === 'running' ? '#4ade80' : '#f87171' }}>
                            {agent.status.toUpperCase()}
                        </div>
                    </div>
                )) : (
                    <div className="p-4 text-center text-zinc-500 font-mono text-[10px] uppercase">
                        No active agents detected in cluster
                    </div>
                )}
            </div>

             <div className="health-summary">
                <div className="summary-item">
                    <span className="count">{agentLoad.filter(a => a.status === 'running').length}</span>
                    <span className="lbl">Healthy Agents</span>
                </div>
                <div className="summary-item error">
                    <span className="count">{agentLoad.filter(a => a.status !== 'running').length}</span>
                    <span className="lbl">Not Running</span>
                </div>
                 <div className="summary-item">
                    <span className="count">{(agentLoad.reduce((acc, a) => acc + a.cpu_usage, 0) / (agentLoad.length || 1)).toFixed(1)}%</span>
                    <span className="lbl">Avg Cluster Load</span>
                </div>
            </div>
        </div>
    );
};

export default AgentLoadBalancer;
