from flask import Blueprint, jsonify, render_template
health_bp = Blueprint("health", __name__)

@health_bp.get("/healthz")
def health(): return jsonify(status="ok")

@health_bp.get("/")
def index(): return render_template("index.html")
