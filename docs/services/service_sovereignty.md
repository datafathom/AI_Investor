# Backend Service: Sovereignty (The Private Channel)

## Overview
The **Sovereignty Service** provides secure, private communication infrastructure for the platform's users and agents. It's the foundation for a self-hosted, off-grid messaging capability.

## Core Components

### 1. Chat Server (`chat_server.py`)
- Minimal implementation for private, secure messaging.
- Designed for internal agent-to-agent or user-to-advisor communication.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used | Frontend Status |
| :--- | :--- | :--- | :--- |
| **Advisor Chat** | Message Window | `chat_server` | **Missing** |

## Notes
This is a minimal service, likely a placeholder for future expansion into Matrix/Signal-based secure communications.
