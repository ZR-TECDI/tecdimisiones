import os
from datetime import datetime

logger = None


class MulaLogger:
    log_file: str
    log_dir: str

    def __init__(self, log_dir: str, log_file: str):
        self.log_dir = log_dir
        self.log_file = os.path.join(self.log_dir, log_file)

        self.check_log_dir()

    def check_log_dir(self):
        try:
            if not os.path.isdir(self.log_dir):
                os.makedirs(self.log_dir, exist_ok=True)
        except Exception as e:
            print("ERROR: al intentar crear directorio de log!")
            print(str(e))

    def log(self, msg: str):
        log_msg = f"{self.get_timestamp()}\t{msg}\n"
        print(log_msg)

        with open(self.log_file, "a", encoding="UTF-8") as f:
            f.write(log_msg)

    @staticmethod
    def get_timestamp():
        return str(datetime.now())


def instance(log_dir: str = None, log_file: str = None) -> MulaLogger:
    global logger
    if logger is None:
        logger = MulaLogger(log_dir, log_file)
    return logger
