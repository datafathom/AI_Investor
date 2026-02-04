# Docker Troubleshooting Guide

## Permission Denied Error

If you see `permission denied while trying to connect to the Docker daemon socket`, you have two options:

### Option 1: Use sudo (Quick Fix)
```bash
sudo docker compose up -d --build
```

### Option 2: Add User to Docker Group (Permanent Fix)
```bash
# Add your user to the docker group
sudo usermod -aG docker $USER

# Log out and log back in (or restart your terminal session)
# Then verify:
groups | grep docker

# Now you can run without sudo:
docker compose up -d --build
```

## Common Issues

### Container Exits Immediately
Check the logs:
```bash
sudo docker compose logs -f
```

### Port Already in Use
If ports 3002 or 5176 are already in use:
```bash
# Check what's using the ports
sudo lsof -i :3002
sudo lsof -i :5176

# Stop the processes or change ports in docker-compose.yml
```

### Build Fails
```bash
# Clean up and rebuild
sudo docker compose down
sudo docker compose build --no-cache
sudo docker compose up -d
```

### Container Can't Access Files
Make sure the volumes are mounted correctly. Check `docker-compose.yml`:
```yaml
volumes:
  - .:/app
  - /app/node_modules
```

## Verifying the Setup

1. **Check if container is running:**
   ```bash
   sudo docker compose ps
   ```

2. **View logs:**
   ```bash
   sudo docker compose logs -f app
   ```

3. **Access the application:**
   - Frontend: http://localhost:5176
   - Backend: http://localhost:3002
   - Health Check: http://localhost:3002/api/health

4. **Stop the container:**
   ```bash
   sudo docker compose down
   ```

