import os
import requests
from session import get_fivepaisa_client
def place_order(user_key, access_token, order_type, exchange, exchange_type, 
                scrip_code, qty, price=0, stop_loss_price=None, 
                dis_qty=None, is_intraday=True, ah_placed='N', remote_order_id=None):
    url = "https://Openapi.5paisa.com/VendorsAPI/Service1.svc/V1/PlaceOrderRequest"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"bearer {access_token}"
    }
    
#     payload = {
# 	"head": {
# 		"key": "IEmwWeCtDyhbmMUXBq4XWPX383rvnk7m",
# 		"Key": "IEmwWeCtDyhbmMUXBq4XWPX383rvnk7m"
# 	},
# 	"body": {
# 		"RequestToken": f"{access_token}",
# 		"EncryKey": "6VfIc2NT8DW5Iiw3UfuLwNvbTjkSyeDx",
# 		"UserId": "FIggoLnCIkK",
# 		"OrderType": "B",
# 		"ScripCode": 59178,
# 		"Qty": 30,
# 		"Price": 0,
# 		"Exchange": "N",
# 		"ExchangeType": "D",
# 		"AHPlaced": "Y"
# 	}
# }
    payload=  {
        "head": {
            "key": f"{user_key}",
            "Key": f"{user_key}"
        },
        "body": {
            "RequestToken": f"{access_token}",
            "EncryKey": "6VfIc2NT8DW5Iiw3UfuLwNvbTjkSyeDx",
		    "UserId": "FIggoLnCIkK",
            "OrderType": "B",
            "Exchange": exchange,
            "ExchangeType": exchange_type,
            "ScripCode": scrip_code,
            "Price": price,
            "Qty": qty,
            "AHPlaced": ah_placed
        }
    }
    
    # {
    # "head": {
    #     "key": "{{Your App Key}}"
    # },
    # "body": {
    #     "Exchange":"N",
    #     "ExchangeType":"C",
    #     "ScripCode":"1660",
    #     "Price": "445",
    #     "StopLossPrice": "0",
    #     "OrderType": "Buy",
    #     "Qty": 1,
    #     "DisQty": "0",
    #     "IsIntraday": True,
    #     "iOrderValidity": "0",
    #     "AHPlaced":"N"
#     # }
# }
# {'body': {'BrokerOrderID': 168401497, 'ClientCode': '53200425', 'Exch': 'N', 'ExchOrderID': '0', 
# 'ExchType': 'D', 'LocalOrderID': 0, 'Message': 'Success', 'RMSResponseCode': 1, 'RemoteOrderID': '', 'ScripCode': 59178, 'Status': 0, 'Time': '/Date(1727634600000+0530)/'},
#   'head': {'responseCode': '5PPlaceOrdReqV1', 'status': '0', 'statusDescription': 'Success'}}
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

# Example usage:
client = get_fivepaisa_client()

result = place_order(user_key=os.getenv('USER_KEY'), access_token=client.get_access_token(),
                      order_type="B", exchange="N", 
                      exchange_type="C", scrip_code="59178",
                          qty=15
                        ,ah_placed="Y", remote_order_id="123456")
print(result)