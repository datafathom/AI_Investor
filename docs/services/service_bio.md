# Backend Service: Bio

## Overview
The **Bio Service** is a unique component of the Sovereign OS that treats the user's biological health as an essential asset. It integrates health telemetry, genomic data, and longevity protocols to maximize the user's "Human Alpha"—ensuring the biological operator of the system remains high-performing and resilient over the long term.

## Core Health Pillars

### 1. Biological Age & Epigenetics (`biological_age.py`)
Computes the difference between chronological and biological age.
- **PhenoAge Calculation**: Uses blood biomarkers (Glucose, CRP, Albumin, etc.) to estimate biological aging rates.
- **Rejuvenation Protocols**: Automatically suggests lifestyle or physiological adjustments (e.g., Zone 2 cardio, sleep optimization) if the biological age is accelerating beyond the chronological baseline.

### 2. Genomic Vault & Pharmacogenomics (`genomic_vault.py`)
Provides a secure environment for managing sensitive DNA-based risk profiles.
- **Drug Sensitivity Checks**: Compares drug names against a pharmacogenomic map (e.g., CYP2D6 gene) to identify potential toxicities or ineffective treatments.
- **Longevity Profiling**: Identifies genetic strengths (FOXO3) and risks (APOE4) to inform long-term preventative health strategies.

### 3. Longevity Stack Management (`supplement_mgr.py`)
Manages the inventory and compliance of the user's daily longevity supplements.
- **Inventory Tracking**: Monitors "on-hand" counts for items like NMN, Resveratrol, and Magnesium.
- **Auto-Reorder**: Generates order lists when stocks fall below defined thresholds, integrating with preferred high-quality vendors.

### 4. Health Telemetry Ingestion (`wearable_ingest.py`)
The data hub for real-time biological monitoring.
- **Provider Support**: Designed to ingest data from Oura, Apple Health, and Whoop.
- **Biometric Sync**: Captures daily scores for **Readiness**, **Sleep**, **HRV**, and **Resting Heart Rate** to inform the system's assessment of the user's current cognitive and physical capacity.

## Dependencies
- `pyotp`: Used to secure access to the Genomic Vault.
- `decimal`: Ensures precision in biomarker and dosage calculations.
- `logging`: Used for bio-feedback alerts and low-stock warnings.

## Usage Examples

### Assessing Pharmacogenomic Risk
```python
from services.bio.genomic_vault import GenomicVaultService

vault = GenomicVaultService()
check = vault.check_drug_sensitivity("Codeine")

if check['status'] == "WARNING":
    print(f"ALERT: Genetic risk detected on gene {check['gene']}. {check['implication']}")
```

### Checking Supplement Inventory
```python
from services.bio.supplement_mgr import SupplementManager

mgr = SupplementManager()
low_stock = mgr.check_inventory()

if low_stock:
    print(f"Items to reorder: {', '.join(low_stock)}")
    order = mgr.generate_order_list()
    print(f"Order status: {order['status']} via {order['vendor']}")
```
