# Database Design

## Notes
- only a certain number of messages (per client) / logs can be stored

---

## Entities

### Clients
Stores client information.
- `user_id` (primary key)  
- `username` (unique)  
- `status` 
(for future login feature) 
- `password_hash`   

### Messages
Stores messages exchanged between clients.
- `message_id` (primary key)  
- `sender_id` (foreign key → Clients)  
- `receiver_id` (foreign key → Clients)  
- `content` (text)  
- `timestamp` (message sent time)  

### Connections
Stores client connection states.
- `connection_id` (primary key)  
- `user_id` (foreign key → Clients)  
- `connected_at` (timestamp)  
- `disconnected_at` (timestamp, optional)  
- `state` (current client state, e.g., active/inactive)  

### Server Logs
Stores server events for debugging and monitoring.
- `log_id` (primary key)  
- `event_type` (connection, message, error)  
- `details` (text)  
- `timestamp`

