import logging


class Logger(object):
    def __new__(
        self,
        name: str,
    ):
        logger = logging.getLogger(name)
        logger.setLevel(10)
        # overwrite handlers if they already exist
        if logger.handlers:  # pragma: no cover
            logger.handlers.clear()
        c_handler = logging.StreamHandler()
        c_handler.setLevel(10)
        c_format = logging.Formatter(
            "%(asctime)-30s %(funcName)-40s %(levelname)-10s %(message)s"
        )
        c_handler.setFormatter(c_format)

        logger.addHandler(c_handler)

        return logger
