import os
from pathlib import Path

from dotenv import load_dotenv
from supabase import Client, create_client


class StorageManager:
    def __init__(self):
        load_dotenv(Path(__file__).resolve().parents[3] / ".env", override=False)

        url: str = os.environ.get("SUPABASE_URL")
        key: str = os.environ.get("SUPABASE_KEY")

        if not url or not key:
            raise ValueError("SUPABASE_URL or SUPABASE_KEY not found in .env file")

        self.db: Client = create_client(url, key)

    # AUTHENTICATION

    def create_client(self, username: str, password: str) -> bool:
        try:
            # Insert new user into clients table
            self.db.table("clients").insert(
                {"username": username, "password": password}
            ).execute()
            return True

        except Exception as e:
            # Returns False if username already exists or other error
            print(f"Error creating user: {e}")
            return False

    def client_exists(self, target_username: str) -> bool:
        # Search for user by username, select only username column
        response = (
            self.db.table("clients")
            .select("username")
            .eq("username", target_username)
            .execute()
        )

        # If data list is not empty — user exists
        return len(response.data) > 0

    def verify_password(self, target_username: str, target_password: str) -> bool:
        # Search for row where both username AND password match
        response = (
            self.db.table("clients")
            .select("username")
            .eq("username", target_username)
            .eq("password", target_password)
            .execute()
        )

        # If found at least one row — credentials are correct
        return len(response.data) > 0
