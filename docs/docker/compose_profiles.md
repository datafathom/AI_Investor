# Docker Compose Profiles

The AI Investor infrastructure is modular. Instead of running every service at once, you can use "Profiles" to start only the components you need.

## Available Profiles

While the default behavior is to start the full stack, the CLI supports specialized profiles:

| Profile | Services Included | Use Case |
| :--- | :--- | :--- |
| **`full`** | All (Postgres, Kafka, Redis, Neo4j) | Complete local development or single-node production. |
| **`storage`** | Postgres, Zookeeper | Offloading transactional data to a dedicated machine. |
| **`graph`** | Neo4j | Dedicated graph processing node. |
| **`streaming`** | Kafka, Zookeeper | High-bandwidth event pipeline isolation. |
| **`supplemental`** | Monitoring (Grafana, Prometheus) | Performance auditing and dashboarding. |

## CLI Integration

Profiles are managed via the `docker` namespace in the CLI:

### 1. Starting with a Profile
```powershell
# Start only the storage components
python cli.py docker up --profile storage
```

### 2. Rebuilding and Starting
```powershell
# Rebuild images and start the full stack
python cli.py docker up --profile full --build
```

## Technical Implementation

Profiles are controlled via the `--profile` flag in `docker compose`. When a profile is specified, Docker Compose only activates services that match that profile label in the `docker-compose.yml`.

> [!NOTE]
> Services without an explicit `profiles` key are considered "always-on" and will start regardless of the profile selected, unless they are dependencies of a specific excluded service.

## Volume Management

When switching profiles or performing a clean reset, you can purge volumes to start from a "Zero-State":

```powershell
# Stop all containers and delete all persisted data
python cli.py docker down --volumes
```
