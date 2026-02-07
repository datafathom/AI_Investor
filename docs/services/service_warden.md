# Backend Service: Warden (The Scheduler)

## Overview
The **Warden Service** manages scheduled jobs and automated routines. It acts as the platform's internal job scheduler, running background tasks on defined intervals.

## Core Components

### 1. Scheduler (`scheduler.py`)
- **Cron-like Scheduling**: Triggers jobs at specified intervals.
- **Job Registry**: Maintains a list of registered background tasks.

### 2. Routine Runner (`routine_runner.py`)
- Executes registered routines sequentially or in parallel.

### 3. Circuit Breaker (`circuit_breaker.py`)
- Halts job execution if failures exceed a threshold.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used | Frontend Status |
| :--- | :--- | :--- | :--- |
| **Ops Dashboard** | Job Monitor | `scheduler` | **Missing** |
