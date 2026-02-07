# Utility: Authentication and Security

## Overview
These scripts handle specialized security tasks and authentication diagnostics.

## Key Utilities

### [diagnostic_auth.py](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/scripts/util/diagnostic_auth.py)
Performs a deep audit of the authentication flow, including token generation, validation, and cookie persistence. It helps identify why sessions might be prematurely expiring or failing validation.

### [generate_lan_certs.py](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/scripts/util/generate_lan_certs.py)
Generates self-signed SSL certificates for local LAN testing, allowing the frontend to communicate with the backend via HTTPS on a local network.

### [fix_admin.py](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/scripts/util/fix_admin.py)
A targeted repair script for the admin user's database record, ensuring the username, role, and permissions are correctly set in cases of database corruption or migration failures.

## Status
**Essential (Security)**: critical for maintaining the security posture of the development and testing environments.
