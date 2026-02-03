# Phase 2: Network Security & Zero Trust (Implementation Plan)

**Goal**: Isolate services so they are unreachable from the external network, and even from each other unless explicitly allowed, across ALL environments (Dev, Prod, Frontend).

## 1. Docker Network Isolation (App-Wide)
**Context**: We found 3 Docker Compose files. ALL must be secured to prevent accidental exposure.

### 1.1 `infra/docker-compose.yml` (Dev Backend)
- **Change**: Define `internal` network.
    ```yaml
    networks:
      investor-network:
        driver: bridge
        internal: true  # <--- No external access for containers
    ```
- **Service Binding**: Ensure `fastapi` (if containerized) or ports mapped in `kafka`/`postgres` use `${DOCKER_BIND_IP:-127.0.0.1}` and NEVER `0.0.0.0`.

### 1.2 `infra/docker-compose.prod.yml` (Prod Backend)
- **Change**: Same as above, but stricter.
- **Verification**: Ensure no `ports:` section exposes 5432, 6379, 9092 to the host unless strictly necessary for a specific management tool (tunneling preferred).

### 1.3 `frontend2/docker-compose.boilerplate.yml`
- **Context**: This likely runs Nginx or a Node server.
- **Change**: Ensure it connects to the backend via the *internal* Docker network (if on same host) or a specific bound IP. It should NOT expose internal status ports (like Nginx stub_status) to the world.

## 2. Host Application Binding (FastAPI/Flask)
**Context**: The app runs on the host. `cli.py` controls startup.

### 2.1 Update `cli.py` & `web/fastapi_gateway.py`
- **Objective**: Prevent `0.0.0.0` binding by default.
- **Action**:
    - Modify `start_backend` handler in `scripts/runners/system_control.py`:
        - Default `host` = `127.0.0.1`.
        - Add `--host` flag to override only when explicitly needed.
    - Modify `web/fastapi_gateway.py`:
        - Ensure `uvicorn.run(..., host=...)` respects this flag.

## 3. Host Firewall (Propagated & Persistent)
**Context**: Scripts must be idempotent and persistent.

### 3.1 `scripts/infra/secure_host_linux.sh`
```bash
#!/bin/bash
# Reset
ufw --force reset
ufw default deny incoming
ufw default allow outgoing

# Management
ufw allow from 192.168.1.0/24 to any port 22 # SSH from LAN
ufw allow from 127.0.0.1 to any # Localhost loopback

# Application (Only if strictly needed from LAN)
# ufw allow from 192.168.1.0/24 to any port 5050

# Enable
ufw --force enable
```

### 3.2 `scripts/infra/Secure-Host-Windows.ps1`
```powershell
# Create a new Firewall Policy
New-NetFirewallRule -DisplayName "AI_Investor_Block_Inbound" -Direction Inbound -Action Block -Profile Any
New-NetFirewallRule -DisplayName "AI_Investor_Allow_Local" -Direction Inbound -RemoteAddress 127.0.0.1 -Action Allow
# Add rule for 5050 only from LAN subnet
New-NetFirewallRule -DisplayName "AI_Investor_Allow_API_LAN" -Direction Inbound -LocalPort 5050 -Protocol TCP -RemoteAddress 192.168.1.0/24 -Action Allow
```

## 4. Verification Plan
### 4.1 Nmap Sweep
- **Target**: Run against the host IP from a *different* machine on the LAN.
- **Command**: `nmap -p 1-65535 <HOST_IP>`
- **Pass Criteria**:
    - Port 5432 (PG): CLOSED/FILTERED
    - Port 6379 (Redis): CLOSED/FILTERED
    - Port 9092 (Kafka): CLOSED/FILTERED
    - Port 22 (SSH): OPEN (If configured)
    - Port 5050 (App): OPEN (Only if LAN access enabled)

## 5. Files to Create/Modify
- [MODIFY] [infra/docker-compose.yml](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/infra/docker-compose.yml)
- [MODIFY] [infra/docker-compose.prod.yml](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/infra/docker-compose.prod.yml)
- [MODIFY] [frontend2/docker-compose.boilerplate.yml](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/frontend2/docker-compose.boilerplate.yml)
- [MODIFY] [scripts/runners/system_control.py](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/scripts/runners/system_control.py)
- [NEW] [scripts/infra/secure_host_linux.sh](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/scripts/infra/secure_host_linux.sh)
- [NEW] [scripts/infra/Secure-Host-Windows.ps1](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/scripts/infra/Secure-Host-Windows.ps1)
