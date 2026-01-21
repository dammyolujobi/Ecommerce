#using .env variables for client and secret.
import os
import requests
from datetime import datetime, timedelta

class AuthManager:
    def __init__(self):
        self.credentials = None
        self.load_credentials()
    
    def load_credentials(self):
        client_id = os.getenv("FLW_CLIENT_ID")
        client_secret = os.getenv("FLW_CLIENT_SECRET")

        if not client_id or not client_secret:
            raise ValueError("Missing FLW_CLIENT_ID or FLW_CLIENT_SECRET in environment variables")

        self.credentials = {
            "client_id": client_id,
            "client_key": client_secret,
            "access_token": None,
            "expiry": None
        }

    def get_credentials(self):
        return self.credentials

    def generate_access_token(self):
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }

        data = {
            "client_id": self.credentials["client_id"],
            "client_secret": self.credentials["client_key"],
            "grant_type": "client_credentials"
        }

        response = requests.post(
            url='https://idp.flutterwave.com/realms/flutterwave/protocol/openid-connect/token',
            headers=headers,
            data=data
        )
        response_json = response.json()

        # store token and expiry
        self.credentials["access_token"] = response_json.get("access_token")
        expires_in = response_json.get("expires_in", 3600)  # default 1 hour
        self.credentials["expiry"] = datetime.now() + timedelta(seconds=expires_in)

        return response_json
    
    def get_access_token(self):
        # If no token or expired, refresh
        if not self.credentials["access_token"] or datetime.now() >= self.credentials["expiry"]:
            self.generate_access_token()

        return self.credentials["access_token"]


if __name__ == "__main__":
    auth = AuthManager()
    token = auth.get_access_token()
    print("Access Token:", token)