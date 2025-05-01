import logging
from datetime import datetime
import os


class ColorFormatter(logging.Formatter):
    # Mapear níveis de log para cores ANSI
    LEVEL_COLORS = {
        logging.DEBUG: "\033[34m",    # Azul
        logging.INFO: "\033[32m",     # Verde
        logging.WARNING: "\033[33m",  # Amarelo
        logging.ERROR: "\033[31m",    # Vermelho
        logging.CRITICAL: "\033[35m"  # Magenta
    }
    RESET_COLOR = "\033[0m"  # Resetar cor

    def format(self, record):
        color = self.LEVEL_COLORS.get(record.levelno, self.RESET_COLOR)
        levelname_colored = f"{color}{record.levelname}{self.RESET_COLOR}"
        record.levelname = levelname_colored
        return super().format(record)


def config_logger(file_name: str = 'app.log', level: int = logging.DEBUG):
    logger = logging.getLogger()

    if logger.handlers:
        return

    logger.setLevel(level)

    if not file_name:
        now = datetime.now().strftime("%Y-%m-%d")
        file_name = f"logs/{now}.log"

        os.makedirs("logs", exist_ok=True)

    format_string = '[%(levelname)s] %(asctime)s %(filename)s: %(message)s'
    formatter = logging.Formatter(format_string, datefmt="%Y-%m-%d %H:%M:%S")

    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(ColorFormatter(format_string))
    logger.addHandler(console_handler)

    file_handler = logging.FileHandler(file_name, encoding='utf-8')
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
