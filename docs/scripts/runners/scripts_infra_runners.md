# Runners: System and Infrastructure

## Overview
Infrastructure runners provide the core process management for starting, stopping, and monitoring the various layers of the AI Investor stack.

## Key Runners

### [backend_runner.py](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/scripts/runners/backend_runner.py)
Orchestrates the startup of the FastAPI gateway. It handles environment variable loading, Uvicorn configuration, and ensures that prerequisite services (Postgres, Redis) are reachable before launching the web process.

### [frontend_runner.py](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/scripts/runners/frontend_runner.py) / [frontend_control.py](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/scripts/runners/frontend_control.py)
Manages the Vite development server and production build previews. `frontend_control.py` provides lower-level process management, while `frontend_runner.py` is the standard entry point for developers.

### [database_runner.py](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/scripts/runners/database_runner.py)
A specialized runner for database-related tasks, including migration checks, seed data application, and connection pool warming.

### [docker_control.py](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/scripts/runners/docker_control.py)
Coordinates with the local Docker daemon to start and stop containerized services (Postgres, Neo4j, Redis, Kafka, Zookeeper). It ensures the correct containers are running and healthy.

### [system_control.py](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/scripts/runners/system_control.py)
The master orchestrator for the entire stack. It provides commands to start all services in the correct order (Infra -> Backend -> Workers -> Frontend).

## Status
**Essential (Runtime)**: these runners form the operational backbone of the development and production environments.
