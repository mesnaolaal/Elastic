#!/usr/bin/env python3
"""Web simulatua: hiri-sentsoreen irakurketak API REST bidez.

Endpoint-ak:
  GET /api/sentsoreak  -> sentsore guztien azken irakurketak (JSON)
  GET /osasuna         -> zerbitzuaren egoera (tarteka 503 itzultzen du)
  GET /api/akatsa      -> beti 500 (log-etan akatsak sortzeko)

Flask 127.0.0.1:5000 helbidean entzuten du. Nginx-ek (80 portua) eskaerak
birbidaltzen dizkio eta sarbide-log-a JSON formatuan idazten du:
/var/log/nginx/access.log
"""
import os
import random
from datetime import datetime, timezone

from flask import Flask, jsonify

# Irakurketen %15 "zikina" da. Aldatzeko: ZIKINKERIA=0 (garbia) edo ZIKINKERIA=0.3
ZIKINKERIA_PROBABILITATEA = float(os.environ.get("ZIKINKERIA", "0.15"))

# (id, mota, unitatea, zona, latitudea, longitudea)
SENTSOREAK = [
    ("temp-001", "temperatura", "°C", "Erdialdea", 43.3183, -1.9812),
    ("temp-002", "temperatura", "°C", "Gros", 43.3258, -1.9757),
    ("temp-003", "temperatura", "°C", "Antiguo", 43.3052, -1.9926),
    ("hez-001", "hezetasuna", "%", "Erdialdea", 43.3190, -1.9800),
    ("hez-002", "hezetasuna", "%", "Egia", 43.3197, -1.9694),
    ("hez-003", "hezetasuna", "%", "Gros", 43.3249, -1.9740),
    ("co2-001", "co2", "ppm", "Erdialdea", 43.3175, -1.9825),
    ("co2-002", "co2", "ppm", "Antiguo", 43.3060, -1.9910),
    ("co2-003", "co2", "ppm", "Egia", 43.3205, -1.9680),
]

app = Flask(__name__)


def balio_normala(mota):
    if mota == "temperatura":
        return round(random.gauss(18, 4), 1)
    if mota == "hezetasuna":
        return round(min(100, max(0, random.gauss(65, 12))), 1)
    return round(random.gauss(550, 120), 1)  # co2 (ppm)


def zikindu(balioa):
    """Tarteka balio okerra itzultzen du: testua, nulua, balio ezinezkoa edo 'N/A'."""
    if random.random() >= ZIKINKERIA_PROBABILITATEA:
        return balioa
    return random.choice([str(balioa), None, -999, "N/A"])


def sortu_irakurketa(sentsorea):
    sentsore_id, mota, unitatea, zona, lat, lon = sentsorea
    return {
        "sentsore_id": sentsore_id,
        "mota": mota,
        "balioa": zikindu(balio_normala(mota)),
        "unitatea": unitatea,
        "zona": zona,
        "kokapena": {"lat": lat, "lon": lon},
        "denbora": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }


@app.route("/api/sentsoreak")
def sentsoreak():
    return jsonify({"sentsoreak": [sortu_irakurketa(s) for s in SENTSOREAK]})


@app.route("/osasuna")
def osasuna():
    if random.random() < 0.10:
        return jsonify({"egoera": "behera"}), 503
    return jsonify({"egoera": "ondo"})


@app.route("/api/akatsa")
def akatsa():
    return jsonify({"akatsa": "barne-errorea"}), 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
