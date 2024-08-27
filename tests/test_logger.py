from veptools.modules.logger import Logger


def foo():
    logger = Logger(name="bar")
    logger.debug("this is debug message")
    logger.info("this is info message")
    logger.error("this is error message")
    logger.critical("this is critical message")


def test_logger(capsys):
    foo()
    captured = capsys.readouterr()
    assert "foo" in captured.err
    assert "DEBUG" in captured.err
    assert "INFO" in captured.err
    assert "ERROR" in captured.err
    assert "CRITICAL" in captured.err
    assert "this is debug message" in captured.err
    assert "this is info message" in captured.err
    assert "this is error message" in captured.err
    assert "this is critical message" in captured.err
