import React from 'react';
import './InflationMatrix.css';
import apiClient from '../../services/apiClient';

const InflationMatrix = () => {
    const [assets, setAssets] = React.useState(null);
    const [correlations, setCorrelations] = React.useState(null);

    React.useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await apiClient.get('/macro/correlations');
                const result = response.data;
                if (result.success) {
                    setAssets(result.data.assets);
                    // Transform api dict to matrix array for rendering
                    const matrix = result.data.assets.map(rowAsset => 
                        result.data.assets.map(colAsset => 
                            result.data.correlations[rowAsset][colAsset]
                        )
                    );
                    setCorrelations(matrix);
                }
            } catch (err) {
                console.error("Failed to fetch correlations:", err);
            }
        };
        fetchData();
    }, []);

    if (!assets || !correlations) return <div className="p-4 text-center text-slate-500">Loading correlation matrix...</div>;

    const getColor = (val) => {
        if (val === 1) return '#333'; // Self
        if (val > 0) return `rgba(76, 175, 80, ${val})`; // Green for positive
        return `rgba(244, 67, 54, ${Math.abs(val)})`; // Red for negative
    };

    return (
        <div className="inflation-matrix-widget">
            <h3>Inflation-Sensitive Correlations</h3>
            <div className="matrix-grid" style={{ gridTemplateColumns: `repeat(${assets.length + 1}, 1fr)` }}>
                <div className="matrix-header-cell"></div>
                {assets.map(a => <div key={a} className="matrix-header-cell">{a}</div>)}
                
                {assets.map((rowAsset, i) => (
                    <React.Fragment key={rowAsset}>
                        <div className="matrix-row-label">{rowAsset}</div>
                        {correlations[i].map((val, j) => (
                            <div 
                                key={`${rowAsset}-${assets[j]}`} 
                                className="matrix-cell"
                                style={{ backgroundColor: getColor(val) }}
                                title={`${rowAsset} vs ${assets[j]}: ${val}`}
                            >
                                {val !== 1 ? val.toFixed(1) : ''}
                            </div>
                        ))}
                    </React.Fragment>
                ))}
            </div>
        </div>
    );
};

export default InflationMatrix;
