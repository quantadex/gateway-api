from bitshares import BitShares, storage
from bitshares.wallet import Wallet
from bitshares.account import Account
import os
from graphenebase.ecdsa import verify_message, sign_message
from binascii import hexlify, unhexlify
import json
from bitshares.exceptions import (
    InvalidMessageSignature,
    AccountExistsException,
    AccountDoesNotExistsException,
    InvalidMemoKeyException,
    WrongMemoKey
)
import hmac
import hashlib
from bitsharesbase.account import PublicKey
import base64

def get_connection():
    rpc_url = os.environ.get("RPC_URL","ws://testnet-02.quantachain.io:8090")
    keys = [os.environ.get("KEY")]
    return BitShares(rpc_url, key_store=storage.InRamPlainKeyStore(), keys = keys)


def register_user(name, owner_key, registrar, referrer):
    conn = get_connection()
    free_QDEX = float(os.environ.get("FREE_QDEX"))
    account_tx = conn.create_account(name, registrar, referrer, 100, owner_key, owner_key, owner_key)
    conn.transfer(name, free_QDEX, "QDEX", "free QDEX", registrar)

def register_airdrop(msgRaw, registrar, referrer, signature):
    print(msgRaw, signature)
    if signature == None:
        raise InvalidMessageSignature("No server-server signature.")

    msgObj = json.loads(msgRaw)
    sig = hmac.new(bytes(os.environ.get("HMAC_SECRET"),'UTF-8'), msgRaw, hashlib.sha256)
    sigBase64 = str(base64.encodebytes(sig.digest()))
    conn = get_connection()

    print(msgRaw, signature, sigBase64)
    if sigBase64 == signature:
        raise InvalidMessageSignature("Signature mismatch")

    try:
        acc = Account(msgObj["name"], blockchain_instance=conn)
        print(acc)
        raise AccountExistsException("Account already exist. Login @ trade.quantadex.com with your private key")
    except AccountDoesNotExistsException:
        pass

    free_QDEX = float(os.environ.get("FREE_QDEX"))
    account_tx = conn.create_account(msgObj["name"], registrar, referrer, 100, msgObj["public_key"], msgObj["public_key"], msgObj["public_key"])
    conn.transfer(msgObj["name"], free_QDEX, "QDEX", "free QDEX", registrar)
    conn.transfer(msgObj["name"], msgObj["amount"], "QAIR", "Airdrop tokens", registrar)
    return { "result" : "Account successfully claimed. Login @ trade.quantadex.com with your private key" }

#res = register_user("dead02", "QA4yeoMtbdDQeSh92HahSg1GPmh1yxg8Em1qRV94ZwJXvSu1huyq","1.2.15","1.2.15")
#print(res)


def testAirDrop():
    msg = {
        "name": "dead11",
        "amount": 100,
        "public_key": "QA4yeoMtbdDQeSh92HahSg1GPmh1yxg8Em1qRV94ZwJXvSu1huyq"
    }
    msgStr = json.dumps(msg)
    print(msgStr)
    sig = hmac.new(bytes(os.environ.get("HMAC_SECRET"),'UTF-8'), bytes(msgStr,'UTF-8'), hashlib.sha256)
    sigBase64 = base64.urlsafe_b64encode(sig.digest())
    print(msg,msgStr,sigBase64)
    res = register_airdrop(msgStr, "1.2.15", "1.2.15", sigBase64)


#testAirDrop()