# Load Testing Guide

This guide explains how to run load and performance tests using k6.

## Overview

Load tests simulate multiple users accessing the API simultaneously to measure performance under load.

## Prerequisites

- k6 installed (https://k6.io/docs/getting-started/installation/)
- Backend API running
- Test user account

## Running Load Tests

### Basic Load Test

```bash
./scripts/testing/run_load_tests.sh load_test_scenarios
```

### Performance Benchmarks

```bash
./scripts/testing/run_load_tests.sh performance_benchmarks
```

### Custom Configuration

```bash
k6 run tests/load/load_test_scenarios.js \
  --vus 50 \
  --duration 5m \
  --env API_URL=http://localhost:5050
```

## Test Scenarios

### Load Test Scenarios
- Ramp up to 50 users over 2 minutes
- Stay at 50 users for 5 minutes
- Ramp up to 100 users over 2 minutes
- Stay at 100 users for 5 minutes
- Ramp down to 0 users

### Performance Benchmarks
- 10 virtual users
- 1 minute duration
- Tests specific endpoints

## Performance Targets

### Response Times
- Health check: < 50ms (p95)
- Portfolio API: < 200ms (p95)
- Analytics API: < 500ms (p95)
- Search API: < 300ms (p95)

### Error Rates
- < 1% error rate
- < 1% failed requests

### Throughput
- Handle 100+ concurrent users
- 1000+ requests per minute

## Interpreting Results

### Key Metrics

- **http_req_duration**: Request duration
- **http_req_failed**: Failed request rate
- **vus**: Virtual users
- **iterations**: Total requests

### Thresholds

Tests fail if thresholds are exceeded:
- p95 response time > 500ms
- p99 response time > 1000ms
- Error rate > 1%

## CI Integration

Load tests run in GitHub Actions:
- On main branch
- Scheduled (weekly)
- Manual trigger

Results are uploaded as artifacts.

## Customizing Tests

### Add New Scenarios

Edit `tests/load/load_test_scenarios.js`:

```javascript
// Add new API call
res = http.get(`${BASE_URL}/api/v1/new-endpoint`, { headers });
check(res, {
  'new endpoint status is 200': (r) => r.status === 200,
});
```

### Adjust Load

Modify `options.stages`:

```javascript
stages: [
  { duration: '2m', target: 100 },  // Ramp to 100 users
  { duration: '5m', target: 100 },  // Stay at 100
  { duration: '2m', target: 0 },    // Ramp down
],
```

## Troubleshooting

### Tests Fail

1. Check API is running
2. Verify test user credentials
3. Check network connectivity
4. Review error logs

### Performance Issues

1. Check database performance
2. Review query optimization
3. Check cache hit rates
4. Monitor resource usage

## Best Practices

1. **Start Small**: Begin with low load, increase gradually
2. **Monitor Resources**: Watch CPU, memory, database
3. **Test Realistic Scenarios**: Match production usage patterns
4. **Regular Testing**: Run load tests regularly
5. **Document Results**: Keep performance baselines

## Next Steps

- [ ] Add more load test scenarios
- [ ] Test peak load scenarios
- [ ] Add stress testing
- [ ] Add spike testing
- [ ] Monitor production performance
