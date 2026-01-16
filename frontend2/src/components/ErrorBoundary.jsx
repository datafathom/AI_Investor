/**
 * Error Boundary Component
 * 
 * Catches React errors and displays user-friendly messages
 * without exposing internal file paths or stack traces.
 */

import React from 'react';
import { useColorPalette } from '../hooks/useColorPalette';

class ErrorBoundaryClass extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    // Log to console in development, but don't expose to user
    if (import.meta.env.DEV) {
      console.error('Error caught by boundary:', error, errorInfo);
    }
  }

  render() {
    if (this.state.hasError) {
      return <ErrorFallback palette={this.props.palette} />;
    }

    return this.props.children;
  }
}

function ErrorFallback({ palette }) {
  return (
    <div
      style={{
        minHeight: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        padding: '2rem',
        backgroundColor: palette?.backgrounds?.main || '#fffef0',
      }}
    >
      <div
        className="glass card"
        style={{
          maxWidth: '600px',
          padding: '2rem',
          textAlign: 'center',
        }}
      >
        <h2 style={{ color: palette?.burgundy?.primary || '#5a1520', marginBottom: '1rem' }}>
          Something went wrong
        </h2>
        <p style={{ color: palette?.text?.secondary || '#5a4a3a', marginBottom: '1.5rem' }}>
          We encountered an unexpected error. Please refresh the page or contact support if the problem persists.
        </p>
        <button
          className="btn btn-primary"
          onClick={() => window.location.reload()}
        >
          Refresh Page
        </button>
      </div>
    </div>
  );
}

function ErrorBoundary({ children }) {
  const { palette } = useColorPalette();
  
  return (
    <ErrorBoundaryClass palette={palette}>
      {children}
    </ErrorBoundaryClass>
  );
}

export default ErrorBoundary;

