def test_import_logger():
    from scripts.shared.logger import get_logger
    logger = get_logger("test")
    assert logger is not None
    assert logger.name == "test"