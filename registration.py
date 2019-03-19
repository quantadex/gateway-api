from bitshares import BitShares, storage
from bitshares.wallet import Wallet
import os

def register_user(name, owner_key, registrar, referrer):
    rpc_url = os.environ.get("RPC_URL","ws://testnet-02.quantachain.io:8090")
    keys = [os.environ.get("KEY")]

    conn = BitShares(rpc_url, key_store=storage.InRamPlainKeyStore(), keys = keys)
    return conn.create_account(name, registrar, referrer, 100, owner_key, owner_key, owner_key)


#res = register_user("dead02", "QA4yeoMtbdDQeSh92HahSg1GPmh1yxg8Em1qRV94ZwJXvSu1huyq","1.2.15","1.2.15")
#print(res)