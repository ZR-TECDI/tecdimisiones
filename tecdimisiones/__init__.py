from flask import Flask
from flask_simplelogin import SimpleLogin
from lib import mulalogger as ml
import os

__version__ = '0.2.0'

local = True
app = Flask(__name__)

messages = {
    'login_success': 'Autentificado con éxito',
    'login_failure': 'Fallo en la autentificación. ¡Contacta a Riquelme!',
    'is_logged_in': 'Tiene permisos de tecdi',
    'logout': 'Desconectar',
    'login_required': 'Se requiere autentificación para ganar permisos de TECDI',
    'access_denied': 'Acceso denegado',
    'auth_error': 'Fallo en la autentificación： {0}'
}

SimpleLogin(app, messages=messages)
PUBLIC_DIR = os.path.join(os.path.curdir, 'public')
logger = ml.instance(PUBLIC_DIR, 'registro.log')


def check_envs():
    if local:
        try:
            logger.log("Entorno local de desarrollo detectado")
            logger.log("Leyendo variables de entornos, si existe archivo .env")
            with open('.env', "r", encoding="UTF-8") as f:
                for line in f.readlines():
                    var, value = line.strip().split("=")
                    os.environ[var] = value

        except Exception as error:
            logger.log("No se pudo leer variables locales")
            logger.log(str(error))
    else:
        logger.log("Entorno de producción detectado. No se leerá archivo con envs.")

    for env in ["HOST", "PORT", "USER", "PASS", "FTP_DIR", "SIMPLELOGIN_USERNAME", "SIMPLELOGIN_PASSWORD"]:
        try:
            _env = os.environ[env]
        except KeyError:
            logger.log(f"{env} es una variable de entorno requerida y no fue seteada")


def init():
    check_envs()
    # Import tardío para modicar objeto en curso y esperar dependencias
    from . import views
    from . import cache_misiones


# Inicialización
init()


