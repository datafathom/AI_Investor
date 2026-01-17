/**
 * ==============================================================================
 * FILE: frontend2/src/pages/StrategyDistillery.jsx
 * ROLE: The Bio-Digital Lab
 * PURPOSE: 
 *   Visualize the genetic evolution of trading strategies.
 *   Shows generations, fitness trends, and the current "Alpha" genome.
 * ==============================================================================
 */

import React, { useState, useEffect, useMemo } from 'react';
import evolutionService from '../services/evolutionService';
import { SimpleLineChart, SimpleAreaChart } from '../components/Charts/SimpleCharts';
import './StrategyDistillery.css';

const StrategyDistillery = () => {
    const [status, setStatus] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const fetchStatus = async () => {
        try {
            const data = await evolutionService.getStatus();
            setStatus(data);
        } catch (err) {
            setError('Distillery offline or not started.');
        }
    };

    const startEvolution = async () => {
        setLoading(true);
        setError(null);
        try {
            await evolutionService.startEvolution();
            await fetchStatus();
        } catch (err) {
            setError('Failed to ignite the distillery.');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchStatus();
    }, []);

    const chartData = useMemo(() => {
        if (!status?.history) return [];
        return status.history.map(h => ({
            name: `G${h.generation}`,
            Best: h.best_fitness,
            Avg: h.avg_fitness
        }));
    }, [status]);

    return (
        <div className="distillery-container">
            <header className="distillery-header">
                <h1> Strategy Distillery</h1>
                <p>Evolutionary Parameter Optimization (Phase 37)</p>
            </header>

            {!status && !loading && (
                <div className="empty-state">
                    <button className="ignite-btn" onClick={startEvolution}>
                        Ignite Evolution
                    </button>
                    {error && <p className="error-msg">{error}</p>}
                </div>
            )}

            {loading && <div className="loading-spinner">Simulating Generations...</div>}

            {status && (
                <div className="distillery-grid">
                    <section className="stats-card">
                        <h3>Evolutionary Vitals</h3>
                        <div className="vitals-row">
                            <div className="vital">
                                <span className="label">Generation</span>
                                <span className="value">{status.current_generation}</span>
                            </div>
                            <div className="vital">
                                <span className="label">Best Fitness</span>
                                <span className="value">{status.best_performer.fitness.toFixed(4)}</span>
                            </div>
                        </div>
                        <button className="evolve-more-btn" onClick={startEvolution} disabled={loading}>
                            Run 5 More Generations
                        </button>
                    </section>

                    <section className="alpha-genome">
                        <h3>Current Alpha Genome</h3>
                        <div className="gene-pool">
                            {Object.entries(status.best_performer.genes).map(([gene, val]) => (
                                <div key={gene} className="gene-tag">
                                    <span className="gene-name">{gene}</span>
                                    <span className="gene-value">{val}</span>
                                </div>
                            ))}
                        </div>
                    </section>

                    <section className="fitness-chart">
                        <h3>Fitness Optimization</h3>
                        <div style={{ height: '300px' }}>
                            <SimpleLineChart data={chartData} />
                        </div>
                    </section>
                </div>
            )}
        </div>
    );
};

export default StrategyDistillery;
