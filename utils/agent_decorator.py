import time
from functools import wraps
from utils.logger import logger


def agent(name):

    def decorator(func):

        @wraps(func)
        def wrapper(state):

            logger.info(f"[AGENT START] {name}")

            start = time.time()

            result = func(state)

            end = time.time()

            logger.info(f"[AGENT END] {name} ({end-start:.2f}s)")

            return result

        return wrapper

    return decorator