import os
try:
    from bitcoinrpc.authproxy import AuthServiceProxy
except Exception:
    AuthServiceProxy = None

def get_client():
    if AuthServiceProxy is None: return None
    rpcuser = os.environ.get("BTC_RPCUSER", "user")
    rpcpassword = os.environ.get("BTC_RPCPASSWORD", "pass")
    rpchost = os.environ.get("BTC_RPCHOST", "127.0.0.1")
    rpcport = os.environ.get("BTC_RPCPORT", "8332")
    return AuthServiceProxy(f"http://{rpcuser}:{rpcpassword}@{rpchost}:{rpcport}")
