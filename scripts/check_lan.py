import socket
import sys

def check_lanbox(host, port):
    print(f"Checking connection to LANBOX {host}:{port}...")
    try:
        with socket.create_connection((host, port), timeout=2.0) as s:
            print("SUCCESS: Connection established.")
            return True
    except Exception as e:
        print(f"FAILED: {e}")
        return False

if __name__ == "__main__":
    check_lanbox("192.168.1.67", 7687)
    check_lanbox("127.0.0.1", 5050)
