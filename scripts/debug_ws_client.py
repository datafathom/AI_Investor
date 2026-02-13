import socketio
import time
import sys

# Standard Python Socket.IO client
sio = socketio.Client()

@sio.event
def connect():
    print("✅ [Client] Connected to Backend successfully!")

@sio.event
def connect_error(data):
    print(f"❌ [Client] Connection failed: {data}")

@sio.event
def disconnect():
    print("⚠️ [Client] Disconnected")

@sio.on('event')
def on_message(data):
    print(f"📩 [Client] Received event: {data.get('topic')} at {data.get('timestamp')}")

def main():
    # Target the backend directly (bypass frontend proxy)
    # Backend runs on 5050
    # Mount point is /ws/admin/event-bus
    # So socket.io path is /ws/admin/event-bus/socket.io
    
    url = 'http://127.0.0.1:5050'
    socket_path = '/ws/admin/event-bus/socket.io'
    
    print(f"🚀 Attempting connection to: {url}")
    print(f"   Path: {socket_path}")
    
    try:
        sio.connect(
            url, 
            socketio_path=socket_path,
            transports=['websocket', 'polling'],
            wait_timeout=5
        )
        print("⏳ Waiting for events...")
        sio.wait()
    except Exception as e:
        print(f"❌ Exception during connect: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
