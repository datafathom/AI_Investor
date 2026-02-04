/**
 * Error Handler Utility
 * 
 * Centralized error handling and logging utilities.
 */

/**
 * Error types
 */
export const ErrorTypes = {
  NETWORK: 'NETWORK_ERROR',
  API: 'API_ERROR',
  VALIDATION: 'VALIDATION_ERROR',
  AUTH: 'AUTH_ERROR',
  UNKNOWN: 'UNKNOWN_ERROR',
};

/**
 * Get error type from error object
 * @param {Error} error - Error object
 * @returns {string} Error type
 */
export function getErrorType(error) {
  if (error.name === 'NetworkError' || error.message.includes('fetch')) {
    return ErrorTypes.NETWORK;
  }
  if (error.status || error.response) {
    return ErrorTypes.API;
  }
  if (error.message.includes('validation') || error.message.includes('invalid')) {
    return ErrorTypes.VALIDATION;
  }
  if (error.status === 401 || error.status === 403) {
    return ErrorTypes.AUTH;
  }
  return ErrorTypes.UNKNOWN;
}

/**
 * Format error message for display
 * @param {Error} error - Error object
 * @returns {string} User-friendly error message
 */
export function formatErrorMessage(error) {
  const type = getErrorType(error);
  
  switch (type) {
    case ErrorTypes.NETWORK:
      return 'Network error. Please check your connection and try again.';
    case ErrorTypes.API:
      return error.message || 'An error occurred while processing your request.';
    case ErrorTypes.VALIDATION:
      return error.message || 'Please check your input and try again.';
    case ErrorTypes.AUTH:
      return 'Authentication required. Please log in and try again.';
    default:
      return error.message || 'An unexpected error occurred.';
  }
}

/**
 * Log error to console and/or external service
 * @param {Error} error - Error object
 * @param {Object} context - Additional context
 */
export function logError(error, context = {}) {
  const errorInfo = {
    message: error.message,
    stack: error.stack,
    type: getErrorType(error),
    context,
    timestamp: new Date().toISOString(),
  };
  
  console.error('Error:', errorInfo);
  
  // In production, send to error tracking service
  if (import.meta.env.PROD) {
    // Example: send to Sentry, LogRocket, etc.
    // errorTrackingService.captureException(error, { extra: context });
  }
}

/**
 * Handle API error
 * @param {Error} error - Error object
 * @param {Function} onError - Error callback
 */
export function handleApiError(error, onError) {
  const formattedError = formatErrorMessage(error);
  logError(error, { source: 'API' });
  
  if (onError) {
    onError(formattedError);
  } else {
    console.error('API Error:', formattedError);
  }
}

/**
 * Create error object
 * @param {string} message - Error message
 * @param {string} type - Error type
 * @param {Object} details - Additional error details
 * @returns {Error} Error object
 */
export function createError(message, type = ErrorTypes.UNKNOWN, details = {}) {
  const error = new Error(message);
  error.type = type;
  error.details = details;
  return error;
}

/**
 * Error boundary helper
 * @param {Error} error - Error object
 * @param {ErrorInfo} errorInfo - React error info
 */
export function handleReactError(error, errorInfo) {
  logError(error, {
    source: 'React',
    componentStack: errorInfo?.componentStack,
  });
}

