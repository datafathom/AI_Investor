#!/bin/sh
# Start both Vite dev server and Node.js backend server

# Function to cleanup on exit
cleanup() {
    echo "Shutting down servers..."
    kill $BACKEND_PID 2>/dev/null
    exit 0
}

# Set up signal handlers
trap cleanup SIGTERM SIGINT

# Start backend server in background
echo "Starting backend server on port 3002..."
node server.js &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 3

# Check if backend started successfully
if ! kill -0 $BACKEND_PID 2>/dev/null; then
    echo "Error: Backend server failed to start"
    exit 1
fi

# Start Vite dev server in foreground
echo "Starting Vite dev server on port 5176..."
npm run dev

# If Vite exits, cleanup
cleanup

