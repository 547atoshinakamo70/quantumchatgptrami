from flask import Blueprint, request, jsonify
import os
from quantum.predictor_core import predict_roadmap

qnn_bp = Blueprint("qnn", __name__)

def _default_signals():
    return {
        "trend_strength": 0.7, "volatility": 0.35, "dev_velocity": 0.6,
        "user_frustration": 0.25, "infra_cost": 0.4, "security_findings": 0.2,
    }

@qnn_bp.post("/infer")
def infer():
    data = request.get_json(silent=True) or {}
    signals = data.get("signals") or _default_signals()
    mode = data.get("mode") or os.getenv("WORMHOLE_SAMPLER_MODE", "auto")
    seed = data.get("seed")
    return jsonify({"roadmap": predict_roadmap(signals, mode=mode, seed=seed), "signals": signals})
