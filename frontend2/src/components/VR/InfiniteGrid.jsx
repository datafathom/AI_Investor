import React from 'react';
import './InfiniteGrid.css'; // We'll add some inline style or assume global CSS

const InfiniteGrid = () => {
    return (
        <div className="absolute inset-0 overflow-hidden bg-black z-0 perspective-[1000px]">
            {/* Horizon Glow */}
            <div className="absolute top-0 w-full h-1/2 bg-gradient-to-b from-black via-[#000000] to-[#0c4a6e] z-0"></div>

            {/* Grid Floor */}
            <div
                className="absolute bottom-0 w-[200%] h-[200%] -left-1/2 bg-[linear-gradient(rgba(6,182,212,0.3)_1px,transparent_1px),linear-gradient(90deg,rgba(6,182,212,0.3)_1px,transparent_1px)] bg-[size:40px_40px] transform-style-3d rotate-x-60 animate-grid-move"
                style={{
                    transformOrigin: '50% 100%',
                    transform: 'perspective(500px) rotateX(60deg) translateY(0)',
                    animation: 'gridMove 2s linear infinite'
                }}
            ></div>

            <style jsx>{`
                @keyframes gridMove {
                    0% { background-position: 0 0; }
                    100% { background-position: 0 40px; }
                }
            `}</style>
        </div>
    );
};

export default InfiniteGrid;
