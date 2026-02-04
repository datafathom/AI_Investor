# React + Node + Socket.io Boilerplate

A standalone, ready-to-use boilerplate for building full-stack applications with React, Express, and Socket.io.

## Features
- **Frontend**: React with Vite.js
- **Backend**: Node.js with Express
- **Real-time**: Socket.io integration
- **Design System**: Centralized color palette configuration
- **Docker**: Pre-configured Dockerfile and Docker Compose

## Getting Started

### Local Development (Manual)

1. **Install Dependencies**:
   ```bash
   npm install
   ```

2. **Initialize Database** (if needed):
   ```bash
   npm run db:push
   ```

3. **Option A: Run Both Servers Together**:
   ```bash
   npm run dev:full
   ```
   *This starts both the backend (port 3002) and Vite dev server (port 5176) together.*

4. **Option B: Run Servers Separately**:
   
   **Terminal 1 - Backend Server**:
   ```bash
   npm start
   ```
   *Backend will be available at `http://localhost:3002`*
   
   **Terminal 2 - Frontend Dev Server**:
   ```bash
   npm run dev
   ```
   *Frontend will be available at `http://localhost:5176`*

### Docker Development

**Note:** You may need to use `sudo` if you're not in the docker group. See `DOCKER_TROUBLESHOOTING.md` for details.

1. **Start with Docker Compose**:
   ```bash
   sudo docker compose up -d --build
   ```
   *This will build the image and start the container with hot-reloading enabled via volumes.*
   
   - Backend API: `http://localhost:3002`
   - Frontend: `http://localhost:5176`
   
2. **View Logs**:
   ```bash
   sudo docker compose logs -f
   ```

3. **Check Container Status**:
   ```bash
   sudo docker compose ps
   ```

4. **Stop the Container**:
   ```bash
   sudo docker compose down
   ```

**Troubleshooting:** If you encounter permission errors, see `DOCKER_TROUBLESHOOTING.md` for solutions.

## Configuration

### Color Palette
Modify `config/color_palette.json` to update your application's colors. The changes will be automatically injected into the React application during development and build.

### Environment Variables
Create a `.env` file based on `.env.example`:
```bash
PORT=3002
NODE_ENV=development
```

## Structure
- `src/`: React source code
- `config/`: Color palette and other configuration
- `server.js`: Express + Socket.io server
- `vite.config.js`: Vite configuration with color injection
- `Dockerfile`: Production multi-stage build
- `docker-compose.yml`: Development orchestration
