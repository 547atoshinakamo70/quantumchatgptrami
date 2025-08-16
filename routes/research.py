from flask import Blueprint, jsonify, request
from duckduckgo_search import DDGS
from bs4 import BeautifulSoup
import httpx

research_bp = Blueprint("research", __name__)

async def fetch_html(client: httpx.AsyncClient, url: str):
    try:
        r = await client.get(url, timeout=10)
        r.raise_for_status()
        return r.text
    except Exception:
        return ""

def summarize(text: str, limit: int = 400):
    t = (text or "").strip()
    return (t[: limit - 3] + "...") if len(t) > limit else t

@research_bp.post("/search")
async def search_api():
    data = request.get_json(silent=True) or {}
    query = (data.get("query") or "").strip()
    k = int(data.get("k") or 3)

    results = []
    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=k):
            results.append({"title": r.get("title"), "href": r.get("href")})

    out = []
    async with httpx.AsyncClient(follow_redirects=True) as client:
        for item in results:
            html = await fetch_html(client, item["href"])
            soup = BeautifulSoup(html, "html.parser")
            text = summarize(soup.get_text(" ", strip=True))
            out.append({"title": item["title"], "url": item["href"], "summary": text})

    return jsonify({"query": query, "items": out})
