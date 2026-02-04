/**
 * ==============================================================================
 * FILE: frontend2/src/pages/AlgorithmicTradingDashboard.jsx
 * ROLE: Algorithmic Trading Dashboard
 * PURPOSE: Phase 15 - Algorithmic Trading & Strategy Automation
 *          Displays trading strategies, execution status, and performance monitoring.
 * 
 * INTEGRATION POINTS:
 *    - StrategyAPI: /api/v1/strategy endpoints
 * 
 * FEATURES:
 *    - Strategy builder
 *    - Live strategy execution
 *    - Performance monitoring
 *    - Risk controls
 * 
 * AUTHOR: AI Investor Team
 * CREATED: 2026-01-21
 * LAST_MODIFIED: 2026-01-21
 * ==============================================================================
 */

import React, { useState, useEffect } from 'react';
import { StorageService } from '../utils/storageService';

import useAlgoStore from '../stores/algoStore';
import './AlgorithmicTradingDashboard.css';

import { Responsive, WidthProvider } from 'react-grid-layout';

const ResponsiveGridLayout = WidthProvider(Responsive);

const AlgorithmicTradingDashboard = () => {
  const {
      strategies,
      selectedStrategy,
      performance,
      isLoading,
      fetchStrategies,
      setSelectedStrategy,
      fetchPerformance,
      createStrategy,
      deployStrategy,
      pauseStrategy
  } = useAlgoStore();

  const [userId] = useState('user_1');
  const [newStrategy, setNewStrategy] = useState({ name: '', description: '' });

  const DEFAULT_LAYOUT = {
    lg: [
      { i: 'create', x: 0, y: 0, w: 12, h: 2 },
      { i: 'strategies', x: 0, y: 2, w: 7, h: 8 },
      { i: 'performance', x: 7, y: 2, w: 5, h: 8 }
    ]
  };
  const STORAGE_KEY = 'layout_algo_trading';

  const [layouts, setLayouts] = useState(() => {
    try {
      const saved = localStorage.getItem(STORAGE_KEY);
      return saved ? JSON.parse(saved) : DEFAULT_LAYOUT;
    } catch (e) {
      return DEFAULT_LAYOUT;
    }
  });

  const onLayoutChange = (currentLayout, allLayouts) => {
    setLayouts(allLayouts);
    StorageService.set(STORAGE_KEY, allLayouts);
  };

  useEffect(() => {
    fetchStrategies(userId);
  }, [fetchStrategies, userId]);

  useEffect(() => {
    if (selectedStrategy) {
      fetchPerformance(selectedStrategy.strategy_id);
    }
  }, [selectedStrategy, fetchPerformance]);


  const handleCreateStrategy = async () => {
    if (!newStrategy.name) return;
    
    await createStrategy(userId, {
        strategy_name: newStrategy.name,
        description: newStrategy.description,
        rules: []
    });
    
    setNewStrategy({ name: '', description: '' });
  };

  const handleDeployStrategy = async (strategyId) => {
    await deployStrategy(strategyId, userId);
  };

  const handlePauseStrategy = async (strategyId) => {
    await pauseStrategy(strategyId, userId);
  };

  return (
    <div className="full-bleed-page algorithmic-trading-dashboard">
      <div className="dashboard-header">
        <h1>Algorithmic Trading</h1>
        <p className="subtitle">Phase 15: Algorithmic Trading & Strategy Automation</p>
      </div>

      <div className="scrollable-content-wrapper">
        <ResponsiveGridLayout
          className="layout"
          layouts={layouts}
          onLayoutChange={onLayoutChange}
          breakpoints={{ lg: 1200, md: 996, sm: 768, xs: 480, xxs: 0 }}
          cols={{ lg: 12, md: 10, sm: 6, xs: 4, xxs: 2 }}
          rowHeight={80}
          isDraggable={true}
          isResizable={true}
          draggableHandle="h2"
          margin={[16, 16]}
        >
          {/* Create Strategy */}
          <div key="create" className="create-strategy-panel">
            <h2>Create Strategy</h2>
            <div className="strategy-form">
              <div className="form-group">
                <span className="form-label">Strategy Name</span>
                <input
                  type="text"
                  placeholder="e.g. Mean Reversion"
                  value={newStrategy.name}
                  onChange={(e) => setNewStrategy({ ...newStrategy, name: e.target.value })}
                  className="form-input"
                />
              </div>
              <div className="form-group">
                <span className="form-label">Description</span>
                <input
                  type="text"
                  placeholder="e.g. Simple RSI strategy"
                  value={newStrategy.description}
                  onChange={(e) => setNewStrategy({ ...newStrategy, description: e.target.value })}
                  className="form-input"
                />
              </div>
              <div className="form-group" style={{ flex: '0 0 auto', justifyContent: 'flex-end' }}>
                <button onClick={handleCreateStrategy} disabled={isLoading} className="create-button">
                  Create Strategy
                </button>
              </div>
            </div>
          </div>

          {/* Strategies List */}
          <div key="strategies" className="strategies-panel">
            <h2>Your Strategies</h2>
            {strategies.length > 0 ? (
              <div className="strategies-list">
                {strategies.map((strategy) => (
                  <div
                    key={strategy.strategy_id}
                    className={`strategy-card ${selectedStrategy?.strategy_id === strategy.strategy_id ? 'selected' : ''}`}
                    onClick={() => setSelectedStrategy(strategy)}
                  >
                    <div className="strategy-header">
                      <h3>{strategy.strategy_name}</h3>
                      <span className={`status ${strategy.status}`}>{strategy.status}</span>
                    </div>
                    <p className="strategy-description">{strategy.description || 'No description'}</p>
                    <div className="strategy-actions">
                      {strategy.status === 'active' ? (
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            handlePauseStrategy(strategy.strategy_id);
                          }}
                          className="pause-button"
                        >
                          Pause
                        </button>
                      ) : (
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            handleDeployStrategy(strategy.strategy_id);
                          }}
                          className="deploy-button"
                        >
                          Deploy
                        </button>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="no-data">No strategies created yet</div>
            )}
          </div>

          {/* Performance */}
          <div key="performance">
            {selectedStrategy && performance && (
              <div className="performance-panel h-full">
                <h2>Strategy Performance</h2>
                <div className="performance-metrics">
                  <div className="perf-card">
                    <div className="perf-label">Total Return</div>
                    <div className="perf-value" style={{ color: performance.total_return >= 0 ? '#00ff88' : '#ff4444' }}>
                      {(performance.total_return * 100).toFixed(2)}%
                    </div>
                  </div>
                  <div className="perf-card">
                    <div className="perf-label">Sharpe Ratio</div>
                    <div className="perf-value">{performance.sharpe_ratio?.toFixed(2)}</div>
                  </div>
                  <div className="perf-card">
                    <div className="perf-label">Win Rate</div>
                    <div className="perf-value">{(performance.win_rate * 100).toFixed(1)}%</div>
                  </div>
                  <div className="perf-card">
                    <div className="perf-label">Total Trades</div>
                    <div className="perf-value">{performance.total_trades}</div>
                  </div>
                </div>
                <div className="risk-controls">
                  <h3>Risk Controls</h3>
                  <div className="control-item">
                    <span>Max Position Size: ${selectedStrategy.max_position_size || 'N/A'}</span>
                  </div>
                  <div className="control-item">
                    <span>Max Daily Loss: ${selectedStrategy.max_daily_loss || 'N/A'}</span>
                  </div>
                  <div className="control-item">
                    <span>Max Drawdown: {(selectedStrategy.max_drawdown * 100 || 0).toFixed(1)}%</span>
                  </div>
                </div>
              </div>
            )}
            {!selectedStrategy && (
               <div className="performance-panel h-full flex items-center justify-center text-zinc-500">
                  <p>Select a strategy to view performance</p>
               </div>
            )}
          </div>
        </ResponsiveGridLayout>
        
        {/* Bottom Buffer */}
        <div className="scroll-buffer-100" />
      </div>
    </div>
  );
};

export default AlgorithmicTradingDashboard;
