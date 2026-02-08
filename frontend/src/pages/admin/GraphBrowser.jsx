import React, { useState, useEffect } from 'react';
import './GraphBrowser.css';

const GraphBrowser = () => {
    const [query, setQuery] = useState('MATCH (n) RETURN n LIMIT 25');
    const [results, setResults] = useState([]);
    const [schema, setSchema] = useState({ nodes: [], relationships: [] });
    const [loading, setLoading] = useState(true);
    const [executing, setExecuting] = useState(false);

    useEffect(() => {
        fetchSchema();
    }, []);

    const fetchSchema = async () => {
        try {
            const response = await fetch('/api/v1/admin/graph/schema');
            const data = await response.json();
            setSchema(data);
        } catch (error) {
            console.error("Error fetching schema:", error);
        } finally {
            setLoading(false);
        }
    };

    const handleRunQuery = async () => {
        setExecuting(true);
        try {
            const response = await fetch('/api/v1/admin/graph/query', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ query })
            });
            const data = await response.json();
            setResults(data.results || []);
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
                    <h3>SCHEMA</h3>
                    <div className="schema-group">
                        <label>NODE_LABELS</label>
                        {schema.nodes.map(l => <div key={l} className="label-pill node">{l}</div>)}
                    </div>
                    <div className="schema-group">
                        <label>RELATIONSHIPS</label>
                        {schema.relationships.map(r => <div key={r} className="label-pill rel">{r}</div>)}
                    </div>
                </aside>

                <main className="query-main">
                    <section className="query-editor">
                        <div className="editor-header">
                            <label>CYPHER_CONSOLE</label>
                            <button onClick={handleRunQuery} disabled={executing}>
                                {executing ? 'EXECUTING...' : 'RUN_QUERY'}
                            </button>
                        </div>
                        <textarea 
                            value={query} 
                            onChange={(e) => setQuery(e.target.value)}
                            spellCheck="false"
                        />
                    </section>

                    <section className="results-view">
                        <div className="view-header">
                            <label>QUERY_RESULTS ({results.length})</label>
                        </div>
                        <div className="results-scroll">
                            <pre>{JSON.stringify(results, null, 2)}</pre>
                        </div>
                    </section>
                </main>
            </div>
        </div>
    );
};

export default GraphBrowser;
