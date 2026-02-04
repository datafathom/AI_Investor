import React, { useState } from 'react';
import { ChevronDown } from 'lucide-react';

const GlassCard = ({ children, className = '', title = '', subTitle = '', collapsible = false }) => {
    const [isOpen, setIsOpen] = useState(true);

    return (
        <div className={`glass-card ${className}`}>
            {(title || subTitle) && (
                <div
                    className={`flex justify-between items-start mb-6 ${collapsible ? 'cursor-pointer' : ''}`}
                    onClick={() => collapsible && setIsOpen(!isOpen)}
                >
                    <div>
                        {title && <h3 className="neon-text text-lg">{title}</h3>}
                        {subTitle && <p className="text-dim text-xs mt-1">{subTitle}</p>}
                    </div>
                    {collapsible && (
                        <div className={`transition-transform duration-300 ${isOpen ? 'rotate-180' : ''}`}>
                            <ChevronDown size={20} className="text-cyan-500" />
                        </div>
                    )}
                </div>
            )}
            <div className={`transition-all duration-300 overflow-hidden ${isOpen ? 'opacity-100 max-h-[1000px]' : 'opacity-0 max-h-0'}`}>
                {children}
            </div>
        </div>
    );
};

export default GlassCard;
