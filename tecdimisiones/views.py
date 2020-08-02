from . import app, logger
from . import cache_misiones
from . import local
from .operar_pbo import eliminar_pbo, subir_pbo
from lib.gif import random_gif
from flask import render_template, request, redirect, url_for
from flask_simplelogin import login_required
from urllib.parse import quote
from .cond_decorator import conditional_decorator


@app.route('/')
@conditional_decorator(login_required, not local)
def lista_misiones():
    cache = cache_misiones.get_cache()["misiones"]

    return render_template("lista_misiones.html", cache=cache)


@app.route('/regenerar')
@conditional_decorator(login_required, not local)
def regenerar_listado():
    logger.log("Usuarios solicitó regenerar el caché de misiones!")
    cache_misiones.create_cache()

    return redirect(url_for("lista_misiones"))


@app.route('/subirmision', methods=['GET', 'POST'])
@conditional_decorator(login_required, not local)
def subir_mision():
    if request.method == "POST":
        mision = request.files["mision"]
        logger.log(f" intentan subir archivo: {mision}")

        resultado = subir_pbo(mision)

        if resultado is None:
            return redirect(url_for("exito"))
        else:
            error_msg = f"Error intentando subir archivo {mision.filename}.\n{resultado}"
            return redirect(url_for("error", error_msg=error_msg, **request.args))

    else:
        return render_template("subir_mision.html")


@app.route('/montar')
@conditional_decorator(login_required, not local)
def montar():
    return redirect(
        url_for("error", error_msg="característica en desarrollo.\n\nTodo bien, nomás no he terminado esto."))


@app.route('/borrar')
@conditional_decorator(login_required, not local)
def borrar():
    archivo = quote(request.args.get("archivo", type=str))
    resultado = eliminar_pbo(archivo)

    if resultado is None:
        return redirect(url_for("exito"))
    else:
        error_msg = f"Error tratando de eliminar {archivo}\n\n {str(resultado)}"
        return redirect(url_for("error", error_msg=error_msg))


@app.route('/exito')
@conditional_decorator(login_required, not local)
def exito():
    gif = random_gif("success")
    return render_template("exito.html", gif=gif)


@app.route('/error')
@conditional_decorator(login_required, not local)
def error():
    gif = random_gif()
    return render_template("error.html", gif=gif, error_msg=request.args.get("error_msg"))
