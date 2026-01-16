# Deployment Guide

## Overview

This guide covers deploying the OS-Style Web GUI Boilerplate to production.

## Production Build

### Build the Application

```bash
# Build frontend
npm run build

# Output will be in dist/ directory
```

### Environment Variables

Create a `.env.production` file:

```env
NODE_ENV=production
PORT=3002
BACKEND_PORT=3002
VITE_BACKEND_PORT=3002
JWT_SECRET=your-production-secret-key
DATABASE_PATH=./database.sqlite
```

## Docker Deployment

### Production Dockerfile

The project includes a multi-stage Dockerfile for production:

```bash
# Build image
docker build -t boilerplate-app:latest .

# Run container
docker run -d \
  -p 3002:3002 \
  -e NODE_ENV=production \
  -e JWT_SECRET=your-secret \
  --name boilerplate-app \
  boilerplate-app:latest
```

### Docker Compose

```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "3002:3002"
    environment:
      - NODE_ENV=production
      - JWT_SECRET=${JWT_SECRET}
    volumes:
      - ./database.sqlite:/app/database.sqlite
```

```bash
docker compose up -d
```

## Server Deployment

### Node.js Server

1. **Install dependencies**
   ```bash
   npm install --production
   ```

2. **Build frontend**
   ```bash
   npm run build
   ```

3. **Start server**
   ```bash
   npm start
   ```

### Using PM2

```bash
# Install PM2
npm install -g pm2

# Start application
pm2 start server.js --name boilerplate-app

# Save PM2 configuration
pm2 save

# Setup startup script
pm2 startup
```

### Using systemd

Create `/etc/systemd/system/boilerplate-app.service`:

```ini
[Unit]
Description=Boilerplate App
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/path/to/app
ExecStart=/usr/bin/node server.js
Restart=always
Environment=NODE_ENV=production

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable boilerplate-app
sudo systemctl start boilerplate-app
```

## Database Setup

### SQLite (Default)

Database file is created automatically. For production:

1. **Backup database**
   ```bash
   cp database.sqlite database.sqlite.backup
   ```

2. **Initialize schema**
   ```bash
   npm run db:push
   ```

### PostgreSQL (Optional)

To use PostgreSQL instead of SQLite:

1. **Install PostgreSQL driver**
   ```bash
   npm install pg drizzle-orm
   ```

2. **Update database config**
   ```javascript
   // db/index.js
   import { drizzle } from 'drizzle-orm/node-postgres';
   import pg from 'pg';
   
   const pool = new pg.Pool({
     connectionString: process.env.DATABASE_URL
   });
   
   export const db = drizzle(pool);
   ```

## Reverse Proxy (Nginx)

### Nginx Configuration

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:3002;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    # WebSocket support
    location /socket.io/ {
        proxy_pass http://localhost:3002;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

### SSL with Let's Encrypt

```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal
sudo certbot renew --dry-run
```

## CI/CD

### GitHub Actions

The project includes a CI workflow (`.github/workflows/ci.yml`):

- Runs on push to main/develop
- Tests on Node.js 18.x and 20.x
- Builds Docker image
- Runs linter

### Custom CI/CD

Example GitHub Actions workflow:

```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
      - run: npm ci
      - run: npm run build
      - run: npm test
      - name: Deploy to server
        run: |
          # Your deployment commands
```

## Monitoring

### Health Checks

The server includes health check endpoints:

```bash
# Health check
curl http://localhost:3002/health

# API status
curl http://localhost:3002/api/status
```

### Logging

Logs are output to console. For production:

1. **Use a logging service** (e.g., Winston, Pino)
2. **Set up log aggregation** (e.g., ELK, Datadog)
3. **Monitor errors** (e.g., Sentry)

### Performance Monitoring

- Use the built-in Performance Monitor widget
- Set up APM (Application Performance Monitoring)
- Monitor Core Web Vitals

## Security

### Production Checklist

- [ ] Change JWT_SECRET to a strong random value
- [ ] Enable HTTPS/SSL
- [ ] Set secure CORS origins
- [ ] Use environment variables for secrets
- [ ] Enable rate limiting
- [ ] Set up firewall rules
- [ ] Keep dependencies updated
- [ ] Regular security audits

### Rate Limiting

Add rate limiting middleware:

```javascript
import rateLimit from 'express-rate-limit';

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100 // limit each IP to 100 requests per windowMs
});

app.use('/api/', limiter);
```

## Scaling

### Horizontal Scaling

For multiple instances:

1. **Use a shared database** (PostgreSQL recommended)
2. **Use Redis for sessions** (if needed)
3. **Use a load balancer** (Nginx, HAProxy)
4. **Sticky sessions for Socket.io** (if needed)

### Database Scaling

- Use connection pooling
- Set up read replicas
- Implement caching (Redis)
- Optimize queries

## Backup

### Database Backup

```bash
# Backup SQLite
cp database.sqlite backups/database-$(date +%Y%m%d).sqlite

# Automated backup script
#!/bin/bash
BACKUP_DIR="./backups"
DATE=$(date +%Y%m%d_%H%M%S)
cp database.sqlite "$BACKUP_DIR/database-$DATE.sqlite"
# Keep only last 7 days
find "$BACKUP_DIR" -name "database-*.sqlite" -mtime +7 -delete
```

### Automated Backups

Set up cron job:

```bash
# Edit crontab
crontab -e

# Add daily backup at 2 AM
0 2 * * * /path/to/backup-script.sh
```

## Troubleshooting

### Common Issues

**Port already in use:**
```bash
# Find process using port
lsof -i :3002
# Kill process
kill -9 <PID>
```

**Database locked:**
- Ensure only one instance is accessing the database
- Check for long-running transactions

**Memory issues:**
- Increase Node.js memory limit: `node --max-old-space-size=4096 server.js`
- Monitor memory usage
- Optimize code

**Socket.io connection issues:**
- Check CORS settings
- Verify WebSocket support
- Check firewall rules

## Support

For issues or questions:
- Check documentation
- Review error logs
- Check GitHub issues
- Contact support

