from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Optional
from .wormhole_samplers import sample8, CATEGORIES

@dataclass
class Signals:
    trend_strength: float = 0.5
    volatility: float = 0.5
    dev_velocity: float = 0.5
    user_frustration: float = 0.2
    infra_cost: float = 0.4
    security_findings: float = 0.1

def _clip01(x: float) -> float: return max(0.0, min(1.0, float(x)))

SUGGESTIONS = {
    "latency":  "Streaming, cache logits, batching; monitor p95/p99.",
    "retrieval":"RAG por dominios + refresco incremental + re-ranker.",
    "security": "Firmas en RPC, validación fuerte, límites y fuzz/Audit CI.",
    "wallet":   "Login email+pass, cifrado local, 2FA opcional, cuentas observadas.",
    "mining":   "Planificador HTTP con colas/backoff; métricas por worker.",
    "zk":       "Precompila circuitos, caché de pruebas, colas async.",
    "coinjoin": "Selector BnB + políticas; coinjoin programable por metas.",
    "ui":       "Onboarding simple, plantillas y diagnósticos visibles.",
}

def rank_improvements(weights: dict, sig: Signals, top_k: int = 6):
    boosts = {
        "security": 1.0 + 0.7*_clip01(sig.security_findings),
        "latency":  1.0 + 0.6*_clip01(sig.user_frustration),
        "retrieval":1.0 + 0.4*_clip01(sig.trend_strength),
        "ui":       1.0 + 0.3*_clip01(sig.trend_strength),
        "mining":   1.0 + 0.4*_clip01(sig.dev_velocity),
        "zk":       1.0 + 0.4*_clip01(sig.dev_velocity),
        "coinjoin": 1.0 + 0.3*_clip01(sig.volatility),
        "wallet":   1.0 + 0.4*_clip01(sig.user_frustration),
    }
    scored = []
    for cat, base in weights.items():
        scored.append((cat, float(base)*boosts.get(cat,1.0)))
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:top_k]

def predict_roadmap(signals_dict: Dict[str, float], mode: str = "auto", seed: Optional[int] = None) -> Dict:
    sig = Signals(
        trend_strength=signals_dict.get("trend_strength",0.5),
        volatility=signals_dict.get("volatility",0.5),
        dev_velocity=signals_dict.get("dev_velocity",0.5),
        user_frustration=signals_dict.get("user_frustration",0.2),
        infra_cost=signals_dict.get("infra_cost",0.4),
        security_findings=signals_dict.get("security_findings",0.1),
    )
    probs = sample8(signals_dict, mode=mode, seed=seed)
    weights = {CATEGORIES[i]: float(probs[i]) for i in range(len(CATEGORIES))}
    ranked = rank_improvements(weights, sig, top_k=6)
    return {
        "mode": mode,
        "weights": weights,
        "recommendations": [
            {"category": c, "score": round(s,6), "suggestion": SUGGESTIONS[c]}
            for c,s in ranked
        ]
    }
