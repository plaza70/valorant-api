from flask import Flask, jsonify
import requests
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "Valorant API funcionando"

@app.route("/rango/<region>/<name>/<tag>")
def rango(region, name, tag):
    url = f"https://api.henrikdev.xyz/valorant/v3/mmr/{region}/{name}/{tag}"

    response = requests.get(url)

    if response.status_code != 200:
        return jsonify({"error": "No se pudo obtener la información"}), 404

    data = response.json()

    return jsonify(data)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
