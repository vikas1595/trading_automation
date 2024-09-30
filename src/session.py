from py5paisa import FivePaisaClient
from dotenv import load_dotenv
import os
import pyotp 
import time

def get_fivepaisa_client():
    load_dotenv()

    totp_key = os.getenv('totp_key')
    cred = {
        "APP_NAME": os.getenv('APP_NAME'),
        "APP_SOURCE": os.getenv('APP_SOURCE'),
        "USER_ID": os.getenv('USER_ID'),
        "PASSWORD": os.getenv('PASSWORD'),
        "USER_KEY": os.getenv('USER_KEY'),
        "ENCRYPTION_KEY": os.getenv('ENCRYPTION_KEY'),
    }

    client = FivePaisaClient(cred=cred)

    totp = pyotp.TOTP(totp_key)
    one_time_password = totp.now()
    client_code = os.getenv('CLIENT_CODE')
    pin = os.getenv('PIN')
    
    client.get_totp_session(client_code, int(one_time_password), pin)
    client.get_access_token()
    
    if client.__dict__['client_code']=="":
        time.sleep(31)
        get_fivepaisa_client()
                       
    return client

# get_fivepaisa_client()   


