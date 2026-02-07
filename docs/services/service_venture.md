# Backend Service: Venture (The Cap Table)

## Overview
The **Venture Service** manages capitalization tables for startup investments, tracking ownership stakes, dilution, and vesting schedules.

## Core Components

### 1. Cap Table Service (`cap_table_service.py`)
- **Ownership Tracking**: Records share classes, options, and SAFEs.
- **Dilution Modeling**: Projects dilution from future funding rounds.
- **Exit Scenarios**: Calculates payout under different exit valuations.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used | Frontend Status |
| :--- | :--- | :--- | :--- |
| **Venture Dashboard** | Cap Table View | `cap_table_service` | **Missing** |
