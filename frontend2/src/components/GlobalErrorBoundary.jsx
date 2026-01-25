
import React from 'react';
import { captureException } from '../utils/errorTracking';

class GlobalErrorBoundary extends React.Component {
    constructor(props) {
        super(props);
        this.state = { hasError: false, error: null, errorInfo: null };
    }

    static getDerivedStateFromError(error) {
        return { hasError: true };
    }

    componentDidCatch(error, errorInfo) {
        console.error("Global Error Boundary caught an error", error, errorInfo);
        // Send to error tracking
        captureException(error, {
            componentStack: errorInfo.componentStack,
            errorBoundary: 'GlobalErrorBoundary',
        });
        this.setState({
            error,
            errorInfo: errorInfo || { componentStack: 'Not available' }
        });
    }

    render() {
        if (this.state.hasError) {
            return (
                <div style={{ padding: '20px', backgroundColor: '#fff0f0', border: '2px solid #ff0000', margin: '20px', borderRadius: '8px', color: '#333' }}>
                    <h2 style={{ color: '#d32f2f' }}>Something went wrong.</h2>
                    <details style={{ whiteSpace: 'pre-wrap' }}>
                        {this.state.error && this.state.error.toString()}
                        <br />
                        {this.state.errorInfo ? this.state.errorInfo.componentStack : 'No stack trace available'}
                    </details>
                    <button
                        onClick={() => window.location.reload()}
                        style={{ marginTop: '20px', padding: '10px 20px', cursor: 'pointer', backgroundColor: '#d32f2f', color: 'white', border: 'none', borderRadius: '4px' }}
                    >
                        Reload Page
                    </button>
                </div>
            );
        }

        return this.props.children;
    }
}

export default GlobalErrorBoundary;
