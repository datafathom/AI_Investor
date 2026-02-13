import React from 'react';

const MessageFlowChart = ({ stats }) => {
    // In a real app, we'd use Chart.js or D3.
    // For now, a simplified visualization of throughput.
    const totalMsgs = Object.values(stats).reduce((acc, s) => acc + (s.publish_count || 0), 0);
    
    return (
        <div className="flow-chart-container">
            <h3 className="section-title">THROUGHPUT_VISUALIZATION (PULSE)</h3>
            <div className="placeholder-chart">
                <div className="pulse-text">SYSTEM_WIDE_ACTIVITY: {totalMsgs} EVENTS_REGISTERED</div>
                <div className="visual-bars">
                    {Object.entries(stats).slice(0, 15).map(([topic, s]) => (
                        <div key={topic} className="bar-wrapper">
                            <div 
                                className="bar" 
                                style={{ 
                                    height: `${Math.min(100, (s.publish_count || 0) / 10)}%`,
                                    background: '#00f2ff' 
                                }}
                            ></div>
                        </div>
                    ))}
                </div>
            </div>
            <style jsx="true">{`
                .flow-chart-container {
                    display: flex;
                    flex-direction: column;
                    height: 100%;
                }
                .section-title {
                    font-size: 0.9rem;
                    color: #888;
                    margin-bottom: 10px;
                }
                .placeholder-chart {
                    flex: 1;
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                    background: #000;
                    border: 1px inset #111;
                    position: relative;
                    overflow: hidden;
                }
                .pulse-text {
                    color: #00f2ff;
                    font-size: 0.8rem;
                    z-index: 2;
                }
                .visual-bars {
                    position: absolute;
                    bottom: 0;
                    left: 0;
                    right: 0;
                    display: flex;
                    gap: 5px;
                    height: 100%;
                    align-items: flex-end;
                    padding: 0 10px;
                    opacity: 0.2;
                }
                .bar-wrapper {
                    flex: 1;
                    height: 100%;
                    display: flex;
                    align-items: flex-end;
                }
                .bar {
                    width: 100%;
                    transition: height 0.5s ease;
                }
            `}</style>
        </div>
    );
};

export default MessageFlowChart;
