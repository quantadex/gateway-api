from sendy.api import SendyAPI
import os

def subscribe(email:str, account:str):
    api = SendyAPI(host='http://sendy.env.quantadex.com/', api_key=os.environ.get("SENDY_API"))
    api.subscribe(os.environ.get("SENDY_SUBSCRIBE_LIST"), email, '', account=account)



#subscribe("quocble@gmail.com", "cryptoQuoc")