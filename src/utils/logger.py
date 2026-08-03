"""
Configuração de logging para o Zion Hotel AI Developer.
"""

import logging
import sys
from rich.logging import RichHandler

from src.config import LOG_LEVEL


def setup_logger(name: str = "zion") -> logging.Logger:
    """
    Configura e retorna um logger com Rich handler.

    Args:
        name: Nome do logger

    Returns:
        Logger configurado
    """
    logger = logging.getLogger(name)

    if not logger.handlers:
        logger.setLevel(getattr(logging, LOG_LEVEL, logging.INFO))

        rich_handler = RichHandler(
            level=getattr(logging, LOG_LEVEL, logging.INFO),
            rich_tracebacks=True,
            markup=True,
            show_time=True,
            show_path=False,
        )
        rich_handler.setFormatter(
            logging.Formatter("%(message)s", datefmt="[%X]")
        )

        logger.addHandler(rich_handler)

    return logger
