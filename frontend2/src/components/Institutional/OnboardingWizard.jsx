import React from 'react';
import { User, Shield, CreditCard, PieChart, CheckCircle, ChevronRight, ChevronLeft } from 'lucide-react';
import './OnboardingWizard.css';
import useInstitutionalStore from '../../stores/institutionalStore';
import { useStore } from '../../store/store';

const OnboardingWizard = () => {
    const { onboardingStep, setOnboardingStep, createClient, resetOnboarding } = useInstitutionalStore();
    const user = useStore(state => state.user);
    
    const [formData, setFormData] = React.useState({
        clientName: '',
        email: '',
        jurisdiction: 'US',
        fundingSource: 'Plaid',
        strategy: 'Aggressive AI',
    });

    const steps = [
        { id: 1, name: 'Identity', icon: User },
        { id: 2, name: 'Compliance', icon: Shield },
        { id: 3, name: 'Funding', icon: CreditCard },
        { id: 4, name: 'Strategy', icon: PieChart },
        { id: 5, name: 'Finalize', icon: CheckCircle },
    ];

    const handleNext = () => setOnboardingStep(Math.min(onboardingStep + 1, 5));
    const handleBack = () => setOnboardingStep(Math.max(onboardingStep - 1, 1));

    const handleSubmit = async () => {
        await createClient({
            client_name: formData.clientName,
            advisor_id: user?.id || 'demo-advisor',
            jurisdiction: formData.jurisdiction,
            funding_source: formData.fundingSource,
            strategy: formData.strategy
        });
        setOnboardingStep(5);
    };

    const renderStepContent = () => {
        switch (onboardingStep) {
            case 1:
                return (
                    <div className="space-y-4">
                        <h3 className="text-xl font-bold">Client Identity</h3>
                        <div className="space-y-2">
                            <label className="text-xs uppercase text-slate-500">Client Name</label>
                            <input 
                                type="text" 
                                className="w-full bg-white/5 border border-white/10 rounded-lg p-3 text-white" 
                                placeholder="e.g. John Doe / Alpha Trust"
                                value={formData.clientName}
                                onChange={(e) => setFormData({...formData, clientName: e.target.value})}
                            />
                        </div>
                    </div>
                );
            case 2:
                return (
                    <div className="space-y-4">
                        <h3 className="text-xl font-bold">Compliance Check</h3>
                        <p className="text-sm text-slate-400">Automated AML/KYC screening initiated for {formData.jurisdiction}.</p>
                        <select 
                            className="w-full bg-white/5 border border-white/10 rounded-lg p-3 text-white"
                            value={formData.jurisdiction}
                            onChange={(e) => setFormData({...formData, jurisdiction: e.target.value})}
                        >
                            <option value="US">United States (SEC/FINRA)</option>
                            <option value="UK">United Kingdom (FCA)</option>
                            <option value="EU">European Union (ESMA)</option>
                        </select>
                    </div>
                );
            case 3:
                return (
                    <div className="space-y-4">
                        <h3 className="text-xl font-bold">Connect Funding</h3>
                        <div className="grid grid-cols-2 gap-4">
                            <button className="p-4 rounded-xl border border-primary/30 bg-primary/10 flex flex-col items-center gap-2">
                                <span className="font-bold">PLAID</span>
                                <span className="text-[10px] opacity-50">Instant Bank Verif</span>
                            </button>
                            <button className="p-4 rounded-xl border border-white/10 bg-white/5 flex flex-col items-center gap-2 opacity-50">
                                <span className="font-bold">STRIPE</span>
                                <span className="text-[10px]">Merchant Flow</span>
                            </button>
                        </div>
                    </div>
                );
            case 4:
                return (
                    <div className="space-y-4">
                        <h3 className="text-xl font-bold">AI Agent Strategy</h3>
                        <select 
                            className="w-full bg-white/5 border border-white/10 rounded-lg p-3 text-white"
                            value={formData.strategy}
                            onChange={(e) => setFormData({...formData, strategy: e.target.value})}
                        >
                            <option value="Aggressive AI">Aggressive AI (Max Gen Fitness)</option>
                            <option value="Balanced Zen">Balanced Zen (Hedge First)</option>
                            <option value="Capital Preservation">Conservative (Dividend Focused)</option>
                        </select>
                    </div>
                );
            case 5:
                return (
                    <div className="space-y-4 text-center">
                        <div className="w-20 h-20 bg-success/20 rounded-full flex items-center justify-center mx-auto text-success border border-success/30">
                            <CheckCircle size={40} />
                        </div>
                        <h3 className="text-xl font-bold">Onboarding Complete</h3>
                        <p className="text-sm text-slate-400">Legal engagement generated. Client ready for funding.</p>
                        <button 
                            onClick={resetOnboarding}
                            className="px-6 py-2 bg-primary rounded-lg font-bold"
                        >
                            Go to Dashboard
                        </button>
                    </div>
                );
            default:
                return null;
        }
    };

    return (
        <div className="onboarding-wizard glass-premium p-8 rounded-3xl border border-white/5 max-w-2xl mx-auto">
            {/* Progress Header */}
            <div className="flex justify-between mb-12">
                {steps.map((step) => {
                    const Icon = step.icon;
                    const isActive = onboardingStep === step.id;
                    const isCompleted = onboardingStep > step.id;
                    return (
                        <div key={step.id} className="flex flex-col items-center gap-2 relative">
                            <div className={`w-10 h-10 rounded-full flex items-center justify-center border-2 transition-all ${
                                isActive ? 'border-primary bg-primary/20 text-white' :
                                isCompleted ? 'border-success bg-success/20 text-success' :
                                'border-white/10 text-slate-500'
                            }`}>
                                <Icon size={18} />
                            </div>
                            <span className={`text-[10px] font-bold uppercase tracking-widest ${isActive ? 'text-primary' : 'text-slate-500'}`}>
                                {step.name}
                            </span>
                            {step.id < 5 && (
                                <div className={`absolute left-full top-5 w-12 h-[2px] -mx-2 opacity-20 ${isCompleted ? 'bg-success' : 'bg-white'}`} />
                            )}
                        </div>
                    );
                })}
            </div>

            {/* Content Area */}
            <div className="min-h-[200px] mb-8">
                {renderStepContent()}
            </div>

            {/* Navigation */}
            {onboardingStep < 5 && (
                <div className="flex justify-between pt-8 border-t border-white/5">
                    <button 
                        onClick={handleBack} 
                        disabled={onboardingStep === 1}
                        className="flex items-center gap-2 text-sm font-bold opacity-50 hover:opacity-100 disabled:hidden"
                    >
                        <ChevronLeft size={16} /> BACK
                    </button>
                    <button 
                        onClick={onboardingStep === 4 ? handleSubmit : handleNext}
                        className="flex items-center gap-2 bg-primary text-white px-6 py-2 rounded-xl font-bold hover:shadow-[0_0_20px_rgba(var(--primary-h),0.4)] transition-all ml-auto"
                    >
                        {onboardingStep === 4 ? 'FINALIZE' : 'NEXT'} <ChevronRight size={16} />
                    </button>
                </div>
            )}
        </div>
    );
};

export default OnboardingWizard;
