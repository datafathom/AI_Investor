/**
 * Frontend Error Tracking
 * Integrates with Sentry for production error tracking
 */

let sentryInitialized = false;
let errorTracker = null;

/**
 * Initialize error tracking
 */
export function initErrorTracking() {
  // Only initialize in production
  if (import.meta.env.PROD && import.meta.env.VITE_SENTRY_DSN) {
    try {
      import('@sentry/react').then((Sentry) => {
        Sentry.init({
          dsn: import.meta.env.VITE_SENTRY_DSN,
          environment: import.meta.env.MODE || 'production',
          integrations: [
            Sentry.browserTracingIntegration(),
            Sentry.replayIntegration({
              maskAllText: true,
              blockAllMedia: true,
            }),
          ],
          tracesSampleRate: parseFloat(import.meta.env.VITE_SENTRY_TRACES_SAMPLE_RATE || '0.1'),
          replaysSessionSampleRate: parseFloat(import.meta.env.VITE_SENTRY_REPLAY_SAMPLE_RATE || '0.1'),
          replaysOnErrorSampleRate: 1.0,
          beforeSend(event, hint) {
            // Don't send events in development
            if (import.meta.env.DEV) {
              return null;
            }
            return event;
          },
        });
        sentryInitialized = true;
        errorTracker = Sentry;
        console.log('✅ Error tracking initialized (Sentry)');
      });
    } catch (error) {
      console.warn('Failed to initialize error tracking:', error);
    }
  } else {
    console.log('Error tracking not configured (development mode or DSN not set)');
  }
}

/**
 * Capture exception
 */
export function captureException(error, context = {}) {
  // 1. Send to standard console for local debugging
  console.error('[CaptureException]', error, context);

  // 2. Send to backend telemetry (The "Golden Path" for observability)
  // We use a detached promise to avoid blocking the UI
  try {
    const apiClient = window.apiClient; // Accessing via window to avoid circular dependency
    if (apiClient) {
      apiClient.post('/system/error', {
        error: error instanceof Error ? error.message : String(error),
        stack: error instanceof Error ? error.stack : 'N/A',
        context: context
      }).catch(err => console.warn('[TelemetryFailed]', err));
    }
  } catch (err) {
    // Fail silently to avoid recursive error loops
  }

  // 3. Send to Sentry if initialized
  if (errorTracker) {
    errorTracker.captureException(error, {
      contexts: {
        custom: context,
      },
    });
  }
}

/**
 * Capture message
 */
export function captureMessage(message, level = 'error', context = {}) {
  if (errorTracker) {
    errorTracker.captureMessage(message, {
      level,
      contexts: {
        custom: context,
      },
    });
  } else {
    console.log(`[${level.toUpperCase()}]`, message, context);
  }
}

/**
 * Set user context
 */
export function setUser(userId, email, username) {
  if (errorTracker) {
    errorTracker.setUser({
      id: userId,
      email,
      username,
    });
  }
}

/**
 * Add breadcrumb
 */
export function addBreadcrumb(message, category = 'default', level = 'info', data = {}) {
  if (errorTracker) {
    errorTracker.addBreadcrumb({
      message,
      category,
      level,
      data,
    });
  }
}

/**
 * Set tag
 */
export function setTag(key, value) {
  if (errorTracker) {
    errorTracker.setTag(key, value);
  }
}

/**
 * Set context
 */
export function setContext(key, value) {
  if (errorTracker) {
    errorTracker.setContext(key, value);
  }
}

// Initialize on module load
if (typeof window !== 'undefined') {
  initErrorTracking();
  
  // Global error handler
  window.addEventListener('error', (event) => {
    captureException(event.error, {
      filename: event.filename,
      lineno: event.lineno,
      colno: event.colno,
    });
  });
  
  // Unhandled promise rejection handler
  window.addEventListener('unhandledrejection', (event) => {
    captureException(event.reason, {
      type: 'unhandledrejection',
    });
  });
}

export default {
  initErrorTracking,
  captureException,
  captureMessage,
  setUser,
  addBreadcrumb,
  setTag,
  setContext,
};
