import os
import random
import requests
from session import get_fivepaisa_client
from py5paisa import FivePaisaClient


class order:
    def __init__(
        self,
        client: FivePaisaClient,
        order_type: str,
        scrip_code: str,
        qty: int,
        price: float,
        ah_placed,
    ):
        self.client = client
        self.token = client.get_access_token()
        self.order_type = order_type
        self.exchange = "N"
        self.exchange_type = "C"
        self.scrip_code = scrip_code
        self.qty = qty
        self.price = price
        self.is_intraday = True
        self.ah_placed = ah_placed
        self.user_key = os.getenv("USER_KEY")
        self.user_id = os.getenv("USER_ID")
        self.encryption_key = os.getenv("ENCRYPTION_KEY")
        self.client_code = os.getenv("CLIENT_CODE")

    def place_order(self, remote_order_id):
        url = "https://Openapi.5paisa.com/VendorsAPI/Service1.svc/V1/PlaceOrderRequest"

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"bearer {self.token}",
        }

        payload = {
            "head": {"key": self.user_key, "Key": self.user_key},
            "body": {
                "RequestToken": self.token,
                "EncryKey": self.encryption_key,
                "UserId": self.user_id,
                "OrderType": self.order_type,
                "Exchange": self.exchange,
                "ExchangeType": self.exchange_type,
                "ScripCode": self.scrip_code,
                "Price": self.price,
                "Qty": self.qty,
                "AHPlaced": self.ah_placed,
                "RemoteOrderID": remote_order_id,
            },
        }

        response = requests.post(url, json=payload, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def get_exch_order_id(self, order_id, user_key):
        payload = {
            "head": {"key": f"{self.user_key}", "Key": f"{self.user_key}" },
            "body": {
                "ClientCode": self.client_code,
                "OrdStatusReqList": [{"Exch": "N", "RemoteOrderID": order_id}],
            },
        }
        
        url = "https://Openapi.5paisa.com/VendorsAPI/Service1.svc/V2/OrderStatus"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"bearer {self.token}",
        }
        response = requests.post(url, json=payload, headers=headers)
        return response.json()


# def place_order(
#     order_type,
#     exchange,
#     exchange_type,
#     scrip_code,
#     qty,
#     remote_order_id,
#     price=0,
#     is_intraday=True,
#     ah_placed="N",
# ):
#     url = "https://Openapi.5paisa.com/VendorsAPI/Service1.svc/V1/PlaceOrderRequest"

#     headers = {
#         "Content-Type": "application/json",
#         "Authorization": f"bearer {client.get_access_token()}",
#     }

#     payload = {
#         "head": {"key": os.getenv("USER_KEY"), "Key": os.getenv("USER_KEY")},
#         "body": {
#             "RequestToken": client.get_access_token(),
#             "EncryKey": os.getenv("ENCRYPTION_KEY"),
#             "UserId": os.getenv("USER_ID"),
#             "OrderType": order_type,
#             "Exchange": exchange,
#             "ExchangeType": exchange_type,
#             "ScripCode": scrip_code,
#             "Price": price,
#             "Qty": qty,
#             "AHPlaced": ah_placed,
#             "RemoteOrderID": remote_order_id,
#         },
#     }

#     response = requests.post(url, json=payload, headers=headers)

#     if response.status_code == 200:
#         return response.json()
#     else:
#         response.raise_for_status()


# def get_exch_order_id(client, order_id, user_key):
#     payload = {
#         "head": {"key": f"{user_key}", "Key": f"{user_key}"},
#         "body": {
#             "ClientCode": os.getenv("CLIENT_CODE"),
#             "OrdStatusReqList": [{"Exch": "N", "RemoteOrderID": order_id}],
#         },
#     }
#     url = "https://Openapi.5paisa.com/VendorsAPI/Service1.svc/V2/OrderStatus"
#     headers = {
#         "Content-Type": "application/json",
#         "Authorization": f"bearer {client.get_access_token()}",
#     }
#     response = requests.post(url, json=payload, headers=headers)
#     return response.json()


# client = get_fivepaisa_client()

# result = place_order(
#     order_type="B",
#     exchange="N",
#     exchange_type="C",
#     scrip_code="25756",
#     price=2.67,
#     qty=1,
#     remote_order_id="123456",
#     ah_placed="Y",
# )
# # get exchnageorderid
# order_status = get_exch_order_id(client, 123456, os.getenv("USER_KEY"))
# print(order_status)
