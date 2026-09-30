"""Задание 2. Чистые функции, reduce() и функции высшего порядка."""
from functools import reduce
from typing import Any, Callable


def mean(values: list[float]) -> float:
    """Среднее арифметическое списка чисел."""
    if not values:
        raise ValueError("mean() от пустого списка")
    return reduce(lambda acc, x: acc + x, values, 0) / len(values)


def variance(values: list[float]) -> float:
    """Дисперсия (генеральная) списка чисел."""
    m = mean(values)
    return reduce(lambda acc, x: acc + (x - m) ** 2, values, 0) / len(values)


def median(values: list[float]) -> float:
    """Медиана списка чисел (исходный список не изменяется)."""
    if not values:
        raise ValueError("median() от пустого списка")
    s = sorted(values)
    mid = len(s) // 2
    return s[mid] if len(s) % 2 else (s[mid - 1] + s[mid]) / 2


def compose(*funcs: Callable) -> Callable:
    """compose(f, g, h)(x) == f(g(h(x)))."""
    return reduce(lambda f, g: lambda x: f(g(x)), funcs, lambda x: x)


def pipeline(value: Any, *funcs: Callable) -> Any:
    """Последовательно применяет funcs к value слева направо."""
    return reduce(lambda acc, f: f(acc), funcs, value)


def normalize(values: list[float]) -> list[float]:
    """ЧИСТАЯ: возвращает новый список, приведённый к диапазону [0; 1]."""
    lo, hi = min(values), max(values)
    return [0.0 if hi == lo else (v - lo) / (hi - lo) for v in values]


def normalize_inplace(values: list[float]) -> None:
    """НЕЧИСТАЯ: изменяет переданный список (побочный эффект)."""
    values[:] = normalize(values)


# normalize — чистая: результат зависит только от аргумента, а исходный
# список не меняется. normalize_inplace — нечистая: она ничего не
# возвращает, а мутирует внешний объект, поэтому после вызова меняются
# данные у всех, кто ссылается на этот список.

if __name__ == "__main__":
    data = [4, 8, 15, 16, 23, 42]
    print("Данные:", data)
    print(f"mean = {mean(data):.4f}")
    print(f"variance = {variance(data):.4f}")
    print(f"median = {median(data)}")

    def inc(x): return x + 1
    def dbl(x): return x * 2
    def sqr(x): return x ** 2

    f = compose(inc, dbl, sqr)
    print("\ncompose(inc, dbl, sqr)(3) =", f(3), " # inc(dbl(sqr(3)))")
    print("pipeline(3, inc, dbl, sqr) =", pipeline(3, inc, dbl, sqr),
          " # sqr(dbl(inc(3)))")

    print("\nnormalize(data) =", [round(v, 3) for v in normalize(data)])
    print("data после normalize:", data)
    copy = data.copy()
    normalize_inplace(copy)
    print("copy после normalize_inplace:", [round(v, 3) for v in copy])
