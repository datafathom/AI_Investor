import React, { useEffect, useState } from 'react';
import { Share2, Network, Shield, Loader2 } from 'lucide-react';
import useEstateStore from '../../stores/estateStore';
import './EntityGraph.css';

const EntityGraph = () => {
    const { entityGraph, isLoading, fetchEstateData } = useEstateStore();
    const [selectedNodeId, setSelectedNodeId] = useState('n1');

    useEffect(() => {
        if (entityGraph.nodes.length === 0) {
            fetchEstateData();
        }
    }, [fetchEstateData, entityGraph.nodes.length]);

    const selectedNode = entityGraph.nodes.find(n => n.id === selectedNodeId) || entityGraph.nodes[0];

    const getNodeIcon = (type) => {
        switch (type) {
            case 'TRUST': return <Shield size={24} />;
            case 'INDIVIDUAL': return <Network size={24} />;
            default: return <Share2 size={24} />;
        }
    };

    if (isLoading && entityGraph.nodes.length === 0) {
        return (
            <div className="entity-graph-widget loading">
                <Loader2 className="animate-spin" />
                <span>Visualizing Legal Structure...</span>
            </div>
        );
    }

    return (
        <div className="entity-graph-widget">
            <div className="widget-header">
                <h3><Network size={18} /> Trust & Entity Legal Structure (Neo4j)</h3>
                <div className="graph-controls">
                    <button className="control-btn"><Share2 size={14} /> Optimize</button>
                    <button className="control-btn primary">Add Entity</button>
                </div>
            </div>

            <div className="graph-viewport">
                {entityGraph.nodes.map((node, idx) => (
                    <div 
                        key={node.id} 
                        className={`graph-node ${node.type.toLowerCase()} ${selectedNodeId === node.id ? 'active' : ''}`}
                        style={{ 
                            top: `${20 + (idx % 2 === 0 ? 0 : 40)}%`, 
                            left: `${20 + (idx * 20)}%` 
                        }}
                        onClick={() => setSelectedNodeId(node.id)}
                    >
                        {getNodeIcon(node.type)}
                        <span>{node.label}</span>
                        <div className="node-meta">{node.type} • Active</div>
                    </div>
                ))}

                <svg className="graph-connections" width="100%" height="100%">
                    {entityGraph.edges.map((edge, i) => {
                        const sourceIdx = entityGraph.nodes.findIndex(n => n.id === edge.source);
                        const targetIdx = entityGraph.nodes.findIndex(n => n.id === edge.target);
                        if (sourceIdx === -1 || targetIdx === -1) return null;
                        
                        const x1 = 20 + (sourceIdx * 20);
                        const y1 = 20 + (sourceIdx % 2 === 0 ? 0 : 40);
                        const x2 = 20 + (targetIdx * 20);
                        const y2 = 20 + (targetIdx % 2 === 0 ? 0 : 40);

                        return (
                            <line 
                                key={i}
                                x1={`${x1}%`} y1={`${y1 + 10}%`} 
                                x2={`${x2}%`} y2={`${y2 + 10}%`} 
                                stroke="rgba(255,255,255,0.2)" 
                                strokeWidth="2" 
                            />
                        );
                    })}
                </svg>
            </div>

            {selectedNode && (
                <div className="entity-details-panel">
                    <div className="detail-header">
                        <span className="detail-title">Selection: {selectedNode.label}</span>
                        <span className="detail-badge">Active</span>
                    </div>
                    <div className="detail-grid">
                        <div className="item">
                            <label>Tax ID</label>
                            <span>{selectedNode.tax_id || 'N/A'}</span>
                        </div>
                        <div className="item">
                            <label>Jurisdiction</label>
                            <span>{selectedNode.jurisdiction || 'Direct Control'}</span>
                        </div>
                        <div className="item">
                            <label>Entity Type</label>
                            <span>{selectedNode.type}</span>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default EntityGraph;
