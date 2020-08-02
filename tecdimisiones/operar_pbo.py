from . import logger
from lib.ftper import eliminar_archivo, enviar_archivo, all_errors
from . import cache_misiones
from os import path


def subir_pbo(mision):
    nombre = mision.filename

    if validar_pbo(nombre):
        mision.save(mision.save(path.join('public', nombre)))

        try:
            with open(path.join('public', mision.filename), "rb") as binario:
                enviar_archivo(mision.filename, binario)
        except Exception as e:
            return str(e)
        else:
            cache_misiones.create_cache()
            return None
    else:
        logger.log(f"Intentaron subir un PBO inválido, archivo: {nombre}")
        return f"{nombre} es un archivo inválido!\n Debiése estar en formato PBO y tener este formato: nombre.isla.pbo"


def eliminar_pbo(filename: str):
    with open("tecdimisiones/protegidas.txt", encoding="UTF-8") as f:
        protegidas = f.readlines()

    for p in protegidas:
        if p.strip() in filename:
            return f"{filename} es una misión protegida y no se puede eliminar por este medio."

    resultado = eliminar_archivo(filename)

    if resultado is None:
        cache_misiones.create_cache()
        return None
    else:
        return resultado


def validar_pbo(filename: str):
    nombre = filename.lower()

    if not nombre.endswith(".pbo"):
        return False

    if "." not in nombre:
        return False

    formato = nombre.split(".")
    if len(formato) != 3:
        return False

    logger.log(f"{filename} es un PBO válido")
    return True





