import functools
import logging


def log(filename=None):
    """
    Декоратор для логирования начала и окончания выполнения функции, а также её результата.

    """
    logger = logging.getLogger("log_decorator")
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter("%(levelname)s %(funcName)s: %(message)s")

    if filename:
        handler = logging.FileHandler(filename, encoding="utf-8")
    else:
        handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    if logger.hasHandlers():
        logger.handlers.clear()
    logger.addHandler(handler)

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logger.info(f"Начало выполнения функции")
            try:
                result = func(*args, **kwargs)
                logger.info(f"Функция успешно выполнена. Результат: {result}")
                return result
            except Exception as e:
                args_repr = ", ".join(repr(a) for a in args)
                kwargs_repr = ", ".join(f"{k}={v!r}" for k, v in kwargs.items())
                params = ", ".join(filter(None, [args_repr, kwargs_repr]))
                logger.error(f"Ошибка: {type(e).__name__}. Входные параметры: {params}")
                raise
            finally:
                for h in logger.handlers:
                    h.flush()

        return wrapper

    return decorator
