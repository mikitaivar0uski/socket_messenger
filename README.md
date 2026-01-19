# Socket Messenger

## Description
A simple **client–server messenger** written in Python.  
- Allows multiple clients to connect to a central server.  
- Clients are identified only by user-provided names.  
- Clients can send messages directly to other clients (no broadcast).  
- All messages, client info, and connection states exist **only during runtime**.  
- No login, database, or persistent storage yet.  
- Built with Python libraries: `socket`, `threading`, `dotenv`, `os`. 

---

## Usage
### First Method
1. Clone the repository:
```
git clone https://github.com/YehorSolonukha/socket_messenger
```
2. Run the server:
```
python ./server_side/src/server_main.py
```
3. Run clients in their respective windows:
```
python ./client_side/src/client_main.py
```
4. Enter a name to connect and start interacting with the server
---
### Second Method
1. Clone the repository:
```
git clone https://github.com/YehorSolonukha/socket_messenger
```
2. Run auto setup
```
./env_setup_windows2.ps1
```

---

## Future Enhancements:
- Database storage
- User login and authentication  
- Message timestamps
- Encryption
- Broadcast Messages
- Sending files and images
