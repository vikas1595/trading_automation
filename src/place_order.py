import json
import os
import random
import requests
import sqlite3
from src.login import Session
from dataclasses import dataclass
from src.order_database import OrderDatabase


@dataclass
class Order:
    order_type: str
    scrip_code: str
    qty: int
    price: float | None = 0
    ah_placed: str | None = "N"
    exchange: str | None = "N"
    exchange_type: str | None = "C"
    is_intraday: bool | None = True
    remote_order_id: int = random.randint(100000, 999999)
    stop_loss_price: float | None = None
    broker_order_id: str | None = None
    last_trade_price: float | None = None


class OrderExecutor:
    def __init__(self, session: Session, order: Order):
        self.session = session
        self.order = order

    def place(self):
        url = "https://Openapi.5paisa.com/VendorsAPI/Service1.svc/V1/PlaceOrderRequest"

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"bearer {self.session.access_token}",
        }

        payload = {
            "head": {"key": self.session.current_user.USER_KEY, "Key": self.session.current_user.USER_KEY},
            "body": {
                "RequestToken": self.session.access_token,
                "EncryKey": self.session.current_user.ENCRYPTION_KEY,
                "UserId": self.session.current_user.USER_ID,
                "OrderType": self.order.order_type,
                "Exchange": self.order.exchange,
                "ExchangeType": self.order.exchange_type,
                "ScripCode": self.order.scrip_code,
                "Price": self.order.price,
                "Qty": self.order.qty,
                "AHPlaced": self.order.ah_placed,
                "RemoteOrderID": self.order.remote_order_id
            },
        }
        if self.order.stop_loss_price:
            payload["body"]["StopLossPrice"] = self.order.stop_loss_price

        response = requests.post(url, json=payload, headers=headers)

        if response.status_code == 200:
            response_data = response.json()
            # status = response_data.get('body', {}).get('Status')
            # buying_price = response_data.get('body', {}).get('Price')
            # broker_order_id = response_data.get('body', {}).get('BrokerOrderID')
            # self.db.save_order(self.order, status, buying_price, broker_order_id)
            return response_data
        else:
            response.raise_for_status()

    def order_status(self):
        payload = {
            "head": {
                "key": f"{self.session.current_user.USER_KEY}",
                "Key": f"{self.session.current_user.USER_KEY}",
            },
            "body": {
                "ClientCode": self.session.current_user.CLIENT_CODE,
                "OrdStatusReqList": [
                    {"Exch": "N", "RemoteOrderID": self.order.remote_order_id}
                ],
            },
        }

        url = "https://Openapi.5paisa.com/VendorsAPI/Service1.svc/V2/OrderStatus"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"bearer {self.session.access_token}",
        }
        response = requests.post(url, json=payload, headers=headers)
        return response.json()

    def get_market_feed(self):
        url = "https://Openapi.5paisa.com/VendorsAPI/Service1.svc/V1/MarketFeed"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"bearer {self.session.access_token}",
        }
        payload = {
            "head": {
                "key": f"{self.session.current_user.USER_KEY}",
            },
            "body": {
                "MarketFeedData": [
                    {
                        "Exch": self.order.exchange, 
                        "ExchType": self.order.exchange_type,  
                        "ScripCode": self.order.scrip_code,  
                    }
                ],
                "LastRequestTime": "/Date(0)/",
                "RefreshRate": "H",
            },
        }

        # Send POST request
        response = requests.post(url, headers=headers, json=payload)

        # Parse response
        if response.status_code == 200:
            data = response.json().get("body", {}).get("Data", [])
            return data if data else None
        else:
            print(f"HTTP Error: {response.status_code}")


# current_session = session()
# test_order = Order(order_type="B", scrip_code="25756", qty=1, price=0, ah_placed="Y")
# order_executor = OrderExecutor(current_session, test_order)

# # Fetch LastRate using get_market_feed
# market_feed = order_executor.get_market_feed()
# if not market_feed:
#     raise Exception("Failed to fetch market feed data")

# last_rate = market_feed[0].get("LastRate")
# stop_loss_price = last_rate - 30

# # Update order with stop loss price
# test_order.stop_loss_price = stop_loss_price

# # Place stop loss buy order
# order_executor.place()

# # Fetch ExchangeOrderId using order_status
# order_status_response = order_executor.order_status()
# exchange_order_id = order_status_response.get('body', {}).get('OrdStatusReqList', [{}])[0].get('ExchOrderID')

# # Update order with ExchangeOrderId
# order_executor.db.update_order_exchange_id(test_order.remote_order_id, exchange_order_id)
