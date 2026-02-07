# Backend Service: Workspace (The User Hub)

## Overview
The **Workspace Service** manages user preferences and personalization settings for the application.

## Core Components

### 1. User Preferences Service (`user_preferences_service.py`)
- **Theme Preferences**: Dark/light mode, color schemes.
- **Layout Settings**: Dashboard widget arrangement.
- **Notification Preferences**: Email, push, and in-app alert settings.
- **Default Account**: Sets default portfolio for trading actions.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used | Frontend Status |
| :--- | :--- | :--- | :--- |
| **Settings Page** | Preferences Panel | `user_preferences_service` | **Implemented** |
