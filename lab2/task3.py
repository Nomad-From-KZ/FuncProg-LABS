"""Задание 3. Декораторы на основе замыканий."""
import time
from functools import wraps
from typing import Callable


def log_calls(func: Callable) -> Callable:
    """Логирует имя функции, аргументы, результат и время выполнения."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = (time.perf_counter() - start) * 1000
        print(f"[LOG] {func.__name__}(args={args}, kwargs={kwargs}) "
              f"-> {result!r} за {elapsed:.3f} мс")
        return result
    return wrapper


def _type_name(tp: type | tuple) -> str:
    """Человекочитаемое имя типа или кортежа типов."""
    return (" или ".join(map(_type_name, tp)) if isinstance(tp, tuple)
            else tp.__name__)


def validate_types(**expected_types: type) -> Callable:
    """Фабрика декораторов: проверяет типы аргументов по именам."""
    def decorator(func: Callable) -> Callable:
        names = func.__code__.co_varnames[:func.__code__.co_argcount]

        @wraps(func)
        def wrapper(*args, **kwargs):
            bound = {**dict(zip(names, args)), **kwargs}
            for name, tp in expected_types.items():
                if name in bound and not isinstance(bound[name], tp):
                    raise TypeError(
                        f"{func.__name__}(): аргумент '{name}' должен быть "
                        f"{_type_name(tp)}, получен "
                        f"{type(bound[name]).__name__} ({bound[name]!r})")
            return func(*args, **kwargs)
        return wrapper
    return decorator


def memoize(func: Callable) -> Callable:
    """Собственная мемоизация: кеш хранится в замыкании."""
    cache: dict = {}

    @wraps(func)
    def wrapper(*args, **kwargs):
        key = (args, tuple(sorted(kwargs.items())))
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]
    wrapper.cache = cache
    return wrapper


@log_calls
@validate_types(price=(int, float), percent=int)
def apply_discount(price: float, percent: int = 10) -> float:
    """Возвращает цену со скидкой."""
    return round(price * (100 - percent) / 100, 2)


@memoize
def power(base: int, exp: int = 2) -> int:
    """Медленное возведение в степень (имитация тяжёлых вычислений)."""
    time.sleep(0.2)
    return base ** exp


@memoize
def fib(n: int) -> int:
    """n-е число Фибоначчи."""
    return n if n < 2 else fib(n - 1) + fib(n - 2)


if __name__ == "__main__":
    print("=== @log_calls + @validate_types ===")
    apply_discount(1500, 20)
    apply_discount(price=99.9, percent=5)
    apply_discount(250)
    try:
        apply_discount("1000", 15)
    except TypeError as e:
        print("Перехвачена ошибка TypeError:", e)
    print("Имя функции сохранено wraps:", apply_discount.__name__)

    print("\n=== @memoize ===")
    for args, kwargs in [((3,), {"exp": 4}), ((3,), {"exp": 4}),
                         ((5,), {}), ((5,), {})]:
        t = time.perf_counter()
        r = power(*args, **kwargs)
        ms = (time.perf_counter() - t) * 1000
        print(f"power(*{args}, **{kwargs}) = {r:<3} за {ms:6.1f} мс")
    t = time.perf_counter()
    print(f"fib(80) = {fib(80)} за {(time.perf_counter() - t) * 1000:.2f} мс,"
          f" записей в кеше: {len(fib.cache)}")
