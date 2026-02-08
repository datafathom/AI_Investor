import React from 'react';
import './LatencyHistogram.css';

const LatencyHistogram = ({ data }) => {
    const maxCount = Math.max(...data.map(d => d.count), 1);

    return (
        <div className="latency-histogram">
            {data.map((bucket, i) => (
                <div key={i} className="histogram-bar-group">
                    <div className="bar-wrapper">
                        <div 
                            className="bar" 
                            style={{ height: `${(bucket.count / maxCount) * 100}%` }}
                        >
                            {bucket.count > 0 && <span className="bar-label">{bucket.count}</span>}
                        </div>
                    </div>
                    <span className="bucket-range">{bucket.range}</span>
                </div>
            ))}
        </div>
    );
};

export default LatencyHistogram;
