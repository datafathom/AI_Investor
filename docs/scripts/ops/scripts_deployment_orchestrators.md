# Script: swap_deploy.py / deploy.ps1

## Overview
These scripts handle the orchestration of the deployment process.

## Core Functionality
- **Blue-Green Logic**: `swap_deploy.py` manages the switching of traffic between two instances (Blue and Green) of the application services, allowing for zero-downtime updates.
- **PowerShell Orchestration**: `deploy.ps1` provides a Windows-compatible entry point for the local deployment workflow, including environment setup, build triggering, and script calling.

## Status
**Essential (Deployment)**: provides the core logic for the project's automated deployment strategy.
