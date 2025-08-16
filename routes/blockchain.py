from flask import Blueprint, jsonify
import os, httpx
bchain_bp = Blueprint("bchain", __name__)
CHAIN_URL = os.environ.get("CHAIN_RPC_URL", "http://2.137.118.154:5000")

@bchain_bp.get("/stats")
async def stats():
    async with httpx.AsyncClient() as client:
        try:
            r = await client.get(f"{CHAIN_URL}/stats", timeout=5.0); r.raise_for_status()
            return jsonify(r.json())
        except Exception:
            return jsonify({"ok": False, "error": "unreachable"}), 502
