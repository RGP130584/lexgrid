import logging
from scripts.shared.logger import get_logger

def test_get_logger_level():
    logger = get_logger("test_logger")
    assert isinstance(logger, logging.Logger)
    assert logger.level == logging.INFO