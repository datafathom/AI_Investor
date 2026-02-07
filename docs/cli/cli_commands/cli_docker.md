# CLI Command: docker

## Description
Docker infrastructure management

## Main Help Output
```text

Command: docker
Description: Docker infrastructure management

Available subcommands:
  down                 Stop Docker containers
  logs                 View/Follow Docker container logs
  ps                   Show Docker container status (formatted table)
  status               Show Docker container status
  up                   Start Docker containers (localhost only)


```

## Subcommands

### Subcommand: `docker up`
Start Docker containers (localhost only)

#### Help Output
```text

Command: docker up
Description: Start Docker containers (localhost only)

Flags:
  --build              Rebuild images before starting (Default: False)
  --profile            Docker Compose profile to run (e.g. storage, graph, full) (Default: full)


```

### Subcommand: `docker down`
Stop Docker containers

#### Help Output
```text

Command: docker down
Description: Stop Docker containers

Flags:
  -v, --volumes            Purge all mounted volumes (Default: False)


```

### Subcommand: `docker status`
Show Docker container status

#### Help Output
```text

Command: docker status
Description: Show Docker container status


```

### Subcommand: `docker logs`
View/Follow Docker container logs

#### Help Output
```text

Command: docker logs
Description: View/Follow Docker container logs

Flags:
  --service            Specific service to log (e.g. backend, frontend) (Default: )
  --follow             Follow log output (Default: True)


```

### Subcommand: `docker ps`
Show Docker container status (formatted table)

#### Help Output
```text

Command: docker ps
Description: Show Docker container status (formatted table)


```

