import React from 'react';
import { render, screen } from '@testing-library/react';
import FeatureFlagManager from '../pages/admin/FeatureFlagManager';
import { vi } from 'vitest';

// Mock FeatureFlagCard
vi.mock('@/components/cards/FeatureFlagCard', () => ({
    default: () => <div>Feature Flag Card</div>
}));

// Mock fetch
global.fetch = vi.fn(() => Promise.resolve({
    ok: true,
    json: () => Promise.resolve({})
}));

// Mock apiClient
vi.mock('../services/apiClient', () => ({
    default: {
        get: vi.fn(() => Promise.resolve({})),
    }
}));

describe('FeatureFlagManager Component', () => {
    it('renders the feature containment header', async () => {
        render(<FeatureFlagManager />);
        expect(await screen.findByText(/Feature Containment/i)).toBeTruthy();
    });
});
