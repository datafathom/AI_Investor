# Deployment Guide: Local vs. Distributed

This guide explains how to configure AI Investor for a single machine or a 2-node LAN cluster.

## 1. Single Machine (Localhost)
*Best for development and testing on a single device.*

1. **Initialize Environment**:
   ```powershell
   # Configures .env to use 127.0.0.1 for all services
   python cli.py infra init-node 127.0.0.1
   ```

2. **Start Docker Stack**:
   ```powershell
   # Starts Database, Redis, Kafka, Graph (Full Stack)
   python cli.py docker up --profile full
   ```

3. **Start Application**:
   ```powershell
   # Terminal 1: Application Backend
   python cli.py start-backend

   # Terminal 2: Frontend
   python cli.py start-frontend
   ```

---

## 2. Distributed (2-Node LAN Cluster)
*Scenario: "This machine" runs only Backend/Frontend. "Other machine" runs all Docker containers.*

### Machine A: The "Other" Machine (Infrastructure)
*The powerful machine running Docker. Example IP: `192.168.1.50`*

1. **Open Ports**:
   ```powershell
   # Configures Docker to listen on its LAN IP (not just localhost)
   # REPLACE 192.168.1.50 with Machine A's actual LAN IP!
   python cli.py infra init-node 192.168.1.50
   ```

2. **Start Docker**:
   ```powershell
   python cli.py docker up --profile full
   ```

### Machine B: THIS Machine (Application)
*Your laptop/dev machine running only code.*

1. **Point to Machine A**:
   ```powershell
   # Tells this machine where to find the database
   # Use Machine A's IP here!
   python cli.py infra set-lan-ip 192.168.1.50
   ```

2. **Start App**:
   ```powershell
   # No 'docker up' needed here!
   python cli.py start-backend
   python cli.py start-frontend
   ```
