import socket
import json
import time
import os
USERNAME_FILE = "my_username.txt"
BROADCAST_IP = "192.168.1.255"
PORT = 6000

# Ask for and store username
if os.path.exists(USERNAME_FILE):
    with open(USERNAME_FILE, "r") as f:
        USERNAME = f.read().strip()
else:
    USERNAME = input("Enter your username: ").strip()
    with open(USERNAME_FILE, "w") as f:
        f.write(USERNAME)

hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)

def broadcast_presence():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    message = json.dumps({"username": USERNAME, "ip": local_ip})

    while True:
        sock.sendto(message.encode(), (BROADCAST_IP, PORT))
        print(f"[Announcer] Broadcasting: {message}")
        time.sleep(8)

if __name__ == "__main__":
    broadcast_presence()
