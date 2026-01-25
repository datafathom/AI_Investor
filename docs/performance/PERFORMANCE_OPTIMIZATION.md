# Performance Optimization Guide

This guide covers performance optimization strategies for the AI Investor platform.

## Caching Strategy

### Redis Caching
- **Purpose**: Reduce database load and improve response times
- **TTL**: Default 1 hour, configurable per endpoint
- **Usage**: Use `@cached` decorator or `get_cache().get_or_set()`

### Example Usage

```python
from services.caching.performance_cache import cached, get_cache

# Decorator approach
@cached(ttl=3600)
def get_portfolio_data(user_id: str):
    # Expensive database query
    return db.query("SELECT * FROM portfolios WHERE user_id = ?", user_id)

# Manual caching
cache = get_cache()
data = cache.get_or_set(
    f"portfolio:{user_id}",
    lambda: expensive_computation(),
    ttl=3600
)
```

## Database Optimization

### Query Optimization
- Use indexes on frequently queried columns
- Limit result sets with LIMIT
- Use SELECT only needed columns
- Avoid N+1 queries (use JOINs)

### Connection Pooling
- Max connections: 20
- Reuse connections when possible
- Monitor connection pool usage

## Response Optimization

### Compression
- Gzip compression enabled for all responses
- Reduces bandwidth by 60-80%

### Cache Headers
- Static assets: 1 year cache
- API responses: Configurable (default 1 hour)
- Use `@cache_control` decorator

## Frontend Optimization

### Code Splitting
- Lazy load routes and components
- Split vendor bundles
- Dynamic imports for heavy libraries

### Asset Optimization
- Minify JavaScript and CSS
- Optimize images
- Use CDN for static assets

## Monitoring

### Performance Metrics
- Response time tracking
- Slow query logging (>1s)
- Cache hit/miss rates
- Database connection pool usage

### Tools
- Application Performance Monitoring (APM)
- Database query profiler
- Redis monitoring
- Browser DevTools

## Best Practices

1. **Cache Frequently Accessed Data**
   - User preferences
   - Market data (with short TTL)
   - Portfolio summaries

2. **Optimize Database Queries**
   - Use EXPLAIN ANALYZE
   - Add appropriate indexes
   - Avoid full table scans

3. **Minimize API Calls**
   - Batch requests when possible
   - Use WebSockets for real-time data
   - Implement pagination

4. **Optimize Frontend**
   - Lazy load components
   - Use virtual scrolling for large lists
   - Debounce search inputs

5. **Monitor Performance**
   - Set up alerts for slow requests
   - Track key performance metrics
   - Regular performance audits

## Performance Targets

- **API Response Time**: <200ms (p95)
- **Page Load Time**: <2s
- **Database Query Time**: <100ms (p95)
- **Cache Hit Rate**: >80%
