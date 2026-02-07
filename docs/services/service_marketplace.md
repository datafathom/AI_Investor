# Backend Service: Marketplace

## Overview
The **Marketplace Service** is the platform's ecosystem and extensibility infrastructure. It provides a standardized **Extension Framework** that allows third-party developers and institutions to build, validate, and deploy plugins and strategies within the Sovereign OS environment. The service manages the entire lifecycle of an extension—from sandboxed development and security validation to public listing, user reviews, and secure installation.

## Core Components

### 1. Extension Framework (`extension_framework.py`)
The foundational layer for third-party contributions.
- **Sandboxed Development**: Enables developers to create and test extensions in a secure, isolated environment before submission.
- **Security Validation Pipeline**: Performs automated security and code-quality checks on submitted extensions to ensure they comply with the platform's Zero-Trust architecture.
- **Extension Registry**: Manages versioning and metadata for all available plugins, ensuring that users always have access to stable and authenticated code.

### 2. Marketplace Orchestration (`marketplace_service.py`)
The consumer-facing layer for strategy and tool discovery.
- **Discovery & Listing**: Provides a searchable catalog of extensions categorized by functionality (e.g., Risk, Trading, Reporting).
- **Reputation & Feedback**: Manages a granular review and rating system, allowing the community to vet the effectiveness of various third-party strategies.
- **Installation Management**: Orchestrates the secure deployment of extensions into a user's local instance, maintaining a ledger of active installations and subscription states.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used |
| :--- | :--- | :--- |
| **Marketplace Station**| Extension Grid / Catalog | `marketplace_service.get_extension_reviews()` |
| **Marketplace Station**| Review & Rating Form | `marketplace_service.add_review()` |
| **Marketplace Station**| Extension Detail View | `extension_framework.cache_service` |
| **Developer Console** | Extension Creation Wizard | `extension_framework.create_extension()` |
| **Developer Console** | Security Audit Results | `extension_framework.validate_extension()` |
| **System Settings** | Installed Plugins Ledger | `marketplace_service.install_extension()` |

## Dependencies
- `services.system.cache_service`: Persists extension metadata, reviews, and installation records.
- `schemas.marketplace`: Defines the standard `Extension`, `ExtensionStatus`, and `ExtensionReview` models.
- `SecurityService`: (External) Performs deep-packet inspection of extension code during validation.

## Usage Examples

### Creating a New Developer Extension
```python
from services.marketplace.extension_framework import get_extension_framework

framework = get_extension_framework()

# Developer submits a new Momentum Alpha strategy
extension = await framework.create_extension(
    developer_id="dev_black_swann_001",
    extension_name="Hyper-Momentum-V2",
    description="Captures volatility breakout signals in G10 FX pairs.",
    version="1.0.0",
    category="Trading Strategy"
)

print(f"Extension Registered: {extension.extension_id} (Status: {extension.status})")
```

### Validating an Extension for Production
```python
from services.marketplace.extension_framework import get_extension_framework

framework = get_extension_framework()

# (Simulated) Run the validation pipeline
# extension comes from the framework
report = await framework.validate_extension(extension=extension)

if report['valid']:
    print(f"Security Audit PASSED. Timestamp: {report['timestamp']}")
else:
    print(f"Audit FAILED: {report['security']['errors']}")
```

### Installing a Strategy for a Client
```python
from services.marketplace.marketplace_service import get_marketplace_service

marketplace = get_marketplace_service()

# Client installs the strategy to their instance
install = await marketplace.install_extension(
    extension_id="ext_dev_001_123456789",
    user_id="user_vanderbilt_001"
)

print(f"Installation Success: {install['installation_id']}")
print(f"Status: {install['status']} | Active since: {install['installed_date']}")
```
