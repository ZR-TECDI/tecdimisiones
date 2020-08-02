import json
import os
from lib import ftper
from . import logger


def check_cache():
    logger.log("Comprobando existencia de caché de misiones...")
    if not os.path.isfile("public/mision_cache.json"):
        logger.log("No existe el caché!")
        return False
    logger.log("Caché encontrado.")
    return True


def create_cache():
    logger.log("Intentando crear caché de misiones...")

    misiones = ftper.obtener_lista()
    with open("public/mision_cache.json", "w", encoding="UTF-8") as f:
        json.dump(jsonizar_misiones(misiones), f, indent=4)


def jsonizar_misiones(misiones: list):
    mision_dct = {
        "misiones": []
    }

    for m in misiones:
        mision = m.split()

        if not mision[3].lower().endswith(".pbo"):
            continue

        archivo = mision[3].split(".")
        fecha = f"{mision[0]} {mision[1]}"
        nombre = humanizar_nombre(archivo[0])
        isla = archivo[1]
        archivo = mision[3]

        mision_dct["misiones"].append([nombre, isla, fecha, archivo])

    return mision_dct


def humanizar_nombre(nombre: str):
    html_tokens = {
        "%20": " ",
        "%22": "\"",
        "%2C": ",",
        "%2E": ".",
        "%3F": "?",
        "%40": "@"
    }

    for key in html_tokens.keys():
        if key in nombre:
            nombre = nombre.replace(key, html_tokens[key])

    return nombre


def get_cache():
    if not check_cache():
        create_cache()

    with open("public/mision_cache.json", "r", encoding="UTF-8") as f:
        cache = json.load(f)

    return cache
