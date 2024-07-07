from py5paisa import FivePaisaClient
from file_operations import write_file
from dotenv import load_dotenv
import os
import pyotp 
import requests
load_dotenv()

totp_key = os.getenv('totp_key')
cred={
    "APP_NAME":os.getenv('APP_NAME'),
    "APP_SOURCE":os.getenv('APP_SOURCE'),
    "USER_ID":os.getenv('USER_ID'),
    "PASSWORD":os.getenv('PASSWORD'),
    "USER_KEY":os.getenv('USER_KEY'),
    "ENCRYPTION_KEY":os.getenv('ENCRYPTION_KEY'),
    }

client = FivePaisaClient(cred=cred)

totp = pyotp.TOTP(totp_key)
one_time_password = totp.now()

client.get_totp_session(os.getenv('CLIENT_CODE'),int(one_time_password),os.getenv('PIN'))
client.get_access_token()


# a=[{"Exchange":"N","ExchangeType":"C","ScripCode":"2885"},
#    {"Exchange":"N","ExchangeType":"C","ScripData":"ITC_EQ"},
#    ]
# print(client.fetch_market_snapshot(a))
#write_file("./auth_token.txt",auth_token)
print(client.holdings())

#Using Scrip Code :-
client.place_order(OrderType='B',Exchange='N',ExchangeType='C', ScripCode='7', Qty=1, Price=400)