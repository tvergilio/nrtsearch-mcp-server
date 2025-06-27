import logging
from .settings import Settings

_logger_initialized = False

def setup_logging(settings: Settings):
    global _logger_initialized
    if _logger_initialized:
        return
    logger = logging.getLogger("nrtsearch.mcp")
    if not logger.hasHandlers():
        handler = logging.StreamHandler()
        formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    logger.setLevel(getattr(logging, settings.log_level.upper(), logging.INFO))
    _logger_initialized = True
