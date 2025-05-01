import socket
import json
import sys
import threading
import time
from datetime import datetime

PORT = 6001
USERS_FILE = "users.json"
LOG_FILE = "chat_history.txt"

P = 19
G = 2


def log_message(username, ip, message, sent=True):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    direction = "SENT" if sent else "RECEIVED"
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {username} ({ip}) ({direction}): {message}\n")


def load_users():
    try:
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print("users.json not found. Run peer_discovery.py first.")
        return {}


def get_active_users():
    try:
        with open(USERS_FILE, "r") as f:
            users = json.load(f)
        active_users = []
        current_time = time.time()
        for username, data in users.items():
            last_seen = data.get("timestamp", 0)
            status = "Online" if current_time - last_seen <= 10 else "Away"
            if current_time - last_seen <= 900:
                active_users.append((username, status))
        return active_users
    except FileNotFoundError:
        return []


def view_users():
    users = get_active_users()
    print("\n--- Active Users ---")
    for name, status in users:
        print(f"{name} ({status})")


def view_chat_history():
    try:
        with open(LOG_FILE, "r") as f:
            print("\n--- Chat History ---\n")
            print(f.read())
    except FileNotFoundError:
        print("No chat history found.")


def encrypt_message(message, shared_key):
    return ''.join([chr((ord(c) + shared_key) % 256) for c in message])


def chat():
    users = load_users()
    target_username = input("Enter username to chat with: ").strip()
    target = users.get(target_username)

    if not target:
        print("User not found.")
        return

    ip_address = target["ip"]
    secure_chat = input("Secure chat? (yes/no): ").lower().strip() == "yes"

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock.connect((ip_address, PORT))
        print(f"Connected to {target_username} at {ip_address}")

        if secure_chat:
            private_key = int(input("Enter a private number for key exchange: "))
            public_key = (G ** private_key) % P
            key_message = json.dumps({"key": str(public_key)})
            sock.sendall(key_message.encode())

            response = sock.recv(1024)
            response_data = json.loads(response.decode())
            peer_public_key = int(response_data["key"])
            shared_key = (peer_public_key ** private_key) % P
        else:
            shared_key = None

        msg = input("Enter message: ")

        if secure_chat:
            encrypted = encrypt_message(msg, shared_key)
            message = json.dumps({"encrypted message": encrypted})
        else:
            message = json.dumps({"unencrypted message": msg})

        sock.sendall(message.encode())
        log_message(target_username, ip_address, msg, sent=True)

    except Exception as e:
        print(f"Error: {e}")
    finally:
        sock.close()
        print("Chat ended.")


def start_chat():
    while True:
        choice = input("\nChoose an option: Users / Chat / History / Exit: ").strip().lower()
        if choice == "users":
            view_users()
        elif choice == "chat":
            chat()
        elif choice == "history":
            view_chat_history()
        elif choice == "exit":
            break
        else:
            print("Invalid option. Try again.")


if __name__ == "__main__":
    start_chat()
