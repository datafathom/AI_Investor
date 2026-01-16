/**
 * Charts Components Tests
 */

import { describe, it, expect } from 'vitest';
import { render } from '@testing-library/react';
import { SimpleBarChart } from '../../src/components/Charts/SimpleCharts';
import { SimplePlanetMenu } from '../../src/components/Charts/PlanetMenus';

describe('SimpleCharts', () => {
  it('should render SimpleCharts component', () => {
    const mockData = [
      { label: 'Series A', values: [{ x: 'A', y: 10 }, { x: 'B', y: 5 }] }
    ];
    const { container } = render(<SimpleBarChart data={mockData} />);
    // Charts render SVG/canvas elements
    expect(container).toBeTruthy();
  });
});

describe('PlanetMenus', () => {
  it('should render PlanetMenus component', () => {
    const mockItems = [
      { label: 'Item 1', onClick: () => {} },
      { label: 'Item 2', onClick: () => {} },
    ];
    const { container } = render(<SimplePlanetMenu items={mockItems} />);
    // Planet menus render complex SVG/canvas elements
    expect(container).toBeTruthy();
  });
});

