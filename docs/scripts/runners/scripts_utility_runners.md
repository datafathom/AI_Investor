# Runners: Utility and Integration

## Overview
This set of runners provides essential utility functions and manages integrations with external notification and data systems.

## Key Runners

### [slack_runner.py](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/scripts/runners/slack_runner.py)
Controls the Slack integration bot. Provides commands to start, stop, and verify the bot's health.

### [seed_db.py](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/scripts/runners/seed_db.py)
Populates the database with foundational data (Departments, Roles, Base Users) and mock data for development (Clients, Portfolios, Transactions).

### [pip_runner.py](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/scripts/runners/pip_runner.py)
A managed wrapper for `pip` that ensures packages are installed within the project's virtual environment and automatically updates `requirements.txt` upon completion.

### [speed_test_runner.py](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/scripts/runners/speed_test_runner.py)
Benchmarks the response times of the API gateway and critical background workers, providing performance alerts if regression is detected.

## Status
**Essential (Utility)**: provides the supporting functions needed for a robust development lifecycle and real-time operational awareness.
