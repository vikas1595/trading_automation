from py5paisa.order import Order, OrderType, Exchange
from py5paisa import FivePaisaClient
from session import get_fivepaisa_client
from exceldata import entry_signals
import time
from excel_operations import update_excel
def place_order(client:FivePaisaClient,order_type:str,ScripCode:str,qty:int,IsIntraday:bool=True):
    
    order_data={
        "OrderType":order_type,
        "ScripCode": ScripCode,
        "Qty":qty,
        "Price":0,
        "Exchange": "N",
        "ExchangeType": "D",
        "AHPlaced":"Y"
    }

    #Using Scrip Code :-
    client.place_order(**order_data)
    file_path = './5paisatrade_new.xlsm'
    # Append the updates for each row
    updates=({
        'row': 4,  # Excel rows are 1-indexed, and there's a header row
        'exchorderid': 500,
        'entry_price': 100
    })
    update_excel(file_path, updates)


def place_batch_orders(client,entry_orders):
    for item in entry_orders:
        ScripCode=int(float(item.get('script_code')))
        qty=item.get('lot_size')*item.get('qty')
        place_order(client,order_type="B",ScripCode=ScripCode,qty=qty,IsIntraday=True)



for i in range(20):
    client=get_fivepaisa_client()
    entry_orders=entry_signals()
    place_batch_orders(client,entry_orders)
    print(f"batch finished: {i}")
    time.sleep(120)
    






