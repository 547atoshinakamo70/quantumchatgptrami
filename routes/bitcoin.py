from flask import Blueprint, jsonify
from integrations.bitcoin_rpc import get_client
btc_bp = Blueprint("btc", __name__)

@btc_bp.get("/info")
def info():
    cli = get_client()
    if not cli: return jsonify({"ok": False, "error":"rpc not configured"}), 400
    try: return jsonify(cli.getblockchaininfo())
    except Exception as e: return jsonify({"ok": False, "error": str(e)}), 500
