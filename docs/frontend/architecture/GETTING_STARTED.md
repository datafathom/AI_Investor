# Getting Started Guide

## Quick Start

This guide will help you get the OS-Style Web GUI Boilerplate up and running in minutes.

### Prerequisites

- **Node.js** 20.x or higher
- **npm** 10.x or higher
- **Docker** (optional, for containerized deployment)
- **SQLite** (included via better-sqlite3)

### Installation

1. **Clone or download the project**
   ```bash
   cd GUI_boilerplate_react_node_socketio_widgets_os_style
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Initialize the database**
   ```bash
   npm run db:push
   ```
   This creates the SQLite database and all required tables.

4. **Start the development servers**

   **Option A: Run both servers together**
   ```bash
   npm run dev:full
   ```

   **Option B: Run servers separately**
   ```bash
   # Terminal 1 - Backend
   npm start

   # Terminal 2 - Frontend
   npm run dev
   ```

5. **Access the application**
   - Frontend: http://localhost:5176
   - Backend API: http://localhost:3002

### First Steps

1. **Register a new user**
   - Click "Register" in the top menu
   - Enter a username and password
   - Click "Register"

2. **Login**
   - Use your credentials to log in
   - You'll be redirected to the main dashboard

3. **Explore widgets**
   - Open the Widget Catalog from the menu
   - Browse available widgets
   - Add widgets to your layout

4. **Customize your theme**
   - Open the Theme Editor
   - Switch between Light and Dark themes
   - Customize colors and save your theme

5. **Manage windows**
   - Open the Window Manager widget
   - Create new windows
   - Try snap zones and window grouping

### Docker Setup (Optional)

```bash
# Build and start containers
sudo docker compose up -d --build

# View logs
sudo docker compose logs -f

# Stop containers
sudo docker compose down
```

### Environment Variables

Create a `.env` file in the root directory:

```env
NODE_ENV=development
PORT=3002
BACKEND_PORT=3002
VITE_PORT=5176
VITE_BACKEND_PORT=3002
JWT_SECRET=your-secret-key-here
```

### Troubleshooting

**Port already in use:**
- Change ports in `.env` or `vite.config.js` and `server.js`

**Database errors:**
- Delete `database.sqlite` and run `npm run db:push` again

**Module not found:**
- Run `npm install` again
- Clear `node_modules` and reinstall

**Socket.io connection errors:**
- Ensure backend server is running
- Check CORS settings in `server.js`

### Next Steps

- Read the [Architecture Guide](./ARCHITECTURE.md)
- Check the [Component Documentation](./COMPONENTS.md)
- Explore the [API Reference](./API.md)
- Learn about [Features](./FEATURES.md)

