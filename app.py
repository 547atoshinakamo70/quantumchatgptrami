import os
from flask import Flask, request, abort
from routes.health import health_bp
from routes.qnn import qnn_bp
from routes.research import research_bp
from routes.mining import mining_bp
from routes.wallet import wallet_bp
from routes.zk import zk_bp
from routes.coinjoin import coinjoin_bp
from routes.blockchain import bchain_bp
from routes.bitcoin import btc_bp
from routes.rag import rag_bp

API_KEY = os.environ.get("API_KEY")

def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")
    # Blueprints
    app.register_blueprint(health_bp, url_prefix="/")
    app.register_blueprint(qnn_bp, url_prefix="/qnn")
    app.register_blueprint(research_bp, url_prefix="/research")
    app.register_blueprint(mining_bp, url_prefix="/mining")
    app.register_blueprint(wallet_bp, url_prefix="/wallet")
    app.register_blueprint(zk_bp, url_prefix="/zk")
    app.register_blueprint(coinjoin_bp, url_prefix="/coinjoin")
    app.register_blueprint(bchain_bp, url_prefix="/bchain")
    app.register_blueprint(btc_bp, url_prefix="/btc")
    app.register_blueprint(rag_bp, url_prefix="/rag")

    @app.before_request
    def _auth():
        # let UI & health pass
        public = {"/", "/healthz", "/static/style.css"}
        if request.path in public or request.path.startswith("/static/"):
            return
        if API_KEY and request.headers.get("X-API-Key") != API_KEY:
            abort(401)
    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=int(os.environ.get("PORT", "8000")), debug=False)
