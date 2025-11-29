import React from 'react';

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    console.error('Error caught by boundary:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-screen bg-bg-main dark:bg-dark-bg-main flex items-center justify-center p-4">
          <div className="max-w-md w-full bg-bg-card dark:bg-dark-bg-card rounded-lg shadow-lg p-6 border border-gray-200 dark:border-dark-border">
            <h1 className="text-2xl font-bold text-text-heading dark:text-dark-text-primary mb-4">
              Something went wrong
            </h1>
            <p className="text-text-body dark:text-dark-text-secondary mb-4">
              {this.state.error?.message || 'An unexpected error occurred'}
            </p>
            <button
              onClick={() => window.location.reload()}
              className="btn-primary"
            >
              Reload Page
            </button>
            <details className="mt-4">
              <summary className="cursor-pointer text-sm text-text-muted dark:text-dark-text-secondary">
                Error Details
              </summary>
              <pre className="mt-2 text-xs bg-gray-100 dark:bg-dark-bg-main p-2 rounded overflow-auto">
                {this.state.error?.stack}
              </pre>
            </details>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;
