/**
 * Shell Component Tests
 */

import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { MemoryRouter, Routes, Route } from 'react-router-dom';
import Shell from '../../src/components/Layout/Shell';

const renderWithRouter = (content = <div>Test Content</div>) => {
  return render(
    <MemoryRouter initialEntries={['/']}>
      <Routes>
        <Route path="/" element={<Shell />}>
          <Route index element={content} />
        </Route>
      </Routes>
    </MemoryRouter>
  );
};

describe('Shell', () => {
  it('should render shell layout', () => {
    renderWithRouter(<div>Test Content</div>);
    expect(screen.getByText('Test Content')).toBeInTheDocument();
  });

  it('should render with sidebar', () => {
    renderWithRouter(<div>Content</div>);
    // Sidebar is always rendered in Shell
    expect(screen.getByText(/dashboard/i)).toBeInTheDocument();
    expect(screen.getByText('Content')).toBeInTheDocument();
  });
});

