from tecdimisiones import app, logger


if __name__ == "__main__":
    try:
        app.run(host="0.0.0.0", debug=True, port="8000")
    except Exception as e:
        logger.log(str(e))
        raise e
