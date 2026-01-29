import React, { useEffect } from 'react';
import { User, Users, FileText, AlertTriangle, Loader2 } from 'lucide-react';
import useEstateStore from '../../stores/estateStore';
import './BeneficiaryMap.css';

const BeneficiaryMap = () => {
    const { 
        beneficiaries, 
        isLoading, 
        fetchEstateData, 
        updateAllocation 
    } = useEstateStore();

    useEffect(() => {
        fetchEstateData();
    }, [fetchEstateData]);

    const totalAllocation = (beneficiaries || []).reduce((sum, b) => sum + b.allocation_percent, 0);

    const handleAllocationChange = (id, val) => {
        const percent = Math.min(100, Math.max(0, parseInt(val) || 0));
        updateAllocation(id, percent);
    };

    // Mock estate value for tax simulation
    const grossEstateValue = 25400000;
    const federalExemption = 12920000;
    const estTax = grossEstateValue > federalExemption 
        ? (grossEstateValue - federalExemption) * 0.4 
        : 0;

    if (isLoading && (beneficiaries || []).length === 0) {
        return (
            <div className="beneficiary-map-widget loading">
                <Loader2 className="animate-spin" />
                <span>Syncing Beneficiaries...</span>
            </div>
        );
    }

    return (
        <div className="beneficiary-map-widget">
            <div className="widget-header">
                <h3><Users size={18} /> Beneficiary Asset Allocation</h3>
                <div className={`allocation-status ${totalAllocation === 100 ? 'valid' : 'invalid'}`}>
                    Total: {totalAllocation}%
                </div>
            </div>

            <div className="beneficiary-list">
                {(beneficiaries || []).map(ben => (
                    <div key={ben.id} className="beneficiary-node">
                        <div className="node-icon">
                            {ben.relationship === 'Trust' ? <FileText size={20} /> : <User size={20} />}
                        </div>
                        <div className="node-details">
                            <span className="node-name">{ben.name}</span>
                            <span className="node-type">{ben.relationship}</span>
                        </div>
                        <div className="node-allocation">
                            <input 
                                type="number" 
                                value={ben.allocation_percent} 
                                onChange={(e) => handleAllocationChange(ben.id, e.target.value)}
                            />
                            <span className="percent">%</span>
                        </div>
                        <div className="node-docs">
                            {ben.contact_email ? 
                                <span className="doc-link text-green-400" title="Contact Verified"><FileText size={14}/></span> : 
                                <span className="doc-warning text-amber-500" title="Missing Contact"><AlertTriangle size={14}/></span>
                            }
                        </div>
                    </div>
                ))}
            </div>

            <div className="tax-impact-simulation">
                <h4><FileText size={14} /> Estimated Estate Tax Impact</h4>
                <div className="impact-row">
                    <span>Gross Estate Value:</span>
                    <span className="val">${grossEstateValue.toLocaleString()}</span>
                </div>
                <div className="impact-row">
                    <span>Federal Exemption:</span>
                    <span className="val">(${(federalExemption).toLocaleString()})</span>
                </div>
                <div className="impact-row total">
                    <span>Est. Federal Tax:</span>
                    <span className={`val ${estTax > 0 ? 'text-red-400' : 'text-green-400'}`}>
                        ${estTax.toLocaleString()}
                    </span>
                </div>
            </div>
        </div>
    );
};

export default BeneficiaryMap;
