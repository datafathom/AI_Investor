# Sentry Department Agents (`sentry/sentry_agents.py`)

The Sentry department manages physical and digital security, geofencing, and biometric synchronization.

## Travel-Mode Guard Agent (Agent 11.3)
### Description
The `TravelGuardAgent` monitors for device divergence (e.g., your primary workstation vs. your mobile device) and triggers lockouts if security violations are detected.

### Capabilities
- **Geofencing**: Tracks device coordinates (lat/lon) via the `GeofenceService`.
- **Divergence Detection**: Calculates distance between trusted devices.
- **Enforcement**: Triggers a `LOCK_SYSTEM` action if devices diverge beyond a safe proximity threshold.

### Integration
- **Heartbeat Checks**: Validates device proximity in real-time during "Travel Mode."
- **Security Alerts**: Emits high-priority error traces on mismatch detection.
