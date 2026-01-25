
import http from 'k6/http';
import { check, sleep } from 'k6';

/**
 * AI Investor Load Test Script
 * Simulates virtual users (VUs) interacting with critical API endpoints.
 */

export const options = {
  stages: [
    { duration: '30s', target: 20 }, // Ramp up to 20 users
    { duration: '1m', target: 20 },  // Stay at 20 users
    { duration: '30s', target: 0 },  // Ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'], // 95% of requests must complete below 500ms
  },
};

const BASE_URL = __ENV.BASE_URL || 'http://localhost:5050';

export default function () {
  // 1. Health Check
  const healthRes = http.get(`${BASE_URL}/health`);
  check(healthRes, { 'status is 200': (r) => r.status === 200 });

  // 2. Fetch Market Rates (Cached)
  const ratesRes = http.get(`${BASE_URL}/api/v1/settlement/rates`, {
      headers: { 'Authorization': 'Bearer demo-token' } // Mock token for load test bypass if needed
  });
  check(ratesRes, { 'rates status is 200': (r) => r.status === 200 });

  // 3. Simulated think time
  sleep(1);
}
