/**
 * Main Entry Point
 * 
 * This is the entry point for the React application.
 * Simply renders the App component with all widgets on a single page.
 */

import React from 'react';
import ReactDOM from 'react-dom/client';
import ErrorBoundary from './components/ErrorBoundary';
import { BrowserRouter } from 'react-router-dom';
import App from './App';
import './index.css';

// Create root and render the app
ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <ErrorBoundary>
      <BrowserRouter>
        <App />
      </BrowserRouter>
    </ErrorBoundary>
  </React.StrictMode>
);

