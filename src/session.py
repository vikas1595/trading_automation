from py5paisa import FivePaisaClient
from dotenv import load_dotenv
import os
import pyotp 
import time
from functools import cached_property
load_dotenv()

class user:
    def __init__(self):
        self.USER_KEY = os.getenv("USER_KEY")
        self.USER_ID = os.getenv("USER_ID")
        self.ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")
        self.CLIENT_CODE = os.getenv("CLIENT_CODE")
        self.PASSWORD = os.getenv("PASSWORD")
        self.APP_NAME = os.getenv("APP_NAME")
        self.APP_SOURCE = os.getenv("APP_SOURCE")
        self.TOTP_KEY = os.getenv("TOTP_KEY")
        self.PIN=os.getenv("PIN")
    def generate_fivepaisa_cred(self):
        return {
            "USER_KEY": self.USER_KEY,
            "USER_ID": self.USER_ID,
            "ENCRYPTION_KEY": self.ENCRYPTION_KEY,
            "PASSWORD": self.PASSWORD,
            "APP_NAME": self.APP_NAME,
            "APP_SOURCE": self.APP_SOURCE,
        }
    
class session(user):

    @property
    def active_session_client(self)->FivePaisaClient:
        return FivePaisaClient(self.generate_fivepaisa_cred())
    
    @cached_property
    def access_token(self):
        client = self.active_session_client
        client.get_totp_session(self.CLIENT_CODE, int(self.generate_otp()), self.PIN)
        return client.get_access_token()

    def generate_otp(self):
        totp=pyotp.TOTP(self.TOTP_KEY)
        return totp.now()
