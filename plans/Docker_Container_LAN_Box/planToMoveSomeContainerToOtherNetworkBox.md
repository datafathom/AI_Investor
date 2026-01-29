# Distributed Docker Strategy: LAN Box Offloading

## Objective
To reduce local memory utilization (currently 85-95%) by moving secondary infrastructure containers (Neo4j, Kafka, Zookeeper, Postgres) to a dedicated machine on the same Local Area Network (LAN). The setup must support both "100% Local" and "Distributed" modes seamlessly.

## 1. Candidate Containers for Offloading
Based on memory limits in `infra/docker-compose.yml`:
| Service | Memory Limit | Priority | Reason |
| :--- | :--- | :--- | :--- |
| **Neo4j** | 512MB | High | Highest single consumer. |
| **Kafka** | 400MB | High | Heavy JVM process. |
| **Zookeeper**| 300MB | High | Required by Kafka. |
| **Postgres** | 200MB | Medium | Standard DB offloading. |
| **Redis** | 100MB | Low | Small footprint, can stay local. |

**Total Potential Savings**: ~1.4GB RAM on the development laptop.

## 2. Technical Approach: Environmental Multi-Tenancy

### A. IP Binding Abstraction
Modify the `docker-compose.yml` to use a variable for port binding.
- **Local Mode**: Binds to `127.0.0.1` (Default Security).
- **LAN Mode**: Binds to `0.0.0.0` (Exposed to LAN).

### B. Connection String Orchestration
The `.env` file will toggle between `localhost` and the `LAN_BOX_IP`.

## 3. Configuration Steps

### Step 1: Remote Machine Setup (The "LAN Box")
1. Install Docker and Docker Compose.
2. Clone only the `infra/` directory and `data/` placeholders.
3. In the `.env` file on the **LAN Box**, set:
   ```bash
   DOCKER_BIND_IP=0.0.0.0
   ```
4. Run the containers:
   ```bash
   docker-compose -f infra/docker-compose.yml up -d
   ```

### Step 2: Local Machine Setup (The Laptop)
1. In your `.env` file, add the LAN Box IP:
   ```bash
   LAN_BOX_IP=192.168.1.XX  # Replace with actual IP
   ```
2. Update connection strings to use the variable:
   ```bash
   DATABASE_URL=postgresql://user:pass@${LAN_BOX_IP:-localhost}:5432/db
   NEO4J_URI=bolt://${LAN_BOX_IP:-localhost}:7687
   KAFKA_BOOTSTRAP_SERVERS=${LAN_BOX_IP:-localhost}:9092
   ```
3. Stop local instances of the offloaded containers.

## 4. Usage Modes

### Mode A: 100% Local (Developer Solo)
- Keep `LAN_BOX_IP` commented out or empty in `.env`.
- All services run on the laptop.

### Mode B: Distributed (LAN Optimization)
- Set `LAN_BOX_IP` to the remote machine's address.
- Comment out the services in `infra/docker-compose.yml` locally OR use Docker Profiles to disable them.

> [!TIP]
> Use **Docker Profiles** to easily toggle services.
> `docker-compose --profile local-only up` vs `docker-compose --profile distributed up`.

## 5. Verification Plan
1. **Ping Test**: Ensure Laptop can reach LAN Box IP.
2. **Port Check**: Use `Test-NetConnection -ComputerName [IP] -Port 5432` to verify DB visibility.
3. **Application Logs**: Verify the backend connects to the remote Kafka/Neo4j without timeouts.
