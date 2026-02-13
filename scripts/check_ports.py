
import socket
import sys

def check_port(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.settimeout(2)
            s.connect((host, port))
            print(f"✅ Success: {host}:{port} is open")
            return True
        except Exception as e:
            print(f"❌ Failed: {host}:{port} is closed ({e})")
            return False

if __name__ == "__main__":
    check_port("127.0.0.1", 5050)
    check_port("127.0.0.1", 5173)
