/**
 * Test Setup
 * 
 * Global test configuration and utilities.
 */

import { expect, afterEach, vi } from 'vitest';
import { cleanup } from '@testing-library/react';
import '@testing-library/jest-dom';
import React from 'react';

// Cleanup after each test
afterEach(() => {
  cleanup();
});

// Mock window.matchMedia
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: vi.fn().mockImplementation(query => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: vi.fn(),
    removeListener: vi.fn(),
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
    dispatchEvent: vi.fn(),
  })),
});

// Mock localStorage
const localStorageMock = (() => {
  let store = {};
  return {
    getItem: vi.fn((key) => store[key] || null),
    setItem: vi.fn((key, value) => {
      store[key] = value.toString();
    }),
    removeItem: vi.fn((key) => {
      delete store[key];
    }),
    clear: vi.fn(() => {
      store = {};
    }),
  };
})();
global.localStorage = localStorageMock;

// Mock ResizeObserver
global.ResizeObserver = class ResizeObserver {
  constructor(cb) {
    this.cb = cb;
  }
  observe() {}
  unobserve() {}
  disconnect() {}
};

// Mock scrollIntoView
Element.prototype.scrollIntoView = vi.fn();

// Global UI Component Mocks for Admin Pages
vi.mock('@/components/ui/button', () => ({
  Button: ({ children, ...props }) => React.createElement('button', props, children)
}));

vi.mock('@/components/ui/input', () => ({
  Input: (props) => React.createElement('input', props)
}));

vi.mock('@/components/ui/label', () => ({
  Label: ({ children }) => React.createElement('label', null, children)
}));

vi.mock('@/components/ui/use-toast', () => ({
  useToast: () => ({ toast: vi.fn() })
}));

vi.mock('@/components/ui/card', () => ({
  Card: ({ children }) => React.createElement('div', null, children),
  CardContent: ({ children }) => React.createElement('div', null, children),
  CardHeader: ({ children }) => React.createElement('div', null, children),
  CardTitle: ({ children }) => React.createElement('div', null, children),
  CardDescription: ({ children }) => React.createElement('div', null, children),
  CardFooter: ({ children }) => React.createElement('div', null, children)
}));

vi.mock('@/components/ui/dialog', () => ({
  Dialog: ({ children }) => React.createElement('div', null, children),
  DialogContent: ({ children }) => React.createElement('div', null, children),
  DialogDescription: ({ children }) => React.createElement('div', null, children),
  DialogHeader: ({ children }) => React.createElement('div', null, children),
  DialogTitle: ({ children }) => React.createElement('div', null, children),
  DialogFooter: ({ children }) => React.createElement('div', null, children)
}));

vi.mock('@/components/ui/badge', () => ({
  Badge: ({ children }) => React.createElement('span', null, children)
}));

vi.mock('@/components/ui/scroll-area', () => ({
  ScrollArea: ({ children }) => React.createElement('div', null, children)
}));

vi.mock('@/components/ui/alert', () => ({
  Alert: ({ children }) => React.createElement('div', null, children),
  AlertDescription: ({ children }) => React.createElement('div', null, children),
  AlertTitle: ({ children }) => React.createElement('div', null, children)
}));
