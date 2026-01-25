# Production Deployment Checklist

Complete checklist for deploying AI Investor to production.

## Pre-Deployment

### Infrastructure
- [ ] Production servers provisioned
- [ ] Domain names configured
- [ ] SSL certificates obtained (Let's Encrypt)
- [ ] DNS records configured
- [ ] Load balancer configured
- [ ] CDN configured (if applicable)

### Environment Setup
- [ ] `.env.production` file created
- [ ] All environment variables set
- [ ] Secrets configured in Vault/AWS Secrets Manager
- [ ] Database credentials configured
- [ ] API keys configured
- [ ] Email service configured

### Database
- [ ] Production database created
- [ ] Database migrations tested
- [ ] Backup strategy configured
- [ ] Database monitoring enabled
- [ ] Connection pooling configured

### Security
- [ ] Security audit completed
- [ ] Penetration testing done
- [ ] SSL/TLS configured
- [ ] Security headers enabled
- [ ] Rate limiting configured
- [ ] Firewall rules configured
- [ ] DDoS protection enabled

---

## Deployment Steps

### 1. Build Docker Images

```bash
docker build -f infra/Dockerfile.backend.prod -t ai-investor-backend:latest .
docker build -f frontend2/Dockerfile.prod -t ai-investor-frontend:latest ./frontend2
```

### 2. Run Database Migrations

```bash
python scripts/database/migrate.py up
```

### 3. Deploy Services

```bash
docker-compose -f infra/docker-compose.prod.yml up -d
```

### 4. Verify Deployment

```bash
# Health checks
curl https://api.ai-investor.com/api/v1/health
curl https://ai-investor.com/health

# Check services
docker-compose -f infra/docker-compose.prod.yml ps
```

---

## Post-Deployment

### Verification
- [ ] All services healthy
- [ ] Health checks passing
- [ ] API endpoints responding
- [ ] Frontend loading correctly
- [ ] Database connections working
- [ ] Redis cache working
- [ ] WebSocket connections working

### Monitoring
- [ ] Error tracking operational (Sentry)
- [ ] Log aggregation working
- [ ] Metrics collection active
- [ ] Alerts configured
- [ ] Dashboards accessible

### Testing
- [ ] Smoke tests passing
- [ ] Critical user flows working
- [ ] API endpoints functional
- [ ] Authentication working
- [ ] Trading flow working

---

## Rollback Plan

If deployment fails:

1. **Stop New Deployment**
   ```bash
   docker-compose -f infra/docker-compose.prod.yml down
   ```

2. **Rollback Database** (if needed)
   ```bash
   python scripts/database/migration_manager.py rollback --migration-id <last_migration>
   ```

3. **Restore Previous Version**
   ```bash
   ./scripts/deployment/rollback.sh
   ```

4. **Verify Rollback**
   ```bash
   curl https://api.ai-investor.com/api/v1/health
   ```

---

## Monitoring Checklist

### First 24 Hours
- [ ] Monitor error rates
- [ ] Check response times
- [ ] Verify user registrations
- [ ] Monitor database performance
- [ ] Check cache hit rates
- [ ] Review security logs

### First Week
- [ ] Review performance metrics
- [ ] Check user feedback
- [ ] Monitor resource usage
- [ ] Review error patterns
- [ ] Optimize slow queries
- [ ] Adjust rate limits if needed

---

## Emergency Contacts

- **On-Call Engineer**: [Contact Info]
- **DevOps Team**: [Contact Info]
- **Security Team**: [Contact Info]
- **Database Admin**: [Contact Info]

---

**Last Updated**: 2026-01-21
