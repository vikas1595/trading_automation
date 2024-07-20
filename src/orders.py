from py5paisa.order import Order, OrderType, Exchange
from session import get_fivepaisa_client

def place_order(order_type:str,ScripCode:str,qty:int,IsIntraday:bool=True):
    client=get_fivepaisa_client()
    order_data={
        "OrderType":order_type,
        "ScripCode": ScripCode,
        "Qty":qty,
        "Price":0,
        "Exchange": "N",
        "ExchangeType": "D"
    }

    #Using Scrip Code :-
    client.place_order(**order_data)

place_order(order_type="B",ScripCode="36970",qty=15,IsIntraday=True)
print(1)


