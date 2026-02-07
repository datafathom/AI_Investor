# CLI Command: deploy

## Description
Deployment operations

## Main Help Output
```text

Command: deploy
Description: Deployment operations

Available subcommands:
  build                Build Docker images
  health               Check deployment health
  prod                 Deploy to production
  rollback             Rollback deployment


```

## Subcommands

### Subcommand: `deploy prod`
Deploy to production

#### Help Output
```text

Command: deploy prod
Description: Deploy to production

Arguments:
  command               (Optional, Default: prod)

Flags:
  --env                Environment file path (Default: None)


```

### Subcommand: `deploy rollback`
Rollback deployment

#### Help Output
```text

Command: deploy rollback
Description: Rollback deployment

Arguments:
  command               (Optional, Default: rollback)


```

### Subcommand: `deploy build`
Build Docker images

#### Help Output
```text

Command: deploy build
Description: Build Docker images

Arguments:
  command               (Optional, Default: build)


```

### Subcommand: `deploy health`
Check deployment health

#### Help Output
```text

Command: deploy health
Description: Check deployment health

Arguments:
  command               (Optional, Default: health)


```

