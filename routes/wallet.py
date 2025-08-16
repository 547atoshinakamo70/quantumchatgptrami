from flask import Blueprint, request, jsonify, abort
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3, os, secrets
wallet_bp = Blueprint("wallet", __name__)
DB_PATH = os.environ.get("WALLET_DB", "wallet.db")

def _db():
    con = sqlite3.connect(DB_PATH)
    con.execute('CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT,email TEXT UNIQUE,passhash TEXT,seed TEXT)')
    return con

@wallet_bp.post("/register")
def register():
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip().lower(); password = data.get("password") or ""
    if not email or not password: abort(400)
    passhash = generate_password_hash(password); seed = secrets.token_hex(16)
    con = _db()
    try:
        con.execute("INSERT INTO users(email,passhash,seed) VALUES(?,?,?)",(email,passhash,seed)); con.commit()
    except sqlite3.IntegrityError: abort(409)
    return jsonify({"ok": True})

@wallet_bp.post("/login")
def login():
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip().lower(); password = data.get("password") or ""
    con = _db(); cur = con.execute("SELECT id,passhash,seed FROM users WHERE email=?",(email,)); row = cur.fetchone()
    if not row or not check_password_hash(row[1], password): abort(401)
    token = secrets.token_urlsafe(24)
    return jsonify({"ok": True, "token": token, "user_id": row[0]})
