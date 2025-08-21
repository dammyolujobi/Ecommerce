from dotenv import load_dotenv
import os
import requests
from datetime import datetime,timedelta

load_dotenv()

class AuthManager:
    def __init__(self):
        self.credentials = []
        self.load_credentials()
    
    def load_credentials(self):
        while True:
            client_id = os.getenv("CLIENT_ID")
            client_secret = os.getenv("CLIENT_SECRET")

            if not client_id or not client_id:
                break

            self.credentials.append({
                "client_id":client_id,
                "client_key": client_secret,
                "access_token": None,
                "expiry":None
            })

    def get_credentials(self):
        return self.credentials

    def generate_access_token(self):

        header = {
            "Content-Type": "application/x-www-form-urlencoded"
        }

        data = {
            "client_id":self.credentials["client_id"],
            "client_key": self.credentials["client_key"],
            "grant_type": "client_credentials"
        }

        response = requests.post(url ='https://idp.flutterwave.com/realms/flutterwave/protocol/openid-connect/token', headers=header, data=data)

        response_json = response.json()

        return response_json
    
    def get_access_token(self):
        
        if self.credentials['access_token'] and self.credentials['expiry'] is None:
            self.generate_access_token(self.credentials)
        
        expiry_delta = self.credentials['expiry'] - datetime .now()

        if expiry_delta < timedelta(minutes=1):
            self.generate_access_token(self.credentials)

        return self.credentials["access_token"]
    

