import { Responsive, WidthProvider } from 'react-grid-layout';

const ResponsiveGridLayout = WidthProvider(Responsive);

const CreditMonitoringDashboard = () => {
  const [creditScore, setCreditScore] = useState({
    score: 742,
    trend: 'up',
    change: 12,
    bureau: 'Experian',
    last_updated: new Date().toISOString()
  });
  const [creditReport, setCreditReport] = useState({
    total_accounts: 14,
    credit_utilization: 0.12,
    payment_history_percent: 100,
    credit_age_months: 84
  });
  const [recommendations, setRecommendations] = useState([
    { title: 'Decrease Utilization', description: 'Keep total credit card usage below 10% to boost your score.', estimated_score_impact: 15, priority: 'High' },
    { title: 'Age of Accounts', description: 'Avoid closing old accounts to maintain a longer credit history.', estimated_score_impact: 8, priority: 'Medium' }
  ]);
  const [simulationResult, setSimulationResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [userId] = useState('user_1');

  const DEFAULT_LAYOUT = {
    lg: [
      { i: 'score', x: 0, y: 0, w: 4, h: 5 },
      { i: 'report', x: 4, y: 0, w: 8, h: 5 },
      { i: 'recommendations', x: 0, y: 5, w: 7, h: 8 },
      { i: 'simulation', x: 7, y: 5, w: 5, h: 8 }
    ]
  };

  useEffect(() => {
    // fetchData() would go here
  }, []);

  const runSimulation = async (action) => {
    setLoading(true);
    setTimeout(() => {
      setSimulationResult({
        current_score: 742,
        projected_score: 757,
        score_change: 15
      });
      setLoading(false);
    }, 1000);
  };

  const getScoreColor = (score) => {
    if (score >= 750) return '#00ff88';
    if (score >= 700) return '#88ff00';
    if (score >= 650) return '#ff8844';
    return '#ff4444';
  };

  const getScoreCategory = (score) => {
    if (score >= 750) return 'Excellent';
    if (score >= 700) return 'Good';
    if (score >= 650) return 'Fair';
    return 'Poor';
  };

  return (
    <div className="full-bleed-page credit-monitoring-dashboard">
      <div className="dashboard-header mb-6">
        <h1>Credit Monitoring & Optimization</h1>
        <p className="subtitle">Phase 12: Credit Score Monitoring & Improvement</p>
      </div>

      <div className="scrollable-content-wrapper">
        <ResponsiveGridLayout
          className="layout"
          layouts={DEFAULT_LAYOUT}
          breakpoints={{ lg: 1200, md: 996, sm: 768, xs: 480, xxs: 0 }}
          cols={{ lg: 12, md: 10, sm: 6, xs: 4, xxs: 2 }}
          rowHeight={80}
          isDraggable={true}
          isResizable={true}
          draggableHandle="h2"
          margin={[16, 16]}
        >
          {/* Credit Score */}
          <div key="score" className="score-panel glass-panel">
            <h2>Credit Score</h2>
            <div className="score-display flex flex-col items-center justify-center p-6">
              <div className="score-value text-6xl font-black mb-2" style={{ color: getScoreColor(creditScore.score) }}>
                {creditScore.score}
              </div>
              <div className="score-category text-xl font-bold text-white/80">{getScoreCategory(creditScore.score)}</div>
              <div className="score-trend mt-4 text-sm font-mono">
                {creditScore.trend && (
                  <span className={`trend px-3 py-1 rounded bg-white/5 border border-white/10 ${creditScore.trend}`}>
                    {creditScore.trend === 'up' ? '↑' : creditScore.trend === 'down' ? '↓' : '→'} 
                    {creditScore.change && ` ${Math.abs(creditScore.change)} pt improvements`}
                  </span>
                )}
              </div>
            </div>
          </div>

          {/* Credit Report Summary */}
          <div key="report" className="report-panel glass-panel">
            <h2>Credit Report Summary</h2>
            <div className="report-metrics grid grid-cols-2 md:grid-cols-4 gap-4 p-6">
              <div className="metric-card bg-white/5 p-4 rounded-xl border border-white/5">
                <div className="metric-label text-[10px] text-zinc-500 uppercase font-black mb-1">Accounts</div>
                <div className="metric-value text-2xl font-bold text-white">{creditReport.total_accounts || 0}</div>
              </div>
              <div className="metric-card bg-white/5 p-4 rounded-xl border border-white/5">
                <div className="metric-label text-[10px] text-zinc-500 uppercase font-black mb-1">Utilization</div>
                <div className="metric-value text-2xl font-bold text-white">{(creditReport.credit_utilization * 100 || 0).toFixed(1)}%</div>
              </div>
              <div className="metric-card bg-white/5 p-4 rounded-xl border border-white/5">
                <div className="metric-label text-[10px] text-zinc-500 uppercase font-black mb-1">History</div>
                <div className="metric-value text-2xl font-bold text-white">{(creditReport.payment_history_percent || 0).toFixed(0)}%</div>
              </div>
              <div className="metric-card bg-white/5 p-4 rounded-xl border border-white/5">
                <div className="metric-label text-[10px] text-zinc-500 uppercase font-black mb-1">Credit Age</div>
                <div className="metric-value text-2xl font-bold text-white">{creditReport.credit_age_months || 0} mo</div>
              </div>
            </div>
          </div>

          {/* Recommendations */}
          <div key="recommendations" className="recommendations-panel glass-panel overflow-y-auto scrollbar-hide">
            <h2>Improvement Logic</h2>
            <div className="recommendations-list p-4 space-y-4">
              {recommendations.map((rec, idx) => (
                <div key={idx} className="recommendation-card bg-white/5 p-4 rounded-xl border border-white/5 hover:border-blue-500/30 transition-all">
                  <div className="rec-header flex justify-between items-start mb-2">
                    <h3 className="text-sm font-bold text-white">{rec.title}</h3>
                    <span className="impact-badge text-[10px] bg-emerald-950/30 text-emerald-400 px-2 py-1 rounded border border-emerald-500/20">
                      +{rec.estimated_score_impact} pts
                    </span>
                  </div>
                  <p className="rec-description text-xs text-zinc-500 mb-3">{rec.description}</p>
                  <div className="rec-priority text-[9px] font-mono text-zinc-600 uppercase">Priority: {rec.priority}</div>
                </div>
              ))}
            </div>
          </div>

          {/* Score Simulation */}
          <div key="simulation" className="simulation-panel glass-panel">
            <h2>Scenario Simulator</h2>
            <div className="simulation-actions p-6 flex flex-col gap-3">
              <button
                onClick={() => runSimulation('pay_off_credit_card')}
                disabled={loading}
                className="sim-button bg-blue-600 hover:bg-blue-500 text-white rounded-lg py-3 font-bold transition-all disabled:opacity-50"
              >
                Simulate: Pay Off Credit Cards
              </button>
              <button
                onClick={() => runSimulation('reduce_utilization')}
                disabled={loading}
                className="sim-button bg-zinc-800 hover:bg-zinc-700 text-white rounded-lg py-3 font-bold transition-all disabled:opacity-50"
              >
                Simulate: Reduce Utilization
              </button>
              
              {simulationResult && (
                <div className="simulation-results mt-6 p-4 bg-emerald-950/20 border border-emerald-500/20 rounded-xl animate-in fade-in slide-in-from-bottom-2">
                  <div className="sim-metric flex justify-between mb-2">
                    <span className="label text-xs text-zinc-500">Current Score:</span>
                    <span className="value text-xs text-white">{simulationResult.current_score}</span>
                  </div>
                  <div className="sim-metric flex justify-between mb-2">
                    <span className="label text-xs text-zinc-500">Projected Score:</span>
                    <span className="value text-sm font-bold" style={{ color: getScoreColor(simulationResult.projected_score) }}>
                      {simulationResult.projected_score}
                    </span>
                  </div>
                  <div className="sim-metric flex justify-between pt-2 border-t border-white/5">
                    <span className="label text-xs text-zinc-500">Score Change:</span>
                    <span className="value text-sm font-black" style={{ color: simulationResult.score_change >= 0 ? '#00ff88' : '#ff4444' }}>
                      {simulationResult.score_change >= 0 ? '+' : ''}{simulationResult.score_change} points
                    </span>
                  </div>
                </div>
              )}
            </div>
          </div>
        </ResponsiveGridLayout>
        
        {/* Bottom Buffer */}
        <div className="scroll-buffer-100" />
      </div>
    </div>
  );
};
        {/* Credit Score */}
        {creditScore && (
          <div className="score-panel">
            <h2>Credit Score</h2>
            <div className="score-display">
              <div className="score-value" style={{ color: getScoreColor(creditScore.score) }}>
                {creditScore.score}
              </div>
              <div className="score-category">{getScoreCategory(creditScore.score)}</div>
              <div className="score-trend">
                {creditScore.trend && (
                  <span className={`trend ${creditScore.trend}`}>
                    {creditScore.trend === 'up' ? '↑' : creditScore.trend === 'down' ? '↓' : '→'} 
                    {creditScore.change && `${Math.abs(creditScore.change)} points`}
                  </span>
                )}
              </div>
            </div>
            <div className="score-details">
              <div className="detail-item">
                <span className="label">Bureau:</span>
                <span className="value">{creditScore.bureau || 'N/A'}</span>
              </div>
              <div className="detail-item">
                <span className="label">Last Updated:</span>
                <span className="value">
                  {new Date(creditScore.last_updated).toLocaleDateString()}
                </span>
              </div>
            </div>
          </div>
        )}

        {/* Credit Report Summary */}
        {creditReport && (
          <div className="report-panel">
            <h2>Credit Report Summary</h2>
            <div className="report-metrics">
              <div className="metric-card">
                <div className="metric-label">Accounts</div>
                <div className="metric-value">{creditReport.total_accounts || 0}</div>
              </div>
              <div className="metric-card">
                <div className="metric-label">Credit Utilization</div>
                <div className="metric-value">{(creditReport.credit_utilization * 100 || 0).toFixed(1)}%</div>
              </div>
              <div className="metric-card">
                <div className="metric-label">Payment History</div>
                <div className="metric-value">{(creditReport.payment_history_percent || 0).toFixed(0)}%</div>
              </div>
              <div className="metric-card">
                <div className="metric-label">Age of Credit</div>
                <div className="metric-value">{creditReport.credit_age_months || 0} months</div>
              </div>
            </div>
          </div>
        )}

        {/* Recommendations */}
        <div className="recommendations-panel">
          <h2>Improvement Recommendations</h2>
          {recommendations.length > 0 ? (
            <div className="recommendations-list">
              {recommendations.map((rec, idx) => (
                <div key={idx} className="recommendation-card">
                  <div className="rec-header">
                    <h3>{rec.title}</h3>
                    <span className="impact-badge">
                      +{rec.estimated_score_impact} points
                    </span>
                  </div>
                  <p className="rec-description">{rec.description}</p>
                  <div className="rec-priority">Priority: {rec.priority}</div>
                </div>
              ))}
            </div>
          ) : (
            <div className="no-data">No recommendations available</div>
          )}
        </div>

        {/* Score Simulation */}
        <div className="simulation-panel">
          <h2>Score Simulator</h2>
          <div className="simulation-actions">
            <button
              onClick={() => runSimulation('pay_off_credit_card')}
              disabled={loading}
              className="sim-button"
            >
              Pay Off Credit Card
            </button>
            <button
              onClick={() => runSimulation('reduce_utilization')}
              disabled={loading}
              className="sim-button"
            >
              Reduce Utilization
            </button>
            <button
              onClick={() => runSimulation('pay_off_loan')}
              disabled={loading}
              className="sim-button"
            >
              Pay Off Loan
            </button>
          </div>
          {simulationResult && (
            <div className="simulation-results">
              <div className="sim-metric">
                <span className="label">Current Score:</span>
                <span className="value">{simulationResult.current_score}</span>
              </div>
              <div className="sim-metric">
                <span className="label">Projected Score:</span>
                <span className="value" style={{ color: getScoreColor(simulationResult.projected_score) }}>
                  {simulationResult.projected_score}
                </span>
              </div>
              <div className="sim-metric">
                <span className="label">Score Change:</span>
                <span className="value" style={{ color: simulationResult.score_change >= 0 ? '#00ff88' : '#ff4444' }}>
                  {simulationResult.score_change >= 0 ? '+' : ''}{simulationResult.score_change} points
                </span>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default CreditMonitoringDashboard;
