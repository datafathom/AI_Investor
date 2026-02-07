# LAN Distribution & Remote Docker

The Sovereign OS is designed to be distributed. You can host your data layer (Docker containers) on a powerful Linux server while running your development environment or trading frontend on a separate machine (e.g., a Windows laptop).

## Scenario: `dev-no-db` with a LAN Server

In this configuration, the "Server" runs the Docker containers, and the "Developer Machine" runs the logic and connects over the network.

### Step 1: Initialize the Server Machine
On the machine that will host the Docker containers (e.g., `192.168.1.50`):
1.  Clone the repository.
2.  Run the initialization command:
    ```bash
    python cli.py infra init-node 192.168.1.50 --roles storage
    ```
    *This sets `DOCKER_BIND_IP` to the LAN IP and generates SSL certificates tied to this host.*
3.  Start the containers:
    ```bash
    python cli.py docker up --profile storage
    ```

### Step 2: Configure the Developer Machine
On your laptop or workstation:
1.  Map the developer machine to the server's IP:
    ```powershell
    python cli.py infra set-lan-ip --ip 192.168.1.50
    ```
2.  Start the application in "Lightweight" mode:
    ```powershell
    python cli.py dev-no-db
    ```
    *This starts the Backend and Frontend only, skipping local Docker checks and connecting directly to the remote IP.*

## The `DOCKER_BIND_IP` Protocol

The `docker-compose.yml` uses the `${DOCKER_BIND_IP}` environment variable to determine which interface to listen on.

- **Local Mode**: `DOCKER_BIND_IP=127.0.0.1` (Default). Services are only accessible from the host itself.
- **LAN Mode**: `DOCKER_BIND_IP=192.168.1.50`. Services listen on the network interface, allowing authenticated remote connections.

## Security: SSL and Passwords

When distributed, all traffic between your machine and the Docker server is secured:
- **Encrypted Channels**: Traffic is routed through SSL/TLS using the certificates generated during `init-node`.
- **Authentication**: Redis, Postgres, and Neo4j require the passwords defined in your `.env` file. These passwords must match on both the Server and Developer machines.

## Switch Back to Local Mode

If you leave your LAN and want to work locally again:
```powershell
python cli.py infra set-lan-ip --ip 127.0.0.1
python cli.py docker up
python cli.py dev
```
