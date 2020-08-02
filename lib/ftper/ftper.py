from ftplib import FTP, all_errors
from os import environ, path
from tecdimisiones import logger

ftp = FTP()
host = environ["HOST"]
port = int(environ["PORT"])
user = environ["USER"]
pswd = environ["PASS"]
ftp_dir = environ["FTP_DIR"]


def conectar_logear():
    logger.log("Intentando conectar a servidor FTP...")
    try:
        ftp.connect(host=host, port=port, timeout=20)
        ftp.login(user=user, passwd=pswd)
        ftp.cwd(ftp_dir)
    except all_errors as err:
        logger.log(f"ERROR AL CONECTAR AL FTP: {err}")
    else:
        if '220' in ftp.getwelcome():
            logger.log("Conexión FTP exitosa")
        else:
            logger.log(f"Respuesta FTP: {ftp.getwelcome()}")


def cerrar_conexion():
    logger.log("Cerrando conexión FTP")
    ftp.close()


def obtener_lista():
    conectar_logear()
    archivos = []
    logger.log("Obteniendo lista de archivos FTP")
    ftp.dir(archivos.append)

    cerrar_conexion()

    return archivos


def enviar_archivo(archivo_nombre, archivo_binario):
    conectar_logear()
    logger.log(f"Intentando enviar archivo de nombre {archivo_nombre}")

    try:
        ftp.storbinary(f"STOR {archivo_nombre}", archivo_binario)
    except all_errors as e:
        logger.log(str(e))
        cerrar_conexion()
        return False, e
    else:
        logger.log(f"archivo {archivo_nombre} subido!")
        cerrar_conexion()
        return True, None


def eliminar_archivo(archivo_nombre):
    conectar_logear()
    logger.log(f"Intentando eliminar archivo de nombre {archivo_nombre}")

    try:
        ftp.delete(path.join(ftp_dir, archivo_nombre))
    except all_errors as err:
        logger.log(str(err))
        cerrar_conexion()
        return str(err)
    else:
        cerrar_conexion()
        return None

