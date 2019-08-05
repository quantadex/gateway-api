from firebase import Firebase

config = {
  "apiKey": "AIzaSyCwbyI8f9wUMIXE34-MZRKM_O9xixMiJn8",
  "authDomain": "quantadice-01.firebaseapp.com",
  "databaseURL": "https://quantadice-01.firebaseio.com",
  "storageBucket": "quantadice-01.appspot.com"
}

firebase = Firebase(config)

db = firebase.database()

def broadcastFirebase(channel, betId, user, payout, roll, profit):
    data = {
        "betId": betId,
        "user": user,
        "payout": payout,
        "roll": roll,
        "profit": profit
    }
    results = db.child("quantadice/" + channel).push(data)

import urllib
import json
import time

def fetchData(start, count):
    url = 'https://wya99cec1d.execute-api.us-east-1.amazonaws.com/testnet/account?filter_field=operation_type&filter_value=50&sort_by=operation_id_num&from_={}&size={}'.format(start, count)
    print(url)
    jsonobj = json.loads(urllib.request.urlopen(url).read())
    return jsonobj

CHANNEL="history"
SIZE = 5

def streamData():
    start = 100

    while True:
        print("Streaming from ", start, SIZE)
        data = fetchData(start, SIZE)

        for tx in data:
            betId = tx["operation_history"]["op_object"]["tx"],
            user = tx["account_history"]["account"],
            payout = tx["operation_history"]["op_object"]["payout"]["amount"],
            roll = tx["operation_history"]["op_object"]["outcome"],
            profit = tx["operation_history"]["op_object"]["payout"]["amount"]

            broadcastFirebase(CHANNEL, betId, user, payout, roll, profit)
        start = start + len(data)
        time.sleep(2)

print(streamData())
