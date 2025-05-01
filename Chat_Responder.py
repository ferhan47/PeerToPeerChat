import socket
import json
import sys
from datetime import datetime

PORT = 6001
LOG_FILE = "chat_history.txt"
P = 19
G = 2

def log_message(username, ip, message, sent=False):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    direction = "RECEIVED" if not sent else "SENT"
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {username} ({ip}) ({direction}): {message}\n")

def get_username_by_ip(ip):
    try:
        with open("users.json", "r") as f:
            users = json.load(f)
            for name, data in users.items():
                if data["ip"] == ip:
                    return name
    except:
        pass
    return ip

def decrypt_message(message, shared_key):
    return ''.join([chr((ord(c) - shared_key) % 256) for c in message])

def chat_responder():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("", PORT))
    sock.listen(5)
    print(f"[ChatResponder] Listening for incoming connections on port {PORT}...")

    while True:
        conn, addr = sock.accept()
        ip = addr[0]
        username = get_username_by_ip(ip)
        print(f"[ChatResponder] Chat started with {username} ({ip})")

        try:
            data = conn.recv(1024)
            if not data:
                continue
            message = json.loads(data.decode())

            if "key" in message:
                peer_public_key = int(message["key"])
                private_key = 5  # Can be randomized if needed
                public_key = (G ** private_key) % P
                response = json.dumps({"key": str(public_key)})
                conn.sendall(response.encode())
                shared_key = (peer_public_key ** private_key) % P

                data = conn.recv(1024)
                message = json.loads(data.decode())
                if "encrypted message" in message:
                    decrypted = decrypt_message(message["encrypted message"], shared_key)
                    print(f"🔐 {username}: {decrypted}")
                    log_message(username, ip, decrypted, sent=False)

            elif "encrypted message" in message:
                print(f"🔐 {username}: {message['encrypted message']}")
                log_message(username, ip, message['encrypted message'], sent=False)

            elif "unencrypted message" in message:
                print(f"💬 {username}: {message['unencrypted message']}")
                log_message(username, ip, message['unencrypted message'], sent=False)

        except Exception as e:
            print(f"[ChatResponder] Error: {e}")
        finally:
            conn.close()
            print(f"[ChatResponder] Chat ended with {username}")

if __name__ == "__main__":
    chat_responder()
