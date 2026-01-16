/**
 * Performance Utilities
 * 
 * Utilities for performance monitoring and optimization.
 */

/**
 * Debounce function
 * @param {Function} func - Function to debounce
 * @param {number} wait - Wait time in milliseconds
 * @returns {Function} Debounced function
 */
export function debounce(func, wait) {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}

/**
 * Throttle function
 * @param {Function} func - Function to throttle
 * @param {number} limit - Time limit in milliseconds
 * @returns {Function} Throttled function
 */
export function throttle(func, limit) {
  let inThrottle;
  return function executedFunction(...args) {
    if (!inThrottle) {
      func.apply(this, args);
      inThrottle = true;
      setTimeout(() => (inThrottle = false), limit);
    }
  };
}

/**
 * Measure function execution time
 * @param {Function} func - Function to measure
 * @param {string} label - Label for logging
 * @returns {Function} Wrapped function
 */
export function measurePerformance(func, label = 'Function') {
  return function measuredFunction(...args) {
    const start = performance.now();
    const result = func.apply(this, args);
    const end = performance.now();
    console.log(`${label} took ${(end - start).toFixed(2)}ms`);
    return result;
  };
}

/**
 * Lazy load component
 * @param {Function} importFunc - Dynamic import function
 * @returns {Promise} Component promise
 */
export function lazyLoad(importFunc) {
  return importFunc().then(module => ({ default: module.default }));
}

/**
 * Check if code is running in production
 * @returns {boolean} True if production
 */
export function isProduction() {
  return import.meta.env.PROD;
}

/**
 * Check if code is running in development
 * @returns {boolean} True if development
 */
export function isDevelopment() {
  return import.meta.env.DEV;
}

/**
 * Performance observer for monitoring
 */
export class PerformanceMonitor {
  constructor() {
    this.metrics = [];
    this.observers = [];
  }

  /**
   * Start observing performance
   */
  start() {
    if ('PerformanceObserver' in window) {
      // Observe long tasks
      const longTaskObserver = new PerformanceObserver((list) => {
        for (const entry of list.getEntries()) {
          if (entry.duration > 50) {
            this.metrics.push({
              type: 'long-task',
              duration: entry.duration,
              timestamp: entry.startTime,
            });
          }
        }
      });
      
      try {
        longTaskObserver.observe({ entryTypes: ['longtask'] });
        this.observers.push(longTaskObserver);
      } catch (e) {
        // Long task observer not supported
      }

      // Observe paint metrics
      const paintObserver = new PerformanceObserver((list) => {
        for (const entry of list.getEntries()) {
          this.metrics.push({
            type: 'paint',
            name: entry.name,
            duration: entry.duration,
            timestamp: entry.startTime,
          });
        }
      });
      
      try {
        paintObserver.observe({ entryTypes: ['paint'] });
        this.observers.push(paintObserver);
      } catch (e) {
        // Paint observer not supported
      }
    }
  }

  /**
   * Stop observing performance
   */
  stop() {
    this.observers.forEach(observer => observer.disconnect());
    this.observers = [];
  }

  /**
   * Get collected metrics
   * @returns {Array} Performance metrics
   */
  getMetrics() {
    return [...this.metrics];
  }

  /**
   * Clear metrics
   */
  clear() {
    this.metrics = [];
  }
}

// Export singleton instance
export const performanceMonitor = new PerformanceMonitor();

