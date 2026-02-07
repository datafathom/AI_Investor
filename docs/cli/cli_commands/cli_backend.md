# CLI Command: backend

## Description
Backend operations (Flask/Python)

## Main Help Output
```text

Command: backend
Description: Backend operations (Flask/Python)

Available subcommands:
  dev                  Start backend development server
  install              Install backend dependencies
  prod                 Start backend production server (Gunicorn)
  verify               Verify backend setup


```

## Subcommands

### Subcommand: `backend dev`
Start backend development server

#### Help Output
```text

Command: backend dev
Description: Start backend development server

Arguments:
  command               (Optional, Default: dev)

Flags:
  --port               Port to run server on (Default: 5050)
  --host               Host to bind to (Default: 127.0.0.1)


```

### Subcommand: `backend prod`
Start backend production server (Gunicorn)

#### Help Output
```text

Command: backend prod
Description: Start backend production server (Gunicorn)

Arguments:
  command               (Optional, Default: prod)

Flags:
  --workers            Number of worker processes (Default: 4)
  --port               Port to run server on (Default: 5050)


```

### Subcommand: `backend install`
Install backend dependencies

#### Help Output
```text

Command: backend install
Description: Install backend dependencies

Arguments:
  command               (Optional, Default: install)


```

### Subcommand: `backend verify`
Verify backend setup

#### Help Output
```text

Command: backend verify
Description: Verify backend setup

Arguments:
  command               (Optional, Default: verify)


```

