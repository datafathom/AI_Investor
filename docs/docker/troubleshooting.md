# Docker Troubleshooting & Maintenance

This guide covers common issues and maintenance tasks for the AI Investor Docker infrastructure.

## Common Issues

### 1. Port Conflicts (address already in use)
If you see an error like `bind: address already in use`, another process is already listening on a required port (e.g., 5432 for Postgres).
- **Fix**: Run `python cli.py stop-all` to ensure no orphaned processes are holding ports, or check for other Docker instances (`docker ps`).

### 2. Volume Corruption / State Mismatch
If the database fails to start or shows schema errors after a major update, you may need to reset the data layer.
- **Fix**: Run `python cli.py docker down --volumes`. This deletes all data in the `data/` directory and allows Docker to recreate it from scratch.

### 3. Kafka Connectivity
Kafka requires both Zookeeper and correct `ADVERTISED_LISTENERS`. If agents cannot connect:
- **Fix**: Check `DOCKER_BIND_IP` in `.env`. If it's incorrect, Kafka will advertise the wrong address to the agents.

## Maintenance Commands

### Viewing Logs
To stream logs for all services:
```powershell
python cli.py docker logs
```
To follow logs for a specific service (e.g., `postgres`):
```powershell
python cli.py docker logs --service postgres
```

### Checking Health
Use the formatted table view to see which containers are healthy:
```powershell
python cli.py docker status
```

## Performance Tuning

The `docker-compose.yml` includes resource limits to prevent any single container from overwhelming the host:
- **Postgres**: Limited to 1GB RAM.
- **Kafka**: Limited to 400MB RAM.
- **Neo4j**: Limited to 512M RAM.

If you are dealing with extremely large datasets (e.g., 10+ years of high-frequency tick data), you may need to increase these limits in `infra/docker-compose.yml` based on your host's available resources.
