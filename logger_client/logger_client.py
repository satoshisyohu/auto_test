from logging import getLogger, StreamHandler, INFO, Formatter


def get_logger():
    logger = getLogger("log")
    handler = StreamHandler()
    handler.setLevel(INFO)
    logger.setLevel(INFO)
    logger.addHandler(handler)

    formatter = Formatter('[%(levelname)s]%(asctime)s-%(message)s(%(filename)s)')
    handler.setFormatter(formatter)
    return logger
#
#
# if __name__ == "__main__":
#     main()
