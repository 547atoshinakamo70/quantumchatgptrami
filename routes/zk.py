from flask import Blueprint, request, jsonify
from integrations.zk_engine import prove, verify
zk_bp = Blueprint("zk", __name__)

@zk_bp.post("/prove")
def zk_prove():
    data = request.get_json(silent=True) or {}
    statement = data.get("statement") or {}
    witness = data.get("witness") or {}
    proof = prove(statement, witness)
    return jsonify({"proof": proof})

@zk_bp.post("/verify")
def zk_verify():
    data = request.get_json(silent=True) or {}
    statement = data.get("statement") or {}
    proof = data.get("proof") or {}
    ok = verify(statement, proof)
    return jsonify({"valid": bool(ok)})
