import React, { useEffect, useState } from 'react';
import { 
    User, 
    Shield, 
    CreditCard, 
    PieChart, 
    CheckCircle, 
    ChevronRight, 
    ChevronLeft,
    Search,
    Download,
    FileText,
    ExternalLink
} from 'lucide-react';
import './OnboardingWizard.css';
import useInstitutionalStore from '../../stores/institutionalStore';
import AssetAllocationWheel from './AssetAllocationWheel';
import KycRiskGauge from './KycRiskGauge';

const AdvisorOnboardingWizard = () => {
    const { 
        onboardingStep, 
        setOnboardingStep, 
        onboardingData,
        updateOnboardingData,
        createClient, 
        resetOnboarding 
    } = useInstitutionalStore();

    const [isProcessing, setIsProcessing] = useState(false);

    const steps = [
        { id: 1, name: 'Identity', icon: User, description: 'Client Profiles' },
        { id: 2, name: 'KYC', icon: Shield, description: 'AML Screening' },
        { id: 3, name: 'Funding', icon: CreditCard, description: 'Bank Tether' },
        { id: 4, name: 'Allocation', icon: PieChart, description: 'Strategy Tilt' },
        { id: 5, name: 'Approval', icon: CheckCircle, description: 'Final Audit' },
    ];

    const handleNext = () => setOnboardingStep(Math.min(onboardingStep + 1, 5));
    const handleBack = () => setOnboardingStep(Math.max(onboardingStep - 1, 1));

    const handleFinalSubmit = async () => {
        setIsProcessing(true);
        // Simulate a slight delay for "Blockchain Writing" / "Vault Storage"
        setTimeout(async () => {
            await createClient({
                client_name: onboardingData.clientName,
                jurisdiction: onboardingData.jurisdiction,
                funding_source: onboardingData.fundingSource,
                strategy: onboardingData.strategy
            });
            setOnboardingStep(5);
            setIsProcessing(false);
        }, 1500);
    };

    const renderStepContent = () => {
        switch (onboardingStep) {
            case 1:
                return (
                    <div className="wizard-step-container animate-in slide-in-from-right-4 duration-300">
                        <div className="flex items-center gap-4 mb-6">
                            <div className="w-12 h-12 rounded-xl bg-primary/20 flex items-center justify-center text-primary border border-primary/30">
                                <User size={24} />
                            </div>
                            <div>
                                <h3 className="text-2xl font-black tracking-tight text-white uppercase italic">Institutional Identity</h3>
                                <p className="text-xs text-slate-500 font-mono tracking-widest uppercase">Phase 33 / Identity Bridge</p>
                            </div>
                        </div>
                        
                        <div className="space-y-6">
                            <div className="group">
                                <label className="block text-[10px] font-black uppercase tracking-[0.2em] text-slate-500 mb-2 group-focus-within:text-primary transition-colors">Legal Client Name</label>
                                <input 
                                    type="text" 
                                    className="w-full bg-white/5 border border-white/10 rounded-xl p-4 text-white font-bold placeholder:text-slate-600 focus:border-primary/50 focus:ring-1 focus:ring-primary/30 transition-all outline-none" 
                                    placeholder="e.g. BlackRock Global / Silver Lake Trust"
                                    value={onboardingData.clientName}
                                    onChange={(e) => updateOnboardingData({ clientName: e.target.value })}
                                />
                            </div>
                            
                            <div className="grid grid-cols-2 gap-4">
                                <div className="group">
                                    <label className="block text-[10px] font-black uppercase tracking-[0.2em] text-slate-500 mb-2">Entity Type</label>
                                    <select className="w-full bg-white/5 border border-white/10 rounded-xl p-4 text-white font-bold outline-none">
                                        <option>Family Office</option>
                                        <option>Pension Fund</option>
                                        <option>Endowment</option>
                                        <option>Ultra-HNW Individual</option>
                                    </select>
                                </div>
                                <div className="group">
                                    <label className="block text-[10px] font-black uppercase tracking-[0.2em] text-slate-500 mb-2">Primary Jurisdiction</label>
                                    <select 
                                        className="w-full bg-white/5 border border-white/10 rounded-xl p-4 text-white font-bold outline-none"
                                        value={onboardingData.jurisdiction}
                                        onChange={(e) => updateOnboardingData({ jurisdiction: e.target.value })}
                                    >
                                        <option value="US">United States (SEC/FINRA)</option>
                                        <option value="UK">United Kingdom (FCA)</option>
                                        <option value="EU">European Union (ESMA)</option>
                                        <option value="CH">Switzerland (FINMA)</option>
                                    </select>
                                </div>
                            </div>
                        </div>
                    </div>
                );
            case 2:
                return (
                    <div className="wizard-step-container animate-in slide-in-from-right-4 duration-300">
                        <div className="flex items-center gap-4 mb-6">
                            <div className="w-12 h-12 rounded-xl bg-success/20 flex items-center justify-center text-success border border-success/30">
                                <Shield size={24} />
                            </div>
                            <div>
                                <h3 className="text-2xl font-black tracking-tight text-white uppercase italic">Compliance Architecture</h3>
                                <p className="text-xs text-slate-500 font-mono tracking-widest uppercase">Institutional AML/KYC Sweep</p>
                            </div>
                        </div>
                        
                        <div className="grid grid-cols-[1fr_200px] gap-6 items-center">
                            <div className="space-y-4">
                                <div className="p-4 rounded-2xl bg-white/5 border border-white/10 space-y-3">
                                    <div className="flex justify-between items-center">
                                        <span className="text-xs font-bold text-slate-400 capitalize">Global Sanctions List</span>
                                        <span className="text-[10px] font-black text-success uppercase">Clear</span>
                                    </div>
                                    <div className="flex justify-between items-center">
                                        <span className="text-xs font-bold text-slate-400 capitalize">PEP Identification</span>
                                        <span className="text-[10px] font-black text-success uppercase">Negative</span>
                                    </div>
                                    <div className="flex justify-between items-center">
                                        <span className="text-xs font-bold text-slate-400 capitalize">Media Screening</span>
                                        <span className="text-[10px] font-black text-warning uppercase">Neutral</span>
                                    </div>
                                    <div className="h-1.5 w-full bg-white/5 rounded-full overflow-hidden">
                                        <div className="h-full bg-success w-[85%] animate-pulse" />
                                    </div>
                                </div>
                                <p className="text-[10px] leading-relaxed text-slate-500 font-mono uppercase">
                                    Performing real-time audit across 240+ global regulatory databases for <span className="text-white">{onboardingData.clientName}</span>.
                                </p>
                            </div>
                            <div className="scale-75 origin-right">
                                <KycRiskGauge status="Pending" />
                            </div>
                        </div>
                    </div>
                );
            case 3:
                return (
                    <div className="wizard-step-container animate-in slide-in-from-right-4 duration-300">
                        <div className="flex items-center gap-4 mb-6">
                            <div className="w-12 h-12 rounded-xl bg-info/20 flex items-center justify-center text-info border border-info/30">
                                <CreditCard size={24} />
                            </div>
                            <div>
                                <h3 className="text-2xl font-black tracking-tight text-white uppercase italic">Capital Infrastructure</h3>
                                <p className="text-xs text-slate-500 font-mono tracking-widest uppercase">Multi-Tether Funding Flow</p>
                            </div>
                        </div>
                        
                        <div className="grid grid-cols-2 gap-4 mb-6">
                            <button 
                                onClick={() => updateOnboardingData({ fundingSource: 'Plaid' })}
                                className={`p-6 rounded-2xl border transition-all flex flex-col items-center gap-3 relative overflow-hidden ${
                                    onboardingData.fundingSource === 'Plaid' 
                                    ? 'bg-primary/20 border-primary shadow-[0_0_20px_rgba(var(--primary-h),0.2)]' 
                                    : 'bg-white/5 border-white/10 hover:bg-white/10'
                                }`}
                            >
                                <div className="text-2xl font-black text-white italic tracking-tighter">PLAID</div>
                                <span className="text-[10px] font-black text-slate-500 uppercase">Institutional Connect</span>
                                {onboardingData.fundingSource === 'Plaid' && (
                                    <div className="absolute top-2 right-2 text-primary font-black"><CheckCircle size={14} /></div>
                                )}
                            </button>
                            
                            <button 
                                onClick={() => updateOnboardingData({ fundingSource: 'Swift' })}
                                className={`p-6 rounded-2xl border transition-all flex flex-col items-center gap-3 relative overflow-hidden ${
                                    onboardingData.fundingSource === 'Swift' 
                                    ? 'bg-success/20 border-success shadow-[0_0_20px_rgba(var(--success-h),0.2)]' 
                                    : 'bg-white/5 border-white/10 hover:bg-white/10'
                                }`}
                            >
                                <div className="text-2xl font-black text-white italic tracking-tighter">SWIFT/IBAN</div>
                                <span className="text-[10px] font-black text-slate-500 uppercase">Legacy Wire Direct</span>
                                {onboardingData.fundingSource === 'Swift' && (
                                    <div className="absolute top-2 right-2 text-success font-black"><CheckCircle size={14} /></div>
                                )}
                            </button>
                        </div>
                        
                        <div className="p-4 rounded-xl bg-white/5 border border-white/5 flex items-center gap-4">
                            <div className="p-2 rounded-lg bg-white/10 text-slate-400"><Search size={16} /></div>
                            <span className="text-xs text-slate-500 italic">Waiting for secure handshake signature via hardware bridge...</span>
                        </div>
                    </div>
                );
            case 4:
                return (
                    <div className="wizard-step-container animate-in slide-in-from-right-4 duration-300">
                        <div className="flex items-center gap-4 mb-6">
                            <div className="w-12 h-12 rounded-xl bg-warning/20 flex items-center justify-center text-warning border border-warning/30">
                                <PieChart size={24} />
                            </div>
                            <div>
                                <h3 className="text-2xl font-black tracking-tight text-white uppercase italic">Strategic Deployment</h3>
                                <p className="text-xs text-slate-500 font-mono tracking-widest uppercase">AI Agent Gene Splicing</p>
                            </div>
                        </div>
                        
                        <div className="grid grid-cols-[1fr_250px] gap-8">
                            <div className="space-y-4">
                                <label className="block text-[10px] font-black uppercase tracking-[0.2em] text-slate-500">Core Logic Engine</label>
                                <div className="space-y-2">
                                    {['Aggressive AI', 'Balanced Zen', 'Capital Preservation', 'Volatility Harvester'].map((strat) => (
                                        <button 
                                            key={strat}
                                            onClick={() => updateOnboardingData({ strategy: strat })}
                                            className={`w-full p-4 rounded-xl border text-left flex justify-between items-center transition-all ${
                                                onboardingData.strategy === strat 
                                                ? 'bg-primary/20 border-primary text-white shadow-lg' 
                                                : 'bg-white/5 border-white/5 text-slate-400 hover:bg-white/10'
                                            }`}
                                        >
                                            <span className="font-bold text-sm tracking-tight capitalize">{strat}</span>
                                            {onboardingData.strategy === strat && <div className="w-2 h-2 rounded-full bg-primary shadow-[0_0_8px_white]" />}
                                        </button>
                                    ))}
                                </div>
                            </div>
                            <div className="scale-90 origin-top">
                                <AssetAllocationWheel />
                                <div className="mt-4 p-3 rounded-lg bg-white/5 border border-white/5 text-center">
                                    <span className="text-[10px] font-black text-slate-500 uppercase tracking-widest">Expected Yield: <span className="text-white">12.4% ARR</span></span>
                                </div>
                            </div>
                        </div>
                    </div>
                );
            case 5:
                return (
                    <div className="wizard-step-container animate-in zoom-in-95 duration-500 text-center py-8">
                        <div className="relative inline-block mb-8">
                            <div className="w-24 h-24 bg-success/10 rounded-full flex items-center justify-center text-success border-2 border-success/30 animate-pulse">
                                <CheckCircle size={48} />
                            </div>
                            <div className="absolute -top-2 -right-2 bg-success text-white text-[10px] font-black px-2 py-1 rounded-md shadow-xl">SIGNED</div>
                        </div>
                        
                        <h3 className="text-4xl font-black tracking-tighter text-white uppercase italic mb-2">Institutional Genesis</h3>
                        <p className="text-slate-400 text-sm max-w-md mx-auto mb-8 font-medium">
                            Legal entity logic has been persisted to the systemic graph. Client onboarded for <span className="text-success font-black tracking-widest uppercase">${(5000000).toLocaleString()}+</span> initial AUM.
                        </p>
                        
                        <div className="flex flex-col gap-3 max-w-sm mx-auto">
                            <button 
                                onClick={handleFinalSubmit}
                                className="w-full bg-success hover:bg-success-light text-white p-4 rounded-2xl font-black tracking-widest uppercase shadow-[0_0_30px_rgba(var(--success-h),0.4)] transition-all flex items-center justify-center gap-3"
                            >
                                {isProcessing ? (
                                    <>WRITING TO VAULT...</>
                                ) : (
                                    <>GENERATE ENGAGEMENT PDF <Download size={18} /></>
                                )}
                            </button>
                            <button 
                                onClick={resetOnboarding}
                                className="w-full bg-white/5 hover:bg-white/10 text-slate-400 p-4 rounded-2xl font-bold tracking-widest uppercase border border-white/5 transition-all text-xs"
                            >
                                EXPLORE ROSTER <ExternalLink size={14} className="inline ml-1 opacity-50" />
                            </button>
                        </div>
                    </div>
                );
            default:
                return null;
        }
    };

    return (
        <div className="advisor-onboarding-wizard glass-premium p-10 rounded-[2.5rem] border border-white/10 max-w-4xl mx-auto shadow-2xl relative overflow-hidden">
            {/* Background Glow */}
            <div className="absolute -top-24 -right-24 w-64 h-64 bg-primary/10 blur-[100px] rounded-full pointer-events-none" />
            <div className="absolute -bottom-24 -left-24 w-64 h-64 bg-success/5 blur-[100px] rounded-full pointer-events-none" />

            {/* Progress Header */}
            <div className="flex justify-between items-center mb-16 relative z-10 px-4">
                {steps.map((step, idx) => {
                    const Icon = step.icon;
                    const isActive = onboardingStep === step.id;
                    const isCompleted = onboardingStep > step.id;
                    return (
                        <div key={step.id} className="flex-1 flex flex-col items-center gap-3 relative">
                            <div className={`w-14 h-14 rounded-2xl flex items-center justify-center border-2 transition-all duration-500 shadow-xl ${
                                isActive ? 'border-primary bg-primary/20 text-white translate-y-[-4px] ring-4 ring-primary/10' :
                                isCompleted ? 'border-success bg-success/20 text-success' :
                                'border-white/5 bg-white/5 text-slate-700'
                            }`}>
                                <Icon size={24} strokeWidth={2.5} />
                            </div>
                            <div className="text-center">
                                <span className={`block text-[10px] font-black uppercase tracking-[0.2em] transition-colors ${isActive ? 'text-primary' : 'text-slate-600'}`}>
                                    {step.name}
                                </span>
                                <span className="block text-[8px] font-mono text-slate-700 uppercase mt-0.5">{step.description}</span>
                            </div>
                            {idx < steps.length - 1 && (
                                <div className="absolute left-[calc(50%+2rem)] top-7 w-[calc(100%-4rem)] h-[2px] opacity-20 hidden md:block overflow-hidden">
                                     <div className={`h-full transition-all duration-700 ${isCompleted ? 'bg-success translate-x-0' : 'bg-white/20 -translate-x-full'}`} />
                                </div>
                            )}
                        </div>
                    );
                })}
            </div>

            {/* Content Area */}
            <div className="min-h-[380px] mb-12 relative z-10 px-4">
                {renderStepContent()}
            </div>

            {/* Navigation */}
            {onboardingStep < 5 && (
                <div className="flex justify-between items-center pt-10 border-t border-white/5 relative z-10 px-4">
                    <button 
                        onClick={handleBack} 
                        className={`flex items-center gap-3 text-xs font-black tracking-widest text-slate-500 hover:text-white transition-all uppercase ${onboardingStep === 1 ? 'invisible' : ''}`}
                    >
                        <ChevronLeft size={16} /> BACK_LINK
                    </button>
                    
                    <div className="flex items-center gap-4">
                        <span className="text-[10px] font-mono text-slate-700 uppercase tracking-widest">Step 0{onboardingStep} / 05</span>
                        <button 
                            onClick={onboardingStep === 4 ? handleFinalSubmit : handleNext}
                            disabled={onboardingStep === 1 && !onboardingData.clientName}
                            className="flex items-center gap-3 bg-white text-black px-10 py-4 rounded-2xl font-black tracking-widest hover:bg-primary-light hover:text-white hover:shadow-[0_0_40px_rgba(var(--primary-h),0.4)] transition-all uppercase text-xs disabled:opacity-20 disabled:grayscale"
                        >
                            {onboardingStep === 4 ? 'COMMIT_V3' : 'PROCEED_FLOW'} <ChevronRight size={18} />
                        </button>
                    </div>
                </div>
            )}
        </div>
    );
};

export default AdvisorOnboardingWizard;
