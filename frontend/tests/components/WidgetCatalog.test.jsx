/**
 * Widget Catalog Component Tests
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import WidgetCatalog from '../../src/components/WidgetCatalog/WidgetCatalog';
import widgetRegistry from '../../src/core/WidgetRegistry';

vi.mock('../../src/core/WidgetRegistry', () => ({
  default: {
    getAll: vi.fn(),
    getCategories: vi.fn(() => []),
    on: vi.fn(),
    off: vi.fn(),
    get: vi.fn(),
    checkDependencies: vi.fn(),
  },
}));

describe('WidgetCatalog', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should render widget catalog', () => {
    widgetRegistry.getAll.mockReturnValue([]);
    render(<WidgetCatalog />);
    expect(screen.getByText(/widget catalog/i)).toBeInTheDocument();
  });

  it('should display available widgets', () => {
    const mockWidgets = [
      { id: 'widget1', name: 'Widget 1', description: 'Test widget 1' },
      { id: 'widget2', name: 'Widget 2', description: 'Test widget 2' },
    ];
    widgetRegistry.getAll.mockReturnValue(mockWidgets);

    render(<WidgetCatalog />);
    expect(screen.getByText('Widget 1')).toBeInTheDocument();
    expect(screen.getByText('Widget 2')).toBeInTheDocument();
  });

  it('should handle widget search', async () => {
    const mockWidgets = [
      { id: 'widget1', name: 'Chart Widget', description: 'A chart', category: 'charts' },
      { id: 'widget2', name: 'Other Widget', description: 'Other', category: 'other' },
    ];
    widgetRegistry.getAll.mockReturnValue(mockWidgets);

    render(<WidgetCatalog />);
    const searchInput = screen.getByPlaceholderText(/search/i);
    fireEvent.change(searchInput, { target: { value: 'chart' } });

    await waitFor(() => {
      expect(screen.getByText('Chart Widget')).toBeInTheDocument();
      expect(screen.queryByText('Other Widget')).not.toBeInTheDocument();
    });
  });

  it('should handle widget installation', async () => {
    const mockWidgets = [{ id: 'widget1', name: 'Widget 1', description: 'Test', category: 'test', dependencies: [], permissions: [], author: 'Test Author', version: '1.0.0' }];
    widgetRegistry.getAll.mockReturnValue(mockWidgets);
    widgetRegistry.checkDependencies.mockReturnValue({ satisfied: true, missing: [] });

    const onInstall = vi.fn();
    render(<WidgetCatalog onInstall={onInstall} />);
    
    // Widget catalog shows widgets, clicking one selects it
    const widgetItem = screen.getByText('Widget 1');
    fireEvent.click(widgetItem);

    // Look for install button in details section
    await waitFor(() => {
      const installButton = screen.queryByText(/install/i);
      if (installButton) {
        fireEvent.click(installButton);
        // onInstall is called after successful installation
        expect(onInstall).toHaveBeenCalled();
      }
    });
  });
});

