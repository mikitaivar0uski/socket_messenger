from pathlib import Path

class StorageManager:
    def __init__(self):
        file_path = Path("storage.txt")
        file_path.touch()

    def create_client(self, username: str, password: str) -> bool:
        with open("storage.txt", "a") as f:
            f.write(f"{username} {password}\n")
            return True
        return False

    def client_exists(self, target_username: str) -> bool:
        with open("storage.txt", "r") as f:
            for line in f:
                parts = line.strip().split()
                if not parts:
                    continue
                username = parts[0]
                if username == target_username:
                    return True
        return False


    def verify_password(self, target_username: str, target_password: str) -> bool:
        with open("storage.txt", "r") as f:
            for line in f:
                parts = line.strip().split()
                if not parts:
                    continue
                username, password = parts
                if username == target_username and password == target_password:
                    return True
        return False
