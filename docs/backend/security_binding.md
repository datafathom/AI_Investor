# Security & Loopback Binding

The Sovereign OS follows a "Zero-Trust" security model. A critical component of this model is the strict isolation of backend services at the network level.

## Default Policy: Loopback Only

By default, every service in the backend (FastAPI, Redis, Postgres, etc.) is configured to bind ONLY to the loopback interface: **`127.0.0.1`** (or `localhost`).

- **Reasoning**: This ensures that even if a machine is connected to a public or unsecured local network, its trading engine and private keys are not exposed to other devices.
- **Enforcement**:
    - **FastAPI**: `uvicorn.run(app, host="127.0.0.1", port=5050)`
    - **Docker Control**: `cli.py docker up` ensures that network bridges do not expose ports to `0.0.0.0` unless explicitly overriden.

## LAN Distribution (High-Trust Nodes)

For distributed deployments (e.g., a dedicated "Database Box" and a "Trading Box"), the system supports secure LAN distribution.

- **Explicit Mapping**: The `scripts/runners/cert_runner:set_lan_ip` command allows the user to map a specific LAN IP (e.g., `192.168.1.50`) to the `.env` configuration.
- **Certificate-Based Security**: Once a LAN IP is set, the system generates unique SSL certificates for that IP. All traffic between nodes MUST be encrypted using these internal certs.
- **Zero-Trust Bridge**: Even when in LAN mode, the system uses "Security Gateways" between nodes to validate that only whitelisted MAC/IP addresses are communicating.

## Warning: `0.0.0.0` Prohibition

**NEVER** bind a server or listener to `0.0.0.0`. 
Binding to `0.0.0.0` opens the service to the entire network and is a CRITICAL security violation under the Sovereign OS protocol. All changes that even temporarily use `0.0.0.0` during development must be reverted before a git commit/deploy.
