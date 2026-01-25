import React from 'react';
import './NewsTicker.css'; // Will assume marquee animation

const NewsTicker = ({ isWidget = false }) => {
    const headlines = [
        "BREAKING: Senate passes AI Safety Bill (S. 5521) with 88-12 vote.",
        "INSIDER ALERT: Speaker Johnson discloses $2M purchase of Lockheed Martin calls.",
        "REGULATION: SEC proposes new crypto custody rules impacting Coinbase and Kraken.",
        "MONEY FLOW: Energy sector lobbying hits record $500M in Q1 2026.",
        "POLL: 65% of Americans favor ban on congressional stock trading."
    ];

    const containerStyle = isWidget 
        ? "relative w-full h-full overflow-hidden flex items-center"
        : "fixed bottom-0 left-0 w-full h-8 bg-amber-950/80 border-t border-amber-500/30 flex items-center overflow-hidden z-40 backdrop-blur-md";

    return (
        <div className={containerStyle}>
            <div className="px-4 py-1 bg-amber-600 text-black font-bold text-[10px] uppercase tracking-widest h-full flex items-center z-10 shadow-lg">
                CQ WIRE
            </div>
            <div className="flex-1 overflow-hidden relative h-full flex items-center">
                <div className="absolute whitespace-nowrap animate-marquee flex items-center h-full">
                    {headlines.map((item, i) => (
                        <span key={i} className="mx-12 text-2xl font-black font-mono text-amber-100 whitespace-nowrap inline-flex items-center gap-4">
                            <span className="text-amber-500 text-lg">///</span> {item}
                        </span>
                    ))}
                    {headlines.map((item, i) => (
                        <span key={`dup-${i}`} className="mx-12 text-2xl font-black font-mono text-amber-100 whitespace-nowrap inline-flex items-center gap-4">
                            <span className="text-amber-500 text-lg">///</span> {item}
                        </span>
                    ))}
                </div>
            </div>
            <style>
                {`
                @keyframes marquee {
                    0% { transform: translateX(0); }
                    100% { transform: translateX(-50%); }
                }
                .animate-marquee {
                    animation: marquee 30s linear infinite;
                }
                `}
            </style>
        </div>
    );
};

export default NewsTicker;
