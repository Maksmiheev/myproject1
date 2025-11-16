import functools
import sys
import traceback

def log(filename=None):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            output = sys.stdout if filename is None else open(filename, 'a', encoding='utf-8')
            try:
                print(f"Начало выполнения функции: {func.__name__}", file=output)
                result = func(*args, **kwargs)
                print(f"Функция {func.__name__} успешно выполнена. Результат: {result}", file=output)
                return result
            except Exception as e:
                args_repr = ", ".join(repr(a) for a in args)
                kwargs_repr = ", ".join(f"{k}={v!r}" for k, v in kwargs.items())
                params = ", ".join(filter(None, [args_repr, kwargs_repr]))
                print(f"Ошибка в функции {func.__name__}: {type(e).__name__}. Входные параметры: {params}", file=output)
                print(f"Трассировка ошибки:\n{traceback.format_exc()}", file=output)
                raise
            finally:
                if filename is not None:
                    output.close()
                else:
                    output.flush()
                if filename is None:
                    print(f"Конец выполнения функции: {func.__name__}")
        return wrapper
    return decorator