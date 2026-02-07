# Backend Service: Reputation (The Guardian)

## Overview
The **Reputation Service** protects the digital identity of Ultra High Net Worth (UHNW) families. It detects deepfakes, monitors online sentiment, and automates legal takedown requests.

## Core Components

### 1. Deepfake Detector (`deepfake_detect.py`)
- **Media Scanning**: Analyzes videos/audio for manipulation artifacts (e.g., lip sync mismatches).
- **DMCA Automation**: Issues takedown notices for unauthorized AI clones of protected identities.

### 2. Supporting Modules
- `sentiment_radar.py`: Monitors online mentions of family members.
- `seo_shield.py`: Suppresses negative search results.
- `ghost_writer.py`: AI-generated reputation repair content.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used | Frontend Status |
| :--- | :--- | :--- | :--- |
| **Security Dashboard** | Deepfake Alerts | `deepfake_detect.scan_media()` | **Missing** |

## Usage Example

```python
from services.reputation.deepfake_detect import DeepfakeDetectorService

detector = DeepfakeDetectorService()

result = detector.scan_media("https://suspicious-site.com/fake_interview.mp4")
if result["is_deepfake"]:
    detector.issue_takedown(result["url"])
```
