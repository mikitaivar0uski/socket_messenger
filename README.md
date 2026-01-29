# Socket Messenger

## Description
A simple **client–server messenger** written in Python.  

Features:  
- Multiple clients can connect to a central server.  
- Clients are identified by user-provided names.  
- Clients can send messages directly to other clients (no broadcast).  
- All messages, client info, and connection states exist **only during runtime**.  
- No login, database, or persistent storage yet.  
- Built with Python libraries: `socket`, `threading`, `dotenv`, `os`.  

---

## Requirements

### Local setup
- Python 3.10+  
- `py -m pip install -r requirements.txt`

### Docker setup
- [Docker Desktop](https://docs.docker.com/desktop/setup/install/windows-install/)
- [WSL 2](https://docs.docker.com/desktop/setup/install/windows-install/#wsl-verification-and-setup)

The project includes `Dockerfile`s for both **server** and **client**, and a `docker-compose.yml` to simplify running multiple clients and the server.

---

## Usage

### Method 1 — Local Python
1. Clone the repository:
```
git clone https://github.com/YehorSolonukha/socket_messenger
cd socket_messenger
```
2. Run the server:
```
python ./server_side/src/server_main.py
```
3. Run clients in separate terminals:
```
python ./client_side/src/client_main.py
```
4. Enter a username for each client to connect and start messaging


### Method 2 — Docker auto (recommended)
1. Clone the repository:
```
git clone https://github.com/YehorSolonukha/socket_messenger
cd socket_messenger
```
2. Run Docker Desktop
3. (after Docker Desktop is loaded) Run the script for auto-setup:
```
.\windows_docker_setup.ps1
```
4. Enter a username for each client to connect and start messaging