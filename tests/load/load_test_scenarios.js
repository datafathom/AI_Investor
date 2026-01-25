/**
 * Load Test Scenarios using k6
 * Tests system performance under load
 */

import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate, Trend } from 'k6/metrics';

// Custom metrics
const errorRate = new Rate('errors');
const apiResponseTime = new Trend('api_response_time');

export const options = {
  stages: [
    { duration: '2m', target: 50 },   // Ramp up to 50 users
    { duration: '5m', target: 50 },    // Stay at 50 users
    { duration: '2m', target: 100 },  // Ramp up to 100 users
    { duration: '5m', target: 100 },   // Stay at 100 users
    { duration: '2m', target: 0 },     // Ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<500', 'p(99)<1000'], // 95% < 500ms, 99% < 1s
    http_req_failed: ['rate<0.01'],                 // < 1% errors
    errors: ['rate<0.01'],
  },
};

const BASE_URL = __ENV.API_URL || 'http://localhost:5050';
const API_KEY = __ENV.API_KEY || 'test-api-key';

export function setup() {
  // Setup: Create test user and get auth token
  const loginRes = http.post(`${BASE_URL}/api/v1/auth/login`, JSON.stringify({
    email: __ENV.TEST_EMAIL || 'loadtest@example.com',
    password: __ENV.TEST_PASSWORD || 'TestPassword123!',
  }), {
    headers: { 'Content-Type': 'application/json' },
  });

  if (loginRes.status !== 200) {
    console.error('Failed to login:', loginRes.body);
    return null;
  }

  const token = JSON.parse(loginRes.body).data.token;
  return { token };
}

export default function (data) {
  if (!data || !data.token) {
    return;
  }

  const headers = {
    'Authorization': `Bearer ${data.token}`,
    'Content-Type': 'application/json',
  };

  // Scenario 1: Health Check
  let res = http.get(`${BASE_URL}/api/v1/health`, { headers });
  check(res, {
    'health check status is 200': (r) => r.status === 200,
    'health check response time < 100ms': (r) => r.timings.duration < 100,
  }) || errorRate.add(1);
  apiResponseTime.add(res.timings.duration);
  sleep(1);

  // Scenario 2: Get Portfolio
  res = http.get(`${BASE_URL}/api/v1/portfolio`, { headers });
  check(res, {
    'portfolio status is 200': (r) => r.status === 200,
    'portfolio response time < 500ms': (r) => r.timings.duration < 500,
    'portfolio has data': (r) => JSON.parse(r.body).success === true,
  }) || errorRate.add(1);
  apiResponseTime.add(res.timings.duration);
  sleep(1);

  // Scenario 3: Get Analytics
  res = http.get(`${BASE_URL}/api/v1/analytics/attribution/portfolio_1?start_date=2024-01-01&end_date=2024-12-31`, { headers });
  check(res, {
    'analytics status is 200': (r) => r.status === 200,
    'analytics response time < 1000ms': (r) => r.timings.duration < 1000,
  }) || errorRate.add(1);
  apiResponseTime.add(res.timings.duration);
  sleep(1);

  // Scenario 4: Search Symbols
  res = http.get(`${BASE_URL}/api/v1/market/search?q=AAPL`, { headers });
  check(res, {
    'search status is 200': (r) => r.status === 200,
    'search response time < 300ms': (r) => r.timings.duration < 300,
  }) || errorRate.add(1);
  apiResponseTime.add(res.timings.duration);
  sleep(1);
}

export function teardown(data) {
  // Cleanup if needed
}
