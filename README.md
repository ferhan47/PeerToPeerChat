# PeerToPeerChat
# Peer-to-Peer Chat Application

A decentralized chat system for LAN environments that enables peer discovery and encrypted messaging using UDP broadcasts and TCP sockets. Ideal for local networks where users want minimal setup.

---

## Components Overview
1. **`Peer_Discovery.py`**  
   - Listens for UDP broadcasts on port `6000`.
   - Maintains `users.json` with active peers' IPs, usernames, and last-seen timestamps.
   
2. **`Service_Announcer.py`**  
   - Broadcasts your username and IP to the network every 8 seconds.
   - Stores your username in `my_username.txt`.

3. **`Chat_Initiator.py`**  
   - Lets you start chats, view active users, and check history.
   - Supports **Diffie-Hellman key exchange** (shared prime `P=19`, base `G=2`) for encryption.

4. **`Chat_Responder.py`**  
   - Listens on TCP port `6001` for incoming messages.
   - Decrypts messages using a pre-shared key (private key hardcoded to `5`).

5. **`Chat_History.py`**  
   - Displays all logged messages from `chat_history.txt`.

---

## How to Run
### Prerequisites
- Python 3.x (no external libraries needed).
- All files must be in the same directory.
- Firewall must allow **UDP port 6000** (discovery) and **TCP port 6001** (chat).

### Installation
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-repo-url/p2p-chat.git
   cd p2p-chat
   
### Step-by-Step
2. **Start Peer Discovery** (in Terminal 1, Discovers and tracks active peers):  
   ```bash
   python Peer_Discovery.py
This populates/updates users.json.

### Step-by-Step
3. **Broadcast Your Presence** (in Terminal 2, Announce yourself to the network):
   ```bash
   python Service_Announcer.py
Enter a username if running for the first time.
Username is saved to my_username.txt.
   
### Step-by-Step
4. **Listen For Incoming Chats** (in Terminal 3, Always keep this running to receive messages):
   ```bash
   python Chat_Responder.py
   
### Step-by-Step
5. **Start Chatting** (in Terminal 4, Initiate chats or view history):
   ```bash
   python Chat_Initiator.py

Example Workflow 💬
Secure Chat
In **`Chat_Initiator`**, type **`chat`** and enter the target username.

Choose "yes" for secure mode.

Enter a private number (e.g., **`7`**) for Diffie-Hellman key exchange.

Send messages. Encrypted texts are marked with 🔐.

Unsecure Chat
Choose "**`no`**" for secure mode. Messages are plaintext (marked with 💬).

View History
Run python **`Chat_History.py`** or use the **`history`** command in **`Chat_Initiator`**.

Network Configuration ⚙️
Broadcast IP: If your subnet differs from **`192.168.1.*`**, edit **`BROADCAST_IP`** in **`Service_Announcer.py`** (e.g., **`192.168.0.255`**).

Known Limitations ⚠️
Security: Hardcoded Diffie-Hellman parameters (**`P=19, G=2`**) and fixed private key (**`5`** in Responder) make encryption weak.

User Status: "Online" status expires after 10 seconds; "Away" after 15 minutes.

Multi-Device Testing: On a single machine, manually edit **`users.json`** to simulate different users.

Notes
Change Username: **`Delete my_username.txt`** and rerun **`Service_Announcer.py`**.

Logs: All messages are saved in **`chat_history.txt`**
