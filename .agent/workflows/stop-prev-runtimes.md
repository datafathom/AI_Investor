---
description: Stop all previous backend and frontend runtimes and Docker containers
---
1. Stop Docker Infrastructure

   ```powershell
   python cli.py docker down
   ```

2. Kill Python Processes (Backend)

   ```powershell
   taskkill /F /IM python.exe /T
   ```

   *Note: This might error if no python processes are running, which is fine.*

3. Kill Node Processes (Frontend)

   ```powershell
   taskkill /F /IM node.exe /T
   ```

   *Note: This might error if no node processes are running, which is fine.*
