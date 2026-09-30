"""Задание 4. Функциональная обработка логов авторизации."""
from collections import Counter
from functools import reduce
from itertools import groupby
from operator import itemgetter
from typing import Any, Callable

KEYS = ("user", "action", "status", "timestamp")
RAW = [
    ("aigerim", "login", "success", "2026-09-01T08:12:00"),
    ("damir", "login", "fail", "2026-09-01T08:13:20"),
    ("damir", "login", "fail", "2026-09-01T08:13:45"),
    ("damir", "login", "success", "2026-09-01T08:14:10"),
    ("samir", "login", "success", "2026-09-01T08:20:05"),
    ("aigerim", "logout", "success", "2026-09-01T09:02:31"),
    ("arman", "login", "fail", "2026-09-01T09:15:00"),
    ("arman", "login", "fail", "2026-09-01T09:15:40"),
    ("arman", "login", "fail", "2026-09-01T09:16:12"),
    ("arman", "login", "success", "2026-09-01T09:17:03"),
    ("dana", "login", "success", "2026-09-01T10:01:00"),
    ("samir", "logout", "success", "2026-09-01T10:30:44"),
    ("damir", "logout", "success", "2026-09-01T11:05:19"),
    ("aigerim", "login", "fail", "2026-09-01T12:40:00"),
    ("aigerim", "login", "success", "2026-09-01T12:40:30"),
    ("dana", "logout", "success", "2026-09-01T13:00:00"),
    ("arman", "logout", "success", "2026-09-01T14:22:10"),
    ("samir", "login", "fail", "2026-09-01T15:05:00"),
    ("samir", "login", "success", "2026-09-01T15:05:25"),
    ("aigerim", "logout", "success", "2026-09-01T18:00:00"),
]
# Список словарей вида {"user": ..., "action": ..., "status": ..., ...}
logs: list[dict] = [dict(zip(KEYS, row)) for row in RAW]


def failed_attempts(data: list[dict]) -> list[dict]:
    """Записи с неуспешной попыткой входа."""
    return list(filter(lambda r: r["action"] == "login"
                       and r["status"] == "fail", data))


def count_by_user(data: list[dict]) -> dict[str, int]:
    """Количество записей по каждому пользователю (itertools.groupby)."""
    by_user = sorted(data, key=itemgetter("user"))
    return {user: len(list(grp))
            for user, grp in groupby(by_user, key=itemgetter("user"))}


def count_by_user_reduce(data: list[dict]) -> dict[str, int]:
    """То же самое через functools.reduce с накоплением в словарь."""
    return reduce(lambda acc, r: {**acc, r["user"]: acc.get(r["user"], 0) + 1},
                  data, {})


def unique_users(data: list[dict]) -> list[str]:
    """Отсортированный список уникальных пользователей."""
    return sorted({r["user"] for r in data})


def run_pipeline(data: Any, *steps: Callable) -> Any:
    """Последовательно применяет шаги-трансформации к данным."""
    return reduce(lambda acc, step: step(acc), steps, data)


def top_n(n: int) -> Callable[[list[dict]], list[tuple[str, int]]]:
    """Возвращает шаг пайплайна: топ-n пользователей по числу записей."""
    return lambda data: Counter(map(itemgetter("user"), data)).most_common(n)


if __name__ == "__main__":
    print(f"Всего записей: {len(logs)}, "
          f"пользователей: {len(unique_users(logs))}")

    print("\n1) Неуспешные попытки входа:")
    print(*map(lambda r: f"   {r['timestamp']}  {r['user']}",
               failed_attempts(logs)), sep="\n")

    print("\n2) Неуспешных попыток по пользователям:")
    print("   groupby:", count_by_user(failed_attempts(logs)))
    print("   reduce: ", count_by_user_reduce(failed_attempts(logs)))

    print("\n3) Уникальные пользователи:", unique_users(logs))

    print("\n4) Пайплайн: неуспешные входы -> счёт -> сортировка по убыванию")
    fail_rating = run_pipeline(
        logs,
        failed_attempts,
        count_by_user,
        lambda d: sorted(d.items(), key=itemgetter(1), reverse=True),
    )
    print("  ", fail_rating)

    print("\n5) Топ-3 самых активных пользователей:")
    top3 = run_pipeline(logs, top_n(3))
    print("  ", top3)
    print(*map(lambda p: f"   {p[0]}. {p[1][0]:<8} — записей: {p[1][1]}",
               enumerate(top3, 1)), sep="\n")
