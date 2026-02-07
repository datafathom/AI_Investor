# Backend Service: Physical (Security Grid)

## Overview
The **Physical Security Service** connects the digital brain of the Sovereign OS to the physical world. It manages the hardware layer of defense, including biometric access control systems, CCTV surveillance with computer vision, and autonomous drone patrols. It ensures that the servers running the AI and the assets stored in the vault are physically protected.

## Core Components

### 1. Access Control (`access_control.py`)
The Gatekeeper.
- **Biometric Logging**: Tracks all entries and exits from secure zones (Server Room, Vault) using methods like Retina Scan, Fingerprint, and NFC.
- **Audit Trail**: Immutable logs of who went where and when, critical for post-incident forensics.

### 2. CCTV Engine (`cctv_engine.py`)
The Eyes.
- **AI Analytics**: Runs object detection (YOLOv8) on video streams to identify unauthorized persons or vehicles in restricted areas.
- **Retention Policy**: Manages storage rotation for video evidence (default 30 days).

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used | Frontend Status |
| :--- | :--- | :--- | :--- |
| **Mission Control** | Defcon Status | `defcon_svc.get_current_level()` | **Implemented** (`MissionControl.jsx`) |
| **Security Dashboard** | Camera Feed | `cctv_engine.analyze_frame()` | **Missing** (Backend logic exists, UI pending) |

## Dependencies
- `random`: Used for simulating sensor noise and detection events in the current mock implementation.

## Usage Examples

### Logging a Retina Scan Entry
```python
from services.physical.access_control import AccessControlService

security = AccessControlService()

# User scans retina at Server Room door
log = security.log_access_attempt(
    user_id="admin_01",
    zone="Server Room",
    method="RETINA_SCAN",
    success=True
)

print(f"Access Status: {log['status']}")
```

### Analyzing a CCTV Frame
```python
from services.physical.cctv_engine import CCTVEngine

cctv = CCTVEngine()

# Process frame from the Gate Camera
result = cctv.analyze_frame("Cam-01-Gate")

if result['detections']:
    print(f"ALERT: {len(result['detections'])} objects detected!")
    for det in result['detections']:
        print(f"- Detected {det['label']} (Confidence: {det['confidence']:.2f})")
```
