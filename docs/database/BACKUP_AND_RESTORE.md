# Database Backup & Disaster Recovery Guide

This guide explains how to backup and restore databases for the AI Investor platform.

## Overview

The backup system supports:
- **PostgreSQL**: Full database backups with compression
- **Neo4j**: Graph database exports
- **Automated Scheduling**: Cron-based automated backups
- **Retention Management**: Automatic cleanup of old backups
- **Cloud Storage**: Optional S3 integration

## Quick Start

### Manual Backup

**Backup all databases:**
```bash
python scripts/database/backup.py --all
```

**Backup PostgreSQL only:**
```bash
python scripts/database/backup.py --postgres
```

**Backup Neo4j only:**
```bash
python scripts/database/backup.py --neo4j
```

### Manual Restore

**Restore from latest backup:**
```bash
python scripts/database/restore.py --postgres --latest
python scripts/database/restore.py --neo4j --latest
```

**Restore from specific backup:**
```bash
python scripts/database/restore.py --postgres --backup-file backups/postgres_ai_investor_20260121_120000.sql
```

## Automated Backups

### Cron Setup

Add to crontab (`crontab -e`):
```bash
# Daily backup at 2 AM
0 2 * * * /path/to/scripts/database/schedule_backups.sh

# Weekly full backup on Sunday at 1 AM
0 1 * * 0 /path/to/scripts/database/schedule_backups.sh
```

### Systemd Timer (Alternative)

Create `/etc/systemd/system/ai-investor-backup.service`:
```ini
[Unit]
Description=AI Investor Database Backup
After=network.target

[Service]
Type=oneshot
User=ai-investor
WorkingDirectory=/opt/ai-investor
EnvironmentFile=/opt/ai-investor/.env.production
ExecStart=/opt/ai-investor/scripts/database/schedule_backups.sh
```

Create `/etc/systemd/system/ai-investor-backup.timer`:
```ini
[Unit]
Description=AI Investor Database Backup Timer
Requires=ai-investor-backup.service

[Timer]
OnCalendar=daily
OnCalendar=02:00
Persistent=true

[Install]
WantedBy=timers.target
```

Enable and start:
```bash
sudo systemctl enable ai-investor-backup.timer
sudo systemctl start ai-investor-backup.timer
```

## Backup Configuration

### Environment Variables

Set in `.env.production`:
```bash
# PostgreSQL
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
POSTGRES_DB=ai_investor

# Neo4j
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password

# Backup Settings
BACKUP_DIR=/opt/ai-investor/backups
BACKUP_KEEP_DAYS=30
BACKUP_S3_BUCKET=ai-investor-backups  # Optional
```

## Backup Storage

### Local Storage

Backups are stored in the `backups/` directory by default:
```
backups/
├── postgres_ai_investor_20260121_120000.sql
├── postgres_ai_investor_20260121_120000.dump
├── neo4j_20260121_120000.cypher
└── backup_metadata_20260121_120000.json
```

### Cloud Storage (S3)

To enable S3 backups, set `BACKUP_S3_BUCKET` and configure AWS credentials:

```bash
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
export BACKUP_S3_BUCKET=ai-investor-backups
```

The backup script will automatically sync backups to S3.

## Restore Procedures

### PostgreSQL Restore

**1. Stop the application:**
```bash
docker-compose down
# or
systemctl stop ai-investor
```

**2. Restore database:**
```bash
python scripts/database/restore.py \
    --postgres \
    --latest \
    --drop-existing
```

**3. Verify restore:**
```bash
psql -h localhost -U postgres -d ai_investor -c "SELECT COUNT(*) FROM users;"
```

**4. Restart application:**
```bash
docker-compose up -d
# or
systemctl start ai-investor
```

### Neo4j Restore

**1. Stop Neo4j:**
```bash
docker-compose stop neo4j
# or
systemctl stop neo4j
```

**2. Restore database:**
```bash
python scripts/database/restore.py \
    --neo4j \
    --latest \
    --clear-existing
```

**3. Restart Neo4j:**
```bash
docker-compose start neo4j
# or
systemctl start neo4j
```

## Disaster Recovery

### Full System Recovery

**1. Provision new infrastructure:**
- Set up servers
- Install Docker/PostgreSQL/Neo4j
- Configure networking

**2. Restore databases:**
```bash
# Download backups from S3 or backup storage
aws s3 sync s3://ai-investor-backups/backups/ ./backups/

# Restore PostgreSQL
python scripts/database/restore.py --postgres --latest --drop-existing

# Restore Neo4j
python scripts/database/restore.py --neo4j --latest --clear-existing
```

**3. Restore application:**
```bash
# Deploy application code
git clone https://github.com/your-org/ai-investor.git
cd ai-investor

# Configure environment
cp .env.production.template .env.production
# Edit .env.production with production values

# Start services
docker-compose -f infra/docker-compose.prod.yml up -d
```

**4. Verify recovery:**
- Check health endpoints
- Verify database connectivity
- Test critical functionality

## Backup Verification

### List Backups

```bash
python scripts/database/backup.py --list
```

### Verify Backup Integrity

**PostgreSQL:**
```bash
# Test restore to a temporary database
createdb test_restore
python scripts/database/restore.py \
    --postgres \
    --backup-file backups/postgres_ai_investor_20260121_120000.sql \
    --pg-database test_restore
dropdb test_restore
```

**Neo4j:**
```bash
# Check Cypher file syntax
head -n 100 backups/neo4j_20260121_120000.cypher
```

## Backup Retention

### Automatic Cleanup

Backups older than 30 days are automatically removed:
```bash
python scripts/database/backup.py --cleanup 30
```

### Manual Cleanup

```bash
# Remove backups older than 7 days
python scripts/database/backup.py --cleanup 7

# Remove backups older than 90 days
python scripts/database/backup.py --cleanup 90
```

## Best Practices

1. **Regular Backups**: Run daily backups at minimum
2. **Off-Site Storage**: Store backups in S3 or other cloud storage
3. **Test Restores**: Regularly test restore procedures
4. **Monitor Backup Success**: Set up alerts for backup failures
5. **Document Recovery Procedures**: Keep recovery procedures documented
6. **Version Control**: Keep backup scripts in version control
7. **Encryption**: Encrypt backups containing sensitive data
8. **Retention Policy**: Define and enforce retention policies

## Troubleshooting

### Backup Fails

**Check database connectivity:**
```bash
psql -h localhost -U postgres -d ai_investor -c "SELECT 1;"
```

**Check disk space:**
```bash
df -h backups/
```

**Check permissions:**
```bash
ls -la backups/
```

### Restore Fails

**Check backup file integrity:**
```bash
file backups/postgres_ai_investor_20260121_120000.sql
```

**Check database exists:**
```bash
psql -h localhost -U postgres -l | grep ai_investor
```

**Check logs:**
```bash
tail -f /var/log/ai-investor/backup.log
```

## Monitoring

### Backup Success Alerts

Set up monitoring to alert on backup failures:
```bash
# In schedule_backups.sh, add:
if [ $? -ne 0 ]; then
    # Send alert via email, Slack, PagerDuty, etc.
    echo "Backup failed!" | mail -s "Backup Alert" admin@example.com
fi
```

### Backup Size Monitoring

Monitor backup sizes to detect anomalies:
```bash
du -sh backups/
ls -lh backups/ | tail -5
```

## Next Steps

- [ ] Set up automated backups
- [ ] Configure S3 storage
- [ ] Test restore procedures
- [ ] Set up backup monitoring
- [ ] Document recovery procedures
- [ ] Train team on recovery procedures
