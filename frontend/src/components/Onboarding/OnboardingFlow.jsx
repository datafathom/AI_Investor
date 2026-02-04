import React, { useState, useEffect } from 'react';
import './OnboardingFlow.css';

const OnboardingFlow = ({ onComplete, onSkip }) => {
  const [currentStep, setCurrentStep] = useState(0);
  const [userData, setUserData] = useState({
    experience: '',
    goals: [],
    riskTolerance: '',
    investmentAmount: '',
    timeHorizon: ''
  });

  const steps = [
    {
      id: 'welcome',
      title: 'Welcome to AI Investor',
      component: WelcomeStep
    },
    {
      id: 'experience',
      title: 'Your Trading Experience',
      component: ExperienceStep
    },
    {
      id: 'goals',
      title: 'Investment Goals',
      component: GoalsStep
    },
    {
      id: 'risk',
      title: 'Risk Tolerance',
      component: RiskStep
    },
    {
      id: 'preferences',
      title: 'Investment Preferences',
      component: PreferencesStep
    },
    {
      id: 'complete',
      title: 'Setup Complete',
      component: CompleteStep
    }
  ];

  const handleNext = () => {
    if (currentStep < steps.length - 1) {
      setCurrentStep(currentStep + 1);
    } else {
      handleComplete();
    }
  };

  const handleBack = () => {
    if (currentStep > 0) {
      setCurrentStep(currentStep - 1);
    }
  };

  const handleComplete = () => {
    // Save onboarding data
    localStorage.setItem('onboarding_completed', 'true');
    localStorage.setItem('onboarding_data', JSON.stringify(userData));
    
    // Track completion
    if (window.gtag) {
      window.gtag('event', 'onboarding_complete', {
        experience: userData.experience,
        risk_tolerance: userData.riskTolerance
      });
    }
    
    if (onComplete) {
      onComplete(userData);
    }
  };

  const handleSkip = () => {
    if (onSkip) {
      onSkip();
    }
  };

  const CurrentStepComponent = steps[currentStep].component;
  const progress = ((currentStep + 1) / steps.length) * 100;

  return (
    <div className="onboarding-overlay">
      <div className="onboarding-modal">
        <div className="onboarding-header">
          <div className="onboarding-progress">
            <div className="progress-bar" style={{ width: `${progress}%` }} />
          </div>
          <button className="skip-button" onClick={handleSkip}>
            Skip
          </button>
        </div>

        <div className="onboarding-content">
          <CurrentStepComponent
            userData={userData}
            setUserData={setUserData}
            onNext={handleNext}
            onBack={handleBack}
            isFirst={currentStep === 0}
            isLast={currentStep === steps.length - 1}
          />
        </div>

        <div className="onboarding-footer">
          {!steps[currentStep].component.isLast && (
            <>
              {currentStep > 0 && (
                <button className="btn-secondary" onClick={handleBack}>
                  Back
                </button>
              )}
              <button className="btn-primary" onClick={handleNext}>
                {currentStep === steps.length - 1 ? 'Complete' : 'Next'}
              </button>
            </>
          )}
        </div>
      </div>
    </div>
  );
};

// Step Components
const WelcomeStep = ({ onNext }) => (
  <div className="onboarding-step">
    <h2>Welcome to AI Investor</h2>
    <p>Let's get you set up in just a few minutes.</p>
    <div className="welcome-features">
      <div className="feature">
        <span className="icon">🤖</span>
        <h3>AI-Powered Trading</h3>
        <p>Advanced algorithms for smarter investing</p>
      </div>
      <div className="feature">
        <span className="icon">📊</span>
        <h3>Real-Time Analytics</h3>
        <p>Comprehensive portfolio insights</p>
      </div>
      <div className="feature">
        <span className="icon">🛡️</span>
        <h3>Risk Management</h3>
        <p>Built-in safeguards for your investments</p>
      </div>
    </div>
  </div>
);

const ExperienceStep = ({ userData, setUserData }) => {
  const options = [
    { value: 'beginner', label: 'Beginner', description: 'New to trading' },
    { value: 'intermediate', label: 'Intermediate', description: 'Some trading experience' },
    { value: 'advanced', label: 'Advanced', description: 'Experienced trader' },
    { value: 'professional', label: 'Professional', description: 'Professional trader' }
  ];

  return (
    <div className="onboarding-step">
      <h2>What's your trading experience?</h2>
      <p>This helps us customize your experience</p>
      <div className="option-grid">
        {options.map(option => (
          <button
            key={option.value}
            className={`option-card ${userData.experience === option.value ? 'selected' : ''}`}
            onClick={() => setUserData({ ...userData, experience: option.value })}
          >
            <h3>{option.label}</h3>
            <p>{option.description}</p>
          </button>
        ))}
      </div>
    </div>
  );
};

const GoalsStep = ({ userData, setUserData }) => {
  const goals = [
    { id: 'growth', label: 'Long-term Growth', icon: '📈' },
    { id: 'income', label: 'Passive Income', icon: '💰' },
    { id: 'retirement', label: 'Retirement Planning', icon: '🏖️' },
    { id: 'trading', label: 'Active Trading', icon: '⚡' },
    { id: 'education', label: 'Learn & Practice', icon: '📚' }
  ];

  const toggleGoal = (goalId) => {
    const goals = userData.goals || [];
    if (goals.includes(goalId)) {
      setUserData({ ...userData, goals: goals.filter(g => g !== goalId) });
    } else {
      setUserData({ ...userData, goals: [...goals, goalId] });
    }
  };

  return (
    <div className="onboarding-step">
      <h2>What are your investment goals?</h2>
      <p>Select all that apply</p>
      <div className="goal-grid">
        {goals.map(goal => (
          <button
            key={goal.id}
            className={`goal-card ${userData.goals?.includes(goal.id) ? 'selected' : ''}`}
            onClick={() => toggleGoal(goal.id)}
          >
            <span className="goal-icon">{goal.icon}</span>
            <span className="goal-label">{goal.label}</span>
          </button>
        ))}
      </div>
    </div>
  );
};

const RiskStep = ({ userData, setUserData }) => {
  const riskLevels = [
    { value: 'conservative', label: 'Conservative', description: 'Low risk, steady returns' },
    { value: 'moderate', label: 'Moderate', description: 'Balanced risk and return' },
    { value: 'aggressive', label: 'Aggressive', description: 'Higher risk, higher potential' }
  ];

  return (
    <div className="onboarding-step">
      <h2>What's your risk tolerance?</h2>
      <p>How comfortable are you with market volatility?</p>
      <div className="risk-slider-container">
        {riskLevels.map(level => (
          <button
            key={level.value}
            className={`risk-card ${userData.riskTolerance === level.value ? 'selected' : ''}`}
            onClick={() => setUserData({ ...userData, riskTolerance: level.value })}
          >
            <h3>{level.label}</h3>
            <p>{level.description}</p>
          </button>
        ))}
      </div>
    </div>
  );
};

const PreferencesStep = ({ userData, setUserData }) => {
  return (
    <div className="onboarding-step">
      <h2>Investment Preferences</h2>
      <div className="preferences-form">
        <div className="form-group">
          <label>Initial Investment Amount</label>
          <select
            value={userData.investmentAmount}
            onChange={(e) => setUserData({ ...userData, investmentAmount: e.target.value })}
          >
            <option value="">Select amount</option>
            <option value="0-1000">$0 - $1,000</option>
            <option value="1000-10000">$1,000 - $10,000</option>
            <option value="10000-50000">$10,000 - $50,000</option>
            <option value="50000+">$50,000+</option>
          </select>
        </div>
        <div className="form-group">
          <label>Investment Time Horizon</label>
          <select
            value={userData.timeHorizon}
            onChange={(e) => setUserData({ ...userData, timeHorizon: e.target.value })}
          >
            <option value="">Select horizon</option>
            <option value="short">Short-term (0-1 years)</option>
            <option value="medium">Medium-term (1-5 years)</option>
            <option value="long">Long-term (5+ years)</option>
          </select>
        </div>
      </div>
    </div>
  );
};

const CompleteStep = ({ userData }) => {
  return (
    <div className="onboarding-step complete-step">
      <div className="complete-icon">✅</div>
      <h2>You're All Set!</h2>
      <p>Your AI Investor account is ready to go.</p>
      <div className="next-steps">
        <h3>Next Steps:</h3>
        <ul>
          <li>Connect your brokerage account</li>
          <li>Explore the dashboard</li>
          <li>Set up your first strategy</li>
        </ul>
      </div>
    </div>
  );
};

export default OnboardingFlow;
