import logging
from functools import wraps
from typing import Any, Callable

from app.exception.image import ImageServiceCustomException


def exception_handler(exception: Callable) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                return func(*args, **kwargs)
            except ImageServiceCustomException as e:
                logging.error(e)
                raise e
            except Exception as e:
                logging.error(e)
                raise exception(str(e))

        return wrapper

    return decorator
