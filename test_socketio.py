import socketio
print(f"SocketIO path: {socketio.__file__}")
try:
    sio = socketio.AsyncServer()
    print("Successfully created AsyncServer")
except AttributeError as e:
    print(f"Failed to create AsyncServer: {e}")
    print(f"SocketIO dir: {dir(socketio)}")
