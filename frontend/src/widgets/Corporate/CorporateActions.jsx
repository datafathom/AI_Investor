import React from 'react';
import { GitBranch, Bell, History } from 'lucide-react';
import './CorporateActions.css';

const CorporateActions = () => {
    return (
        <div className="corporate-actions-widget">
            <div className="widget-header">
                <h3><GitBranch size={18} className="text-indigo-400" /> Splits & Spin-offs</h3>
                <div className="action-notification">
                    <Bell size={14} className="text-yellow-400" /> 1 New Action
                </div>
            </div>

            <div className="actions-feed">
                <div className="action-card new">
                    <div className="action-header">
                        <span className="type split">STOCK SPLIT</span>
                        <span className="date">Ex-Date: Nov 15</span>
                    </div>
                    <div className="action-body">
                        <strong>NVDA</strong> announced a <strong>10-for-1</strong> split.
                        <div className="cost-basis-preview">
                            <div>Cost Basis Adj:</div>
                            <div className="adj-val">$420.00 → $42.00</div>
                        </div>
                    </div>
                </div>

                <div className="separation-visualizer">
                    <h4>Spin-off Tree Visualization</h4>
                    <div className="tree-mock">
                        <div className="node parent">GE</div>
                        <div className="connector">|</div>
                        <div className="node-row">
                             <div className="node child">GE Health</div>
                             <div className="node child">GE Aero</div>
                             <div className="node child">GE Vernova</div>
                        </div>
                    </div>
                </div>

                <div className="history-link">
                     <History size={14} /> View Historical Actions Log
                </div>
            </div>
        </div>
    );
};

export default CorporateActions;
