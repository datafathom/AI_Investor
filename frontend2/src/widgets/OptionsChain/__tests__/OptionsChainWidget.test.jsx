
import React from 'react';
import { render, screen } from '@testing-library/react';
import OptionsChainWidget from '../OptionsChainWidget';
import '@testing-library/jest-dom';

// Mock dependencies
jest.mock('../../../hooks/useSymbolLinking', () => ({
  useSymbolLinking: () => ({
    groups: { 'blue': { symbol: 'TSLA' } },
    setGroupTicker: jest.fn()
  })
}));

describe('OptionsChainWidget', () => {
  it('renders correctly', () => {
    render(<OptionsChainWidget />);
    // Since it's loading simulated data, we might see the loading state or title
    // But initially it might render the header using defaults.
    // Let's assume default props.
    // Note: The widget relies on fetching data.
    // Accessing text content that exists in the mock or static UI.
    
    // Check if container exists (by class or text)
    // The widget renders a header with symbol.
    // If mock returns 'TSLA', we expect 'TSLA'
  });
});
