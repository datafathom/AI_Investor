/**
 * Main Entry Point
 * 
 * This is the entry point for the React application.
 * Simply renders the App component with all widgets on a single page.
 */

import React from 'react';
import ReactDOM from 'react-dom/client';
import ErrorBoundary from './components/ErrorBoundary';
import { initErrorTracking } from './utils/errorTracking';
import { initRequestGuard } from './utils/requestGuard';

// Enforce centralized API usage
initRequestGuard();

// Initialize error tracking
initErrorTracking();
import { BrowserRouter } from 'react-router-dom';
import App from './App';
import './index.css';
import { initWidgets } from './core/initWidgets';

// Create root and render the app
// Initialize core widgets
initWidgets();

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <ErrorBoundary>
      <BrowserRouter>
        <App />
      </BrowserRouter>
    </ErrorBoundary>
  </React.StrictMode>
);

