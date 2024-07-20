from src.session import get_fivepaisa_client

if __name__=='__main__':
    client=get_fivepaisa_client()
    print(client.holdings())
    _is_close=input(' close the session Y,N: ')
    if _is_close=="Y":
        exit
    else:
        pass