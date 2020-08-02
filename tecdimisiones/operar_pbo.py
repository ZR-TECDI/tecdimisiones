from . import logger


def validar_pbo(filename: str):
    logger.log(f"Intentando validar archivo: {filename}")
    if "." not in filename:
        logger.log(f"{filename} no es un PBO válido")
        return False

    try:
        ext = (filename.split("."))[2]
    except:
        ext = "ERROR"
        logger.log(f"{filename} no es un PBO válido")
        return False

    if ext.upper() not in ["PBO"]:
        logger.log(f"{filename} no es un PBO válido")
        return False

    logger.log(f"{filename} es un PBO válido")

    return True
