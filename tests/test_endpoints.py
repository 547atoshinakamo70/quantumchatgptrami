from app import app as flask_app

def test_health():
    c = flask_app.test_client(); r = c.get("/healthz"); assert r.status_code == 200

def test_qnn():
    c = flask_app.test_client(); r = c.post("/qnn/infer", json={"signals": {"trend_strength":0.6}})
    assert r.status_code == 200
    data = r.get_json(); assert "roadmap" in data
