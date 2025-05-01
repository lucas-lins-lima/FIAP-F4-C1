import logging
import os
from datetime import datetime

class ColorFormatter(logging.Formatter):
    LEVEL_COLORS = {
        logging.DEBUG: "\033[34m",
        logging.INFO: "\033[32m",
        logging.WARNING: "\033[33m",
        logging.ERROR: "\033[31m",
        logging.CRITICAL: "\033[35m"
    }
    RESET_COLOR = "\033[0m"

    def format(self, record):
        color = self.LEVEL_COLORS.get(record.levelno, self.RESET_COLOR)
        levelname_colored = f"{color}{record.levelname}{self.RESET_COLOR}"
        record.levelname = levelname_colored
        return super().format(record)

class Logger:
    def __init__(self, name=None, file_name: str = "app.log", level: int = logging.DEBUG):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        if not self.logger.handlers:
            format_string = '[%(levelname)s] %(asctime)s %(filename)s: %(message)s'
            date_format = "%Y-%m-%d %H:%M:%S"

            console_handler = logging.StreamHandler()
            console_handler.setLevel(level)
            console_handler.setFormatter(ColorFormatter(format_string, datefmt=date_format))
            self.logger.addHandler(console_handler)

            if not file_name:
                now = datetime.now().strftime("%Y-%m-%d")
                os.makedirs("logs", exist_ok=True)
                file_name = f"logs/{now}.log"

            file_handler = logging.FileHandler(file_name, encoding="utf-8")
            file_handler.setLevel(level)
            file_handler.setFormatter(logging.Formatter(format_string, datefmt=date_format))
            self.logger.addHandler(file_handler)

    def __call__(self):
        return self.logger
