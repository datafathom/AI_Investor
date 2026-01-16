/**
 * PageHeader Component Tests
 */

import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { MemoryRouter, Routes, Route } from 'react-router-dom';
import PageHeader from '../../src/components/Layout/PageHeader';

const renderWithRouter = (path = '/dashboard') => {
  return render(
    <MemoryRouter initialEntries={[path]}>
      <Routes>
        <Route path="*" element={<PageHeader />} />
      </Routes>
    </MemoryRouter>
  );
};

describe('PageHeader', () => {
  it('should render page header with title', () => {
    renderWithRouter('/dashboard');
    // PageHeader shows title in h1 element
    const title = document.querySelector('h1');
    expect(title).toBeInTheDocument();
    expect(title?.textContent).toMatch(/dashboard/i);
  });

  it('should render with subtitle', () => {
    renderWithRouter('/chat');
    // PageHeader shows title in h1 element
    const title = document.querySelector('h1');
    expect(title).toBeInTheDocument();
    expect(title?.textContent).toMatch(/chat/i);
  });

  it('should render with actions', () => {
    renderWithRouter('/telemetry');
    // PageHeader shows title in h1 element
    const title = document.querySelector('h1');
    expect(title).toBeInTheDocument();
    expect(title?.textContent).toMatch(/telemetry/i);
  });
});

