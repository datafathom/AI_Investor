import React, { useState, useEffect, useRef, Suspense, lazy } from 'react';
const ForceGraph3D = lazy(() => import('react-force-graph-3d').catch(err => {
    console.error("Vite Dynamic Import Failed:", err);
    return { default: () => <div className="graph-error-msg">VISUALIZER_LOAD_FAILED: THE_3D_ENGINE_STALLED</div> };
}));

const Inspector = ({ item, type, onClear }) => {
    if (!item) return null;
    return (
        <div className="inspector-overlay">
            <div className="inspector-header">
                <span className="type-tag">{type.toUpperCase()}</span>
                <span className="id-tag">ID: {item.id}</span>
                <button className="close-mini-btn" onClick={onClear}>&times;</button>
            </div>
            <div className="inspector-body">
                {type === 'node' && (
                    <div className="labels-row">
                        {item.labels?.map(l => <span key={l} className="label-badge">{l}</span>)}
                    </div>
                )}
                {type === 'edge' && (
                    <div className="edge-type">TYPE: <strong>{item.type}</strong></div>
                )}
                <div className="props-list">
                    <label>PROPERTIES</label>
                    {item.properties && Object.keys(item.properties).length > 0 ? (
                        Object.entries(item.properties).map(([k, v]) => (
                            <div key={k} className="prop-row">
                                <span className="prop-key">{k}:</span>
                                <span className="prop-val">{String(v)}</span>
                            </div>
                        ))
                    ) : (
                        <div className="no-props">NO_PROPERTIES</div>
                    )}
                </div>
            </div>
        </div>
    );
};
import './GraphBrowser.css';
import apiClient from '../../services/apiClient';

const GraphBrowser = () => {
    const [query, setQuery] = useState('MATCH (n) RETURN n LIMIT 25');
    const [results, setResults] = useState([]);
    const [graphData, setGraphData] = useState({ nodes: [], links: [] });
    const [viewMode, setViewMode] = useState('json'); // 'json' or 'visual'
    const [schema, setSchema] = useState({ nodes: [], relationships: [] });
    const [loading, setLoading] = useState(true);
    const [executing, setExecuting] = useState(false);
    const [selectedItem, setSelectedItem] = useState(null);
    const [selectedType, setSelectedType] = useState(null); // 'node' or 'edge'
    const containerRef = useRef();

    useEffect(() => {
        fetchSchema();
    }, []);

    const fetchSchema = async () => {
        const timestamp = new Date().toLocaleTimeString();
        console.log(`[${timestamp}] [GraphBrowser] fetchSchema: START`);
        try {
            console.log(`[${timestamp}] [GraphBrowser] Axios request to /admin/graph/schema: PRE_SEND`);
            const data = await apiClient.get('/admin/graph/schema');
            console.log(`[${timestamp}] [GraphBrowser] Axios request to /admin/graph/schema: SUCCESS`, data);
            setSchema(data);
        } catch (error) {
            console.error(`[${timestamp}] [GraphBrowser] Axios request to /admin/graph/schema: FAILED`, error);
            if (error.code === 'ECONNABORTED') {
                console.warn(`[${timestamp}] [GraphBrowser] DETECTED_TIMEOUT: Server took too long (>30s)`);
            }
        } finally {
            console.log(`[${timestamp}] [GraphBrowser] fetchSchema: FINISHED (setLoading -> false)`);
            setLoading(false);
        }
    };

    const transformData = (rawResults) => {
        const nodes = new Map();
        const links = [];

        rawResults.forEach(row => {
            Object.values(row).forEach(val => {
                if (val && typeof val === 'object') {
                    // Check if it's a node
                    if (val.identity !== undefined && val.labels) {
                        nodes.set(val.identity, {
                            id: val.identity,
                            name: val.properties?.name || val.properties?.id || val.labels[0],
                            labels: val.labels,
                            properties: val.properties,
                            color: val.labels.includes('Investor') ? '#00f2ff' : 
                                   val.labels.includes('Agent') ? '#00ff88' : 
                                   val.labels.includes('Trade') ? '#ff9800' : '#888'
                        });
                    }
                    // Check if it's a relationship
                    if (val.start !== undefined && val.end !== undefined && val.type) {
                        links.push({
                            id: val.identity,
                            source: val.start,
                            target: val.end,
                            type: val.type,
                            properties: val.properties
                        });
                    }
                }
            });
        });

        return { nodes: Array.from(nodes.values()), links };
    };

    const handleRunQuery = async () => {
        setExecuting(true);
        try {
            const data = await apiClient.post('/admin/graph/query', { query });
            const rawResults = data.results || [];
            setResults(rawResults);
            setGraphData(transformData(rawResults));
        } catch (error) {
            console.error("Error executing query:", error);
        } finally {
            setExecuting(false);
        }
    };

    if (loading) return <div className="graph-loading">INITIALIZING_BOLT_PROTOCOL...</div>;

    return (
        <div className="graph-browser-container">
            <header className="page-header">
                <h1>NEO4J_GRAPH_EXPLORER</h1>
            </header>

            <div className="graph-layout">
                <aside className="schema-sidebar">
                    <div className="sidebar-header">
                        <h3>SCHEMA</h3>
                        <button className="retry-mini-btn" onClick={fetchSchema} title="Retry Connection">
                            ⟳
                        </button>
                    </div>
                    <div className="schema-group">
                        <label>NODE_LABELS</label>
                        {schema.nodes.length > 0 ? (
                            schema.nodes.map(l => <div key={l} className="label-pill node">{l}</div>)
                        ) : (
                            <div className="no-schema">NO_NODES</div>
                        )}
                    </div>
                    <div className="schema-group">
                        <label>RELATIONSHIPS</label>
                        {schema.relationships.length > 0 ? (
                            schema.relationships.map(r => <div key={r} className="label-pill rel">{r}</div>)
                        ) : (
                            <div className="no-schema">NO_RELS</div>
                        )}
                    </div>
                </aside>

                <main className="query-main">
                    <section className="query-editor">
                        <div className="editor-header">
                            <label>CYPHER_CONSOLE</label>
                            <button className="run-btn" onClick={handleRunQuery} disabled={executing}>
                                {executing ? '...' : 'RUN'}
                            </button>
                        </div>
                        <input 
                            type="text"
                            value={query} 
                            onChange={(e) => setQuery(e.target.value)}
                            spellCheck="false"
                            onKeyDown={(e) => e.key === 'Enter' && handleRunQuery()}
                        />
                    </section>

                    <section className="results-view" ref={containerRef}>
                        <div className="view-header">
                            <div className="header-meta">
                                <label>QUERY_RESULTS ({results.length})</label>
                            </div>
                            <div className="view-selector">
                                <button 
                                    className={viewMode === 'json' ? 'active' : ''} 
                                    onClick={() => setViewMode('json')}
                                >
                                    DATA
                                </button>
                                <button 
                                    className={viewMode === 'visual' ? 'active' : ''} 
                                    onClick={() => setViewMode('visual')}
                                >
                                    VISUAL
                                </button>
                            </div>
                        </div>
                        
                        <div className="view-content">
                            {viewMode === 'json' ? (
                                <div className="results-scroll">
                                    <pre>{JSON.stringify(results, null, 2)}</pre>
                                </div>
                            ) : (
                                <div className="visualizer-container">
                                    <Suspense fallback={<div className="graph-loading-small">LOADING_3D_ENGINE...</div>}>
                                        <ForceGraph3D
                                            graphData={graphData}
                                            backgroundColor="#000000"
                                            nodeColor={node => node.color}
                                            nodeLabel={node => `${node.labels[0]}: ${node.name}`}
                                            linkLabel={link => link.type}
                                            linkDirectionalArrowLength={3.5}
                                            linkDirectionalArrowRelPos={1}
                                            linkCurvature={0.25}
                                            width={containerRef.current?.clientWidth > 0 ? containerRef.current.clientWidth - 2 : 800}
                                            height={containerRef.current?.clientHeight > 0 ? containerRef.current.clientHeight - 50 : 600}
                                            cooldownTicks={100}
                                            onEngineStop={() => console.log('3D Engine Stabilized')}
                                            onNodeClick={node => {
                                                setSelectedItem(node);
                                                setSelectedType('node');
                                            }}
                                            onLinkClick={link => {
                                                setSelectedItem(link);
                                                setSelectedType('edge');
                                            }}
                                        />
                                    </Suspense>
                                    <Inspector 
                                        item={selectedItem} 
                                        type={selectedType} 
                                        onClear={() => {
                                            setSelectedItem(null);
                                            setSelectedType(null);
                                        }} 
                                    />
                                </div>
                            )}
                        </div>
                    </section>
                    
                    {/* TIMELINE_FIX: Buffer to prevent footer clipping */}
                    <div className="graph-footer-buffer"></div>
                </main>
            </div>
        </div>
    );
};

export default GraphBrowser;
