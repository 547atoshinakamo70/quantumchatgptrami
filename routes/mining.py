from flask import Blueprint, request, jsonify
import time, queue, threading
mining_bp = Blueprint("mining", __name__)
_jobs = queue.Queue(); _results = {}; _lock = threading.Lock()

@mining_bp.post("/submit")
def submit_job():
    payload = request.get_json(silent=True) or {}
    job = {"id": str(time.time_ns()), "payload": payload, "status": "queued", "ts": time.time()}
    _jobs.put(job); return jsonify(job), 202

@mining_bp.post("/claim")
def claim_job():
    try: job = _jobs.get_nowait()
    except queue.Empty: return jsonify({"job": None}), 200
    job["status"]="claimed"; return jsonify({"job": job}), 200

@mining_bp.post("/result/<job_id>")
def submit_result(job_id):
    data = request.get_json(silent=True) or {}
    with _lock: _results[job_id] = {"result": data, "ts": time.time()}
    return jsonify({"ok": True})

@mining_bp.get("/result/<job_id>")
def get_result(job_id): return jsonify(_results.get(job_id) or {"result": None})
