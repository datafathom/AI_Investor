import React from 'react';
import { Cpu, Activity, PlusCircle, MinusCircle } from 'lucide-react';
import './AgentLoadBalancer.css';

const AgentLoadBalancer = () => {
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
                
                <div className="tree-item root">
                    <div className="col name">
                        <span className="expander">-</span> Omni-Forecaster.Main
                    </div>
                    <div className="col pid">8841</div>
                    <div className="col cpu">12%</div>
                    <div className="col ram">1.2GB</div>
                    <div className="col status text-green-400">RUNNING</div>
                </div>

                <div className="tree-item child">
                    <div className="col name">
                        ├── Sentiment-Worker-1
                    </div>
                    <div className="col pid">8842</div>
                    <div className="col cpu">45%</div>
                    <div className="col ram">800MB</div>
                    <div className="col status text-green-400">RUNNING</div>
                </div>

                 <div className="tree-item child">
                    <div className="col name">
                        ├── Sentiment-Worker-2
                    </div>
                    <div className="col pid">8843</div>
                    <div className="col cpu">42%</div>
                    <div className="col ram">750MB</div>
                    <div className="col status text-green-400">RUNNING</div>
                </div>

                <div className="tree-item child error">
                    <div className="col name">
                        └── Technical-Worker-1
                    </div>
                    <div className="col pid">8850</div>
                    <div className="col cpu">0%</div>
                    <div className="col ram">0MB</div>
                    <div className="col status text-red-400">RESTARTING</div>
                </div>
            </div>

             <div className="health-summary">
                <div className="summary-item">
                    <span className="count">14</span>
                    <span className="lbl">Healthy Agents</span>
                </div>
                <div className="summary-item error">
                    <span className="count">1</span>
                    <span className="lbl">Restarting</span>
                </div>
                 <div className="summary-item">
                    <span className="count">0.4%</span>
                    <span className="lbl">Error Rate</span>
                </div>
            </div>
        </div>
    );
};

export default AgentLoadBalancer;
