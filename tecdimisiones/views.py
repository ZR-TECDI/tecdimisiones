from . import app, logger
from . import cache_misiones
from .operar_pbo import validar_pbo
from lib.gif import random_gif
from flask import render_template, request, redirect, url_for
from flask_simplelogin import login_required
from lib.ftper import eliminar_archivo, enviar_archivo
from urllib.parse import unquote, quote
from os import path


@app.route('/')
# @login_required()
def lista_misiones():
    cache = cache_misiones.get_cache()["misiones"]

    return render_template("lista_misiones.html", cache=cache)


@app.route('/subirmision', methods=['GET', 'POST'])
# @login_required()
def subir_mision():
    if request.method == "POST":
        mision = request.files["mision"]
        logger.log(f" intentan subir archivo: {mision}")

        if validar_pbo(mision.filename):
            mision.save(path.join('public', mision.filename))

            with open(path.join('public', mision.filename), "rb") as binario:
                resultado = enviar_archivo(mision.filename, binario)

            if resultado[0]:
                cache_misiones.create_cache()
                return redirect(url_for("exito"))
            else:
                error_msg = f"Error intentando subir archivo {mision.filename}.\n{resultado[1]}"
                return redirect(url_for("error", error_msg=error_msg, **request.args))

        else:
            logger.log("Archivo inválido!")
            error_msg = f"Error intentando subir archivo {mision.filename}.\nArchivo inválido."

            return redirect(url_for("error", error_msg=error_msg, **request.args))
    else:
        return render_template("subir_mision.html")


@app.route('/montar')
# @login_required()
def montar():
    return redirect(
        url_for("error", error_msg="característica en desarrollo.\n\nTodo bien, nomás no he terminado esto."))


@app.route('/borrar')
# @login_required()
def borrar():
    archivo = quote(request.args.get("archivo", type=str))
    resultado = eliminar_archivo(archivo)

    if resultado is None:
        cache_misiones.create_cache()
        return redirect(url_for("exito"))
    else:
        error_msg = f"Error tratando de eliminar {archivo}\n\n {str(resultado)}"
        return redirect(url_for("error", error_msg=error_msg))


@app.route('/exito')
# @login_required()
def exito():
    gif = random_gif("success")
    return render_template("exito.html", gif=gif)


@app.route('/error')
# @login_required()
def error():
    gif = random_gif()
    return render_template("error.html", gif=gif, error_msg=request.args.get("error_msg"))
