"""Single logger factory — configured once from settings."""
from __future__ import annotations

import logging
from functools import lru_cache

from config.settings import settings


@lru_cache(maxsize=None)
def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(
            logging.Formatter(
                fmt="%(asctime)s %(levelname)s %(name)s %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
        )
        logger.addHandler(handler)
        logger.setLevel(settings.log_level)
        logger.propagate = False
    return logger
