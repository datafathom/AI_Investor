# CLI Command: infra

## Description
Infrastructure and LAN distribution management

## Main Help Output
```text

Command: infra
Description: Infrastructure and LAN distribution management

Available subcommands:
  cert-generate        Generate SSL certificates for LAN IP or Service
  init-node            Bootstrap a new node in the distributed cluster
  set-host             Configure .env for a specific service host
  set-lan-ip           Configure .env with global LAN Box IP mapping


```

## Subcommands

### Subcommand: `infra cert-generate`
Generate SSL certificates for LAN IP or Service

#### Help Output
```text

Command: infra cert-generate
Description: Generate SSL certificates for LAN IP or Service

Flags:
  --ip                 Target LAN IP (Default: )
  --service            Target service (pulls IP from .env) (Default: )


```

### Subcommand: `infra set-lan-ip`
Configure .env with global LAN Box IP mapping

#### Help Output
```text

Command: infra set-lan-ip
Description: Configure .env with global LAN Box IP mapping

Arguments:
  ip                   IP address of the LAN Box (Required)


```

### Subcommand: `infra set-host`
Configure .env for a specific service host

#### Help Output
```text

Command: infra set-host
Description: Configure .env for a specific service host

Arguments:
  service              Service name (e.g. postgres, neo4j) (Required)
  ip                   Host IP for the service (Required)


```

### Subcommand: `infra init-node`
Bootstrap a new node in the distributed cluster

#### Help Output
```text

Command: infra init-node
Description: Bootstrap a new node in the distributed cluster

Arguments:
  ip                   IP address of this node (Required)

Flags:
  --roles              Service roles to run (e.g. database, graph, full) (Default: full)


```

