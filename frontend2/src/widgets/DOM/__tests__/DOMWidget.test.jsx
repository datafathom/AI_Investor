
import React from 'react';
import { render, screen } from '@testing-library/react';
import DOMWidget from '../DOMWidget';
import '@testing-library/jest-dom';
import apiClient from '../../../../services/apiClient';

// Mock dependencies
jest.mock('../../../../services/apiClient');
jest.mock('../../../hooks/useSymbolLinking', () => ({
  useSymbolLinking: () => ({
    groups: { 'blue': { symbol: 'NVDA' } },
    setGroupTicker: jest.fn()
  })
}));

describe('DOMWidget', () => {
  it('renders correctly', () => {
    apiClient.get.mockResolvedValue({ data: { asks: [], bids: [] } });
    render(<DOMWidget linkingGroup="blue" />);
    // Expect to see NVDA if linking works
  });
});
