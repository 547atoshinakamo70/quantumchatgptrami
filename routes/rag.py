from flask import Blueprint, request, jsonify
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import threading

rag_bp = Blueprint("rag", __name__)

_docs = []; _vectorizer = TfidfVectorizer(); _matrix = None
_lock = threading.Lock()

@rag_bp.post("/ingest")
def ingest():
    global _matrix
    data = request.get_json(silent=True) or {}
    docs = data.get("docs") or []
    with _lock:
        _docs.extend(docs)
        _matrix = _vectorizer.fit_transform(_docs) if _docs else None
    return jsonify({"count": len(_docs)})

@rag_bp.post("/query")
def query():
    q = (request.get_json(silent=True) or {}).get("q") or ""
    if not _docs: return jsonify({"matches": []})
    qv = _vectorizer.transform([q])
    sims = cosine_similarity(qv, _matrix)[0]
    idx = sims.argsort()[::-1][:5]
    matches = [{"doc": _docs[i], "score": float(sims[i])} for i in idx]
    return jsonify({"matches": matches})
