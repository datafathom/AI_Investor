# Script: update_admin_password.py

## Overview
`update_admin_password.py` is a security utility for resetting or updating the password for the primary `admin` user account.

## Core Functionality
- **Password Reset**: directly updates the hashed password in the `users` table for the account with the username `admin`.
- **Security Compliance**: ensuring that the new password is correctly hashed using the system's standard password hashing algorithm (usually bcrypt or Argon2) to maintain compatibility with the login service.

## Usage
```bash
python scripts/database/update_admin_password.py --password NewSecret123!
```

## Status
**Essential (Administrative)**: critical for recovering access to the system if the administrative password is lost or compromised.
