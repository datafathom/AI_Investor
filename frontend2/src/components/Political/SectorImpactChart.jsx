
import React from 'react';

/**
 * SectorImpactChart Component
 * Simplified CSS-based bar chart for maximum rendering stability.
 * Bypasses Recharts ResponsiveContainer issues.
 */
const SectorImpactChart = () => {
    const data = [
        { name: 'TECH', value: '85%', bias: 'BEARISH', label: 'Heavy Regulation' },
        { name: 'ENERGY', value: '65%', bias: 'BULLISH', label: 'Subsidy Growth' },
        { name: 'HEALTH', value: '45%', bias: 'BEARISH', label: 'Price Caps' },
        { name: 'FINANCE', value: '90%', bias: 'BEARISH', label: 'Rate Pressure' },
        { name: 'DEFENSE', value: '75%', bias: 'BULLISH', label: 'Spend Increase' },
    ];

    return (
        <div className="h-full w-full flex flex-col justify-center gap-4 py-4" style={{ minHeight: '200px', padding: '16px' }}>
            {data.map((item) => (
                <div key={item.name} style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', fontSize: '10px', fontFamily: 'monospace', fontWeight: 'bold' }}>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                            <span style={{ 
                                color: item.bias === 'BULLISH' ? '#10b981' : '#ef4444',
                                background: item.bias === 'BULLISH' ? 'rgba(16, 185, 129, 0.1)' : 'rgba(239, 68, 68, 0.1)',
                                padding: '2px 6px',
                                borderRadius: '4px',
                                fontSize: '9px',
                                border: `1px solid ${item.bias === 'BULLISH' ? 'rgba(16, 185, 129, 0.2)' : 'rgba(239, 68, 68, 0.2)'}`
                            }}>
                                {item.bias}
                            </span>
                            <span style={{ color: '#f8fafc', letterSpacing: '0.05em' }}>{item.name}</span>
                        </div>
                        <span style={{ color: '#64748b', fontStyle: 'italic', fontSize: '9px' }}>{item.label}</span>
                    </div>
                    <div style={{ height: '8px', width: '100%', backgroundColor: '#0f172a', borderRadius: '4px', overflow: 'hidden', border: '1px solid rgba(255,255,255,0.05)' }}>
                        <div 
                            style={{ 
                                height: '100%', 
                                width: item.value, 
                                backgroundColor: item.bias === 'BULLISH' ? '#10b981' : '#ef4444',
                                transition: 'width 1s ease-out',
                                boxShadow: `0 0 10px ${item.bias === 'BULLISH' ? 'rgba(16, 185, 129, 0.4)' : 'rgba(239, 68, 68, 0.4)'}`
                            }}
                        />
                    </div>
                </div>
            ))}
            <div style={{ marginTop: '16px', paddingTop: '12px', borderTop: '1px solid rgba(255,255,255,0.05)', display: 'flex', justifyContent: 'space-between', fontSize: '10px', fontFamily: 'monospace' }}>
                <div style={{ display: 'flex', gap: '12px' }}>
                    <span style={{ color: '#10b981' }}>▲ BULLISH</span>
                    <span style={{ color: '#ef4444' }}>▼ BEARISH</span>
                </div>
                <span style={{ color: '#64748b', opacity: 0.5 }}>V4.0_STABLE</span>
            </div>
        </div>
    );
};

export default SectorImpactChart;
