import logging
from app.config.settings import settings

log_level = logging.DEBUG if settings.DEBUG else logging.INFO

def setup_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:  # Prevent duplicate handlers
        logger.setLevel(log_level)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(levelname)-10s[%(name)s]: %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger
