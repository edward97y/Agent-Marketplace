import logging
import sys

def get_logger(name: str):
    logger = logging.getLogger(name)

    if not logger.handlers:  # prevent duplicate handlers
        logger.setLevel(logging.INFO)

        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )

        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger