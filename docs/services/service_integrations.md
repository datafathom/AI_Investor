# Backend Service: Integrations (Vertical Plugins)

## Overview
The **Integrations (Vertical Plugins) Service** manages niche and vertical-specific third-party API bridges. Unlike the core integration framework which handles broad financial data, this service focuses on high-specificity plugins such as **Real Estate Valuation (Zillow)** and the **Voice Command OS (Whisper)**. It serves as an internal "Marketplace Manager" where administrators can register, enable, and monitor specialized third-party dependencies.

## Core Components

### 1. Real Estate Valuation Bridge (`zillow.py`)
Provides mark-to-market capabilities for physical property assets.
- **Zestimate Integration**: Fetches real-time property valuations and one-month price shifts directly from Zillow. This allows physical real estate to be tracked alongside liquid equities in the platform's unified wealth dashboard.

### 2. Voice Command OS (`voice_cmd.py`)
Enables the platform's human-interface Layer via audio.
- **Speech-to-Intent Orchestration**: Interfaces with AI transcription services (e.g., Whisper) to convert verbal instructions into structured system commands. This allows principals to interact with their portfolio via natural language (e.g., "Show me my exposure to NVDA").

### 3. Integration Manager (`manager.py`)
The administrative registry for specialized plugins.
- **API Marketplace**: Manages the registration of third-party API keys, ensuring they are masked in logs for security.
- **Service Toggle**: Provides a centralized toggle system to enable or disable niche integrations without requiring a system restart.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used |
| :--- | :--- | :--- |
| **Real Estate Detail**| Property Mark-to-Market Card | `zillow_service.get_zestimate()` |
| **Global UI** | Voice Command Pulse | `voice_os.process_audio()` |
| **Marketplace Station**| API Bridge Status List | `integration_manager.get_active_integrations()` |
| **Admin Station** | API Key Registrar | `integration_manager.register_integration()` |

## Dependencies
- `Zillow API`: (External) Source for real estate valuation telemetry.
- `Whisper API`: (External) Source for speech transcription and intent processing.
- `logging`: Records API fetch events and transcription successes/failures.

## Usage Examples

### Tracking Property Value via Zestimate
```python
from services.integrations.zillow import ZillowService

z_svc = ZillowService()

# Fetch latest valuation for a specific property ID
valuation = z_svc.get_zestimate(property_id="PROP_BEL_AIR_01")

print(f"Current Value: ${valuation['current_valuation']:,.2f}")
print(f"Monthly Change: ${valuation['one_month_change']:+, .2f}")
```

### Processing a Voice Instruction
```python
from services.integrations.voice_cmd import VoiceOS

voice = VoiceOS()

# Simulate receiving audio from the user's mobile device
# "Show my exposure to Apple"
intent = voice.process_audio(audio_data=b"binary_audio_payload")

print(f"Detected System Intent: {intent}")
# Logic would then route "SHOW_EXPOSURE_AAPL" to the Exposure Service
```

### Registering a New Marketplace Integration
```python
from services.integrations.manager import IntegrationManager

manager = IntegrationManager()

# Register a specialized data bridge
manager.register_integration(
    name="REUTERS_MACRO",
    api_key="SK_ABC_123_SECRET_KEY",
    enabled=True
)

print(f"Active Integrations: {manager.get_active_integrations()}")
```
