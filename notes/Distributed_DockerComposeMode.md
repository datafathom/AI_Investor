# Developer Guide: Distributed Docker Mode

## Overview
This setup allows you to run heavy infrastructure components (Postgres, Kafka, Neo4j) on a separate machine on your LAN, reducing memory pressure on your primary development laptop.

## Prerequisites
- A secondary machine (the "LAN Box") with Docker and Docker Compose installed.
- Both machines must be on the same Local Area Network (LAN).
- You need the LAN IP address of the "LAN Box".

---

## 1. Remote Machine Setup (LAN Box)

1.  **Clone Infrastructure**: Copy the `infra/` directory and `.env.template` to the remote machine.
2.  **Configure Environment**: Create a `.env` file in the `infra/` directory on the remote machine:
    ```bash
    # Expose ports to the LAN instead of just localhost
    DOCKER_BIND_IP=0.0.0.0
    ```
3.  **Start Services**:
    ```bash
    docker-compose -f docker-compose.yml up -d
    ```

---

## 2. Local Machine Setup (Laptop)

1.  **Configure Environment**: Update your local `.env` file:
    ```bash
    # The IP of your remote machine
    LAN_BOX_IP=192.168.1.XX  # Replace with actual IP
    
    # Keep DOCKER_BIND_IP as 127.0.0.1 locally for security
    DOCKER_BIND_IP=127.0.0.1
    ```
2.  **Toggle Connections**: The application will automatically use the `LAN_BOX_IP` for connection strings due to the dynamic interpolation in `.env.template`:
    ```bash
    DATABASE_URL=postgresql://user:pass@${LAN_BOX_IP:-localhost}:5432/db
    ```
3.  **Stop Local Containers**: Stop any infrastructure containers running locally to free up memory.
4.  **Launch Backend**: Run your development server as usual:
    ```bash
    python cli.py dev
    ```

---

## 3. Switching Back (Local-Only Mode)

To return to 100% local development:
1.  **Comment out** `LAN_BOX_IP` in your `.env`.
2.  **Start** your local Docker containers via `docker-compose up -d`.

## Troubleshooting

-   **Ping Check**: Run `ping [LAN_BOX_IP]` from your laptop to ensure network connectivity.
-   **Port Accessibility**: Verify the remote ports are open:
    -   Postgres: 5432
    -   Kafka: 9092
    -   Neo4j (Bolt): 7687
-   **Firewall**: Ensure the firewall on the LAN Box allows incoming connections on the required ports.

---
> [!NOTE]
> This configuration leverages the interpolated variables added to `infra/docker-compose.yml` and `.env.template`. Ensure these files have the latest changes containing `${DOCKER_BIND_IP:-127.0.0.1}` and `${LAN_BOX_IP:-localhost}`.
