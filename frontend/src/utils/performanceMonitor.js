/**
 * Performance Monitor
 * 
 * Tracks Core Web Vitals and performance metrics.
 * Provides performance dashboard data.
 */

class PerformanceMonitor {
  constructor() {
    this.metrics = {
      LCP: null, // Largest Contentful Paint
      FID: null, // First Input Delay
      CLS: null, // Cumulative Layout Shift
      FCP: null, // First Contentful Paint
      TTFB: null, // Time to First Byte
    };
    this.observers = [];
    this.listeners = new Set();
    this.init();
  }

  init() {
    if (typeof window === 'undefined' || !window.performance) {
      return;
    }

    // Measure TTFB
    this.measureTTFB();

    // Measure FCP
    this.measureFCP();

    // Measure LCP
    this.measureLCP();

    // Measure CLS
    this.measureCLS();

    // Measure FID
    this.measureFID();
  }

  measureTTFB() {
    const navigation = performance.getEntriesByType('navigation')[0];
    if (navigation) {
      this.metrics.TTFB = navigation.responseStart - navigation.requestStart;
      this.emit('metric:ttfb', this.metrics.TTFB);
    }
  }

  measureFCP() {
    const paintEntries = performance.getEntriesByType('paint');
    const fcpEntry = paintEntries.find(entry => entry.name === 'first-contentful-paint');
    if (fcpEntry) {
      this.metrics.FCP = fcpEntry.startTime;
      this.emit('metric:fcp', this.metrics.FCP);
    }
  }

  measureLCP() {
    if (!('PerformanceObserver' in window)) return;

    try {
      const observer = new PerformanceObserver((list) => {
        const entries = list.getEntries();
        const lastEntry = entries[entries.length - 1];
        this.metrics.LCP = lastEntry.renderTime || lastEntry.loadTime;
        this.emit('metric:lcp', this.metrics.LCP);
      });

      observer.observe({ entryTypes: ['largest-contentful-paint'] });
      this.observers.push(observer);
    } catch (error) {
      console.warn('LCP measurement not supported:', error);
    }
  }

  measureCLS() {
    if (!('PerformanceObserver' in window)) return;

    try {
      let clsValue = 0;
      const observer = new PerformanceObserver((list) => {
        for (const entry of list.getEntries()) {
          if (!entry.hadRecentInput) {
            clsValue += entry.value;
          }
        }
        this.metrics.CLS = clsValue;
        this.emit('metric:cls', this.metrics.CLS);
      });

      observer.observe({ entryTypes: ['layout-shift'] });
      this.observers.push(observer);
    } catch (error) {
      console.warn('CLS measurement not supported:', error);
    }
  }

  measureFID() {
    if (!('PerformanceObserver' in window)) return;

    try {
      const observer = new PerformanceObserver((list) => {
        for (const entry of list.getEntries()) {
          this.metrics.FID = entry.processingStart - entry.startTime;
          this.emit('metric:fid', this.metrics.FID);
        }
      });

      observer.observe({ entryTypes: ['first-input'] });
      this.observers.push(observer);
    } catch (error) {
      console.warn('FID measurement not supported:', error);
    }
  }

  /**
   * Get all metrics
   */
  getMetrics() {
    return { ...this.metrics };
  }

  /**
   * Get metric score (good, needs-improvement, poor)
   */
  getMetricScore(metric, value) {
    const thresholds = {
      LCP: { good: 2500, poor: 4000 },
      FID: { good: 100, poor: 300 },
      CLS: { good: 0.1, poor: 0.25 },
      FCP: { good: 1800, poor: 3000 },
      TTFB: { good: 800, poor: 1800 },
    };

    const threshold = thresholds[metric];
    if (!threshold) return 'unknown';

    if (value <= threshold.good) return 'good';
    if (value <= threshold.poor) return 'needs-improvement';
    return 'poor';
  }

  /**
   * Get overall performance score
   */
  getOverallScore() {
    const scores = Object.entries(this.metrics)
      .filter(([_, value]) => value !== null)
      .map(([metric, value]) => this.getMetricScore(metric, value));

    if (scores.length === 0) return 'unknown';

    const goodCount = scores.filter(s => s === 'good').length;
    const needsImprovementCount = scores.filter(s => s === 'needs-improvement').length;
    const poorCount = scores.filter(s => s === 'poor').length;

    if (poorCount > 0) return 'poor';
    if (needsImprovementCount > 0) return 'needs-improvement';
    return 'good';
  }

  /**
   * Cleanup
   */
  disconnect() {
    this.observers.forEach(observer => observer.disconnect());
    this.observers = [];
  }

  /**
   * Event listener management
   */
  on(event, callback) {
    this.listeners.add({ event, callback });
  }

  off(event, callback) {
    this.listeners.forEach(listener => {
      if (listener.event === event && listener.callback === callback) {
        this.listeners.delete(listener);
      }
    });
  }

  emit(event, ...args) {
    this.listeners.forEach(listener => {
      if (listener.event === event) {
        listener.callback(...args);
      }
    });
  }
}

// Singleton instance
const performanceMonitor = new PerformanceMonitor();

export default performanceMonitor;

