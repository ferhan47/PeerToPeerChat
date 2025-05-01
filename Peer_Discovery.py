import socket
import json
import time
import sys

PORT = 6000
USERS_FILE = "users.json"

def listen_for_peers():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("", PORT))
    print(f"[PeerDiscovery] Listening on UDP port {PORT}...")

    users = {}  # IP -> {"username": str, "last_seen_time": float}

    while True:
        data, addr = sock.recvfrom(1024)
        try:
            message = json.loads(data.decode())
            username = message.get("username")
            ip = message.get("ip") or addr[0]

            if username:
                current_time = time.time()
                if ip in users:
                    users[ip]["last_seen_time"] = current_time
                else:
                    users[ip] = {"username": username, "last_seen_time": current_time}
                    print(f"[PeerDiscovery] {username} is online at {ip}")

                # Save dictionary to file in format: username -> {ip, last_seen_readable}
                username_to_ip = {}
                for ip_addr, entry in users.items():
                    readable_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(entry["last_seen_time"]))
                    username_to_ip[entry["username"]] = {"ip": ip_addr, "last_seen": readable_time, "timestamp": entry["last_seen_time"]}

                with open(USERS_FILE, "w") as f:
                    json.dump(username_to_ip, f, indent=4)

        except json.JSONDecodeError:
            print("[PeerDiscovery] Malformed JSON")

if __name__ == "__main__":
    listen_for_peers()
