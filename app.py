from flask import Flask, request
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
        return "Faltan name y tag", 400

    headers = {
        "Authorization": os.environ.get("HENRIK_API_KEY", "")
    }

    url = f"{API}/v3/mmr/{region}/pc/{name}/{tag}"

    try:
        response = requests.get(url, headers=headers, timeout=15)
    except requests.RequestException:
        return "Error conectando con HenrikDev", 502

    if response.status_code != 200:
        return f"Error de HenrikDev: {response.status_code}", response.status_code

    data = response.json()["data"]

    rango_actual = data["current"]["tier"]["name"]
    rr_actual = data["current"]["rr"]
    cambio = data["current"]["last_change"]

    if cambio > 0:
        resultado = f"Victoria (+{cambio} RR)"
    elif cambio < 0:
        resultado = f"Derrota ({cambio} RR)"
    else:
        resultado = "Sin cambio de RR"

    return f"{rango_actual} - {rr_actual} RR • Última: {resultado}"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
