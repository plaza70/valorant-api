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

    # Rango y RR actual
    rank_url = f"{KYROS}/mmr/{region}/{name}/{tag}?show=combo&display=0"

    try:
        rank_response = requests.get(rank_url, timeout=30)
    except requests.RequestException:
        return "No se pudo conectar con la API de Valorant", 503

    if rank_response.status_code != 200:
        return "No se ha encontrado la cuenta", 404

    rango_texto = rank_response.text.strip()

    # Último cambio de RR
    change_url = f"{KYROS}/mmrchange/{region}/{name}/{tag}?display=0"

    try:
        change_response = requests.get(change_url, timeout=30)
    except requests.RequestException:
        return rango_texto

    if change_response.status_code != 200:
        return rango_texto

    cambio_texto = change_response.text.strip()

    # Detectar cambio de RR
    match = re.search(r'([+-]\d+)\s*RR', cambio_texto, re.IGNORECASE)

    if match:
        cambio = int(match.group(1))

        if cambio > 0:
            resultado = f"Victoria (+{cambio} RR)"
        elif cambio < 0:
            resultado = f"Derrota ({cambio} RR)"
        else:
            resultado = "Sin cambio de RR"
    else:
        resultado = "Última partida no disponible"

    return f"{rango_texto} • Última: {resultado}"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
