
import React from 'react';
import { render, screen } from '@testing-library/react';
import DOMWidget from '../DOMWidget';
import '@testing-library/jest-dom';

// Mock dependencies
jest.mock('../../../hooks/useSymbolLinking', () => ({
  useSymbolLinking: () => ({
    groups: { 'blue': { symbol: 'NVDA' } },
    setGroupTicker: jest.fn()
  })
}));

describe('DOMWidget', () => {
  it('renders correctly', () => {
    render(<DOMWidget linkingGroup="blue" />);
    // Expect to see NVDA if linking works
  });
});
