from py5paisa import FivePaisaClient
from dotenv import load_dotenv
import os
import pyotp
import time
from functools import cached_property

load_dotenv()


class User:
    def __init__(self):
        self.USER_KEY = os.getenv("USER_KEY")
        self.USER_ID = os.getenv("USER_ID")
        self.ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")
        self.CLIENT_CODE = os.getenv("CLIENT_CODE")
        self.PASSWORD = os.getenv("PASSWORD")
        self.APP_NAME = os.getenv("APP_NAME")
        self.APP_SOURCE = os.getenv("APP_SOURCE")
        self.TOTP_KEY = os.getenv("TOTP_KEY")
        self.PIN = os.getenv("PIN")


class Session:
    def __init__(self):
        self.current_user = User()

    @property
    def active_session_client(self) -> FivePaisaClient:
        return FivePaisaClient(self.generate_fivepaisa_cred())

    @cached_property
    def access_token(self):
        client = self.active_session_client
        client.get_totp_session(
            self.current_user.CLIENT_CODE,
            int(self.generate_otp()),
            self.current_user.PIN,
        )
        return client.get_access_token()

    def generate_fivepaisa_cred(self):
        return {
            "USER_KEY": self.current_user.USER_KEY,
            "USER_ID": self.current_user.USER_ID,
            "ENCRYPTION_KEY": self.current_user.ENCRYPTION_KEY,
            "PASSWORD": self.current_user.PASSWORD,
            "APP_NAME": self.current_user.APP_NAME,
            "APP_SOURCE": self.current_user.APP_SOURCE,
        }

    def generate_otp(self):
        totp = pyotp.TOTP(self.current_user.TOTP_KEY)
        return totp.now()
