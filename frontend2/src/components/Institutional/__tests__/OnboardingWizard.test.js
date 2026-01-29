import React from 'react';
import { render } from '@testing-library/react';
import OnboardingWizard from '../OnboardingWizard';

// Mock Lucide icons as they can cause issues in snapshots
jest.mock('lucide-react', () => ({
    PenTool: () => <div data-testid="icon-pentool" />,
    CheckCircle2: () => <div data-testid="icon-check" />,
    ArrowRight: () => <div data-testid="icon-arrow-right" />,
    ShieldCheck: () => <div data-testid="icon-shield" />,
    Wallet: () => <div data-testid="icon-wallet" />,
    BarChart3: () => <div data-testid="icon-barchart" />,
    Sparkles: () => <div data-testid="icon-sparkles" />,
    Users: () => <div data-testid="icon-users" />,
    Activity: () => <div data-testid="icon-activity" />,
    Layout: () => <div data-testid="icon-layout" />
}));

// Mock the store
jest.mock('../../stores/institutionalStore', () => ({
    __esModule: true,
    default: () => ({
        onboardingStep: 1,
        setOnboardingStep: jest.fn(),
        createClient: jest.fn()
    })
}));

describe('OnboardingWizard Snapshots', () => {
    it('renders Step 1 correctly', () => {
        const { asFragment } = render(<OnboardingWizard />);
        expect(asFragment()).toMatchSnapshot();
    });
});
