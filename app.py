from flask import Flask, request
import requests
import os
import re

app = Flask(__name__)

KYROS = "https://api.kyroskoh.xyz/valorant/v1"


@app.route("/")
def home():
    return "Valorant API funcionando"

@app.route("/rango")
def rango():
    name = request.args.get("name")
    tag = request.args.get("tag")
    region = request.args.get("region", "eu")

    if not name or not tag:
        return "Faltan name y tag", 400

    rank_url = f"{KYROS}/mmr/{region}/{name}/{tag}?show=combo&display=0"

    try:
        response = requests.get(rank_url, timeout=10)
        response.raise_for_status()
        return response.text.strip()
    except requests.RequestException as e:
        return f"Error conectando con Kyros: {e}", 502

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
