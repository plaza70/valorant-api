from flask import Flask, jsonify, request
import requests
import os

app = Flask(__name__)

API = "https://api.henrikdev.xyz/valorant"

@app.route("/")
def home():
    return "Valorant API funcionando"

@app.route("/rango")
def rango():
    name = request.args.get("name")
    tag = request.args.get("tag")
    region = request.args.get("region", "eu")

    if not name or not tag:
        return "Falta el Riot ID", 400

    # Rango actual
    mmr_url = f"{API}/v3/mmr/{region}/{name}/{tag}"
    mmr_response = requests.get(mmr_url)

    if mmr_response.status_code != 200:
        return "No se ha encontrado la cuenta", 404

    mmr = mmr_response.json()["data"]

    rango_actual = mmr["currenttierpatched"]
    rr_actual = mmr["ranking_in_tier"]

    # Historial MMR
    history_url = f"{API}/v3/mmr-history/{region}/{name}/{tag}"
    history_response = requests.get(history_url)

    if history_response.status_code != 200:
        return f"{rango_actual} • {rr_actual} RR • No se pudo consultar la última partida"

    history = history_response.json()["data"]

    if not history:
        return f"{rango_actual} • {rr_actual} RR"

    ultima = history[0]
    cambio = ultima.get("last_change", 0)

    if cambio > 0:
        resultado = f"Victoria (+{cambio} RR)"
    elif cambio < 0:
        resultado = f"Derrota ({cambio} RR)"
    else:
        resultado = "Sin cambio de RR"

    return f"{rango_actual} • {rr_actual} RR • Última: {resultado}"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
