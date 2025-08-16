from flask import Blueprint, request, jsonify
from integrations.coinjoin_planner import plan_coinjoin
coinjoin_bp = Blueprint("coinjoin", __name__)

@coinjoin_bp.post("/plan")
def plan():
    data = request.get_json(silent=True) or {}
    utxos = data.get("utxos") or []; targets = data.get("targets") or []
    policy = data.get("policy") or {}
    plan = plan_coinjoin(utxos, targets, policy)
    return jsonify(plan)
