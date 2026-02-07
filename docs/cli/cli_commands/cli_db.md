# CLI Command: db

## Description
Database maintenance and management.

## Main Help Output
```text

Command: db
Description: Database maintenance and management.

Available subcommands:
  backup               Backup database.
  migrate              Run database migrations (up/down).
  reinit               DESTRUCTIVE: Full infrastructure reset (Nuke data, Start services, Migrate, Seed).
  restore              Restore database from backup.
  status               Check migration status.


```

## Subcommands

### Subcommand: `db migrate`
Run database migrations (up/down).

#### Help Output
```text

Command: db migrate
Description: Run database migrations (up/down).

Arguments:
  direction            Migration direction: up or down (Optional, Default: up)

Flags:
  --id                 Migration ID (required for rollback) (Default: None)


```

### Subcommand: `db backup`
Backup database.

#### Help Output
```text

Command: db backup
Description: Backup database.

Flags:
  --type               Backup type: postgres, neo4j, or all (Default: all)


```

### Subcommand: `db restore`
Restore database from backup.

#### Help Output
```text

Command: db restore
Description: Restore database from backup.

Flags:
  --file               Backup file path (Default: None)
  --type               Database type: postgres or neo4j (Default: postgres)


```

### Subcommand: `db status`
Check migration status.

#### Help Output
```text

Command: db status
Description: Check migration status.


```

### Subcommand: `db reinit`
DESTRUCTIVE: Full infrastructure reset (Nuke data, Start services, Migrate, Seed).

#### Help Output
```text

Command: db reinit
Description: DESTRUCTIVE: Full infrastructure reset (Nuke data, Start services, Migrate, Seed).


```

