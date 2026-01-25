/**
 * Performance Benchmark Tests
 * Tests specific performance scenarios
 */

import http from 'k6/http';
import { check } from 'k6';
import { Trend } from 'k6/metrics';

const BASE_URL = __ENV.API_URL || 'http://localhost:5050';

export const options = {
  vus: 10,
  duration: '1m',
  thresholds: {
    http_req_duration: ['p(95)<200', 'p(99)<500'],
  },
};

export default function () {
  const headers = {
    'Content-Type': 'application/json',
  };

  // Benchmark 1: Health Check (should be fastest)
  let res = http.get(`${BASE_URL}/api/v1/health`, { headers });
  check(res, {
    'health check < 50ms': (r) => r.timings.duration < 50,
  });

  // Benchmark 2: Portfolio API
  res = http.get(`${BASE_URL}/api/v1/portfolio`, { headers });
  check(res, {
    'portfolio < 200ms': (r) => r.timings.duration < 200,
  });

  // Benchmark 3: Analytics API
  res = http.get(`${BASE_URL}/api/v1/analytics/attribution/portfolio_1?start_date=2024-01-01&end_date=2024-12-31`, { headers });
  check(res, {
    'analytics < 500ms': (r) => r.timings.duration < 500,
  });
}
