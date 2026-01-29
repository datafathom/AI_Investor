# AI Investor: Distributed Docker Cluster Guide

This guide explains how to set up, run, and switch between **Local Development** (1 box) and **Distributed LAN Box** (2+ boxes).

---

## 🚀 Scenario A: Single Machine (Local Dev Only)
*Use this when everything runs on your laptop.*

### 🛠️ Initialization (One-time)
From your project root (on your laptop):
```powershell
# 1. Start the cluster logic on your local machine
python cli.py infra init-node 127.0.0.1 --roles full
```
*This command creates your `.env`, sets IP to localhost, and generates certificates.*

### 🏃 Running
```powershell
# 2. Start the Docker containers locally
python cli.py docker up

# 3. Start the application
python cli.py dev
```

---

## 🌐 Scenario B: Two Machine Cluster (LAN Distribution)
*Use this to offload heavy DBs/Kafka to a "Storage Machine" (192.168.1.27).*

### 🕹️ Step 1: Initialize the STORAGE Machine (`192.168.1.27`)
*On the box that will host the containers:*
1. Clone the repo to this machine.
2. Run:
   ```bash
   python cli.py infra init-node 192.168.1.27 --roles storage
   ```
   *This sets up the bind IP and local SSL certs for this host.*

### 💻 Step 2: Initialize the DEVELOPER Machine (`Laptop`)
*On the machine where you write code:*
1. Run:
   ```powershell
   # Point your laptop to the Storage Machine's IP
   python cli.py infra set-lan-ip --ip 192.168.1.27
   ```

### 🏃 Step 3: Running the Cluster
1. **On the STORAGE Machine**:
   ```bash
   # 1. Install dependencies (Crucial!)
   # If this is ONLY a Storage Host:
   pip install -r requirements-linux-storage-host.txt
   
   # If this box is ALSO your Linux Dev Box (Dual Role):
   # pip install -r requirements-linux-dev.txt

   # 2. Start the containers with the storage profile via CLI
   python cli.py docker up --profile storage
   ```
2. **On the DEVELOPER Machine**:
   ```powershell
   # 1. Install dependencies
   pip install -r requirements-windows-dev.txt
   
   # 2. Start the app (it now auto-connects to 192.168.1.27)
   python cli.py dev
   ```

---

## 🏗️ Dependency Selection Guide

| Machine Role | OS | Installation Command |
| :--- | :--- | :--- |
| **Developer Laptop** | Windows | `pip install -r requirements.txt` |
| **Linux Dev Workstation** | Linux | `pip install -r requirements-linux-dev.txt` |
| **Full Host (Dev + Storage)** | Linux | `pip install -r requirements-linux-dev.txt` |
| **Production Storage Node** | Linux | `pip install -r requirements-linux-storage-host.txt` |
| **Windows Storage Node** | Windows | `pip install -r requirements-windows-storage-host.txt` |

---

## 🔄 Mode Switching: Help, I'm at a Coffee Shop!
*How to swap between LAN Mode and Local Mode.*

| Goal | Action | Command (on Laptop) |
| :--- | :--- | :--- |
| **Switch to LOCAL** | Set IP to Localhost | `python cli.py infra set-lan-ip --ip 127.0.0.1` |
| **Switch to LAN** | Set IP to Remote | `python cli.py infra set-lan-ip --ip 192.168.1.27` |

---

## ❓ FAQ & Command Roles

### Which box runs `cli.py docker up`?
- **In Scenario A (Local)**: Your laptop runs it.
- **In Scenario B (LAN)**: The **Storage Machine** runs it (or you run `docker compose` manually there). 
- *Note: Running `cli.py docker up` on your laptop in LAN mode will try to start a 2nd copy of the DBs on your laptop. Only do this if you want a local fallback.*

### What does `init-node` actually do?
1. Copies `.env.template` to `.env` (if missing).
2. Sets `DOCKER_BIND_IP` to the specified IP (safety first!).
3. Generates SSL Certificates tied to that specific IP.

### What is a "Role"?
- `storage`: Runs Postgres & Zookeeper.
- `graph`: Runs Neo4j.
- `streaming`: Runs Kafka.
- `full`: Runs everything (Default).

---
> [!IMPORTANT]
> **Security Reminder**: When in LAN Mode, `cli.py dev` on your laptop will send data over your home Wi-Fi. We have enabled SSL by default to keep this data encrypted.
