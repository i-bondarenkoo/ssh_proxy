import time
from app.core.logging import logger


def timer(func):
    async def wrapper(*args, **kwargs):
        start = time.time()
        result = await func(*args, **kwargs)
        stop = time.time()
        logger.info(f"Время выполнения запроса - {stop - start} секунд")
        return result

    return wrapper
