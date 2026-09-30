"""Задание 1. Обработка числовых и текстовых массивов без циклов."""

scores: list[int] = [78, 45, 92, 60, 33, 85, 71, 50, 98, 27,
                     64, 88, 55, 40, 73, 81, 69, 95]

names: list[str] = [
    "Момбеков Самир Ерланович", "Ахметова Айгерим Нурлановна",
    "Жумабаев Дамир Асланович", "Ли Ан", "Сериков Арман Болатович",
    "Ким Ир", "Абдрахманова Дана Маратовна", "Оспанов Ержан Кайратович",
]

PASS_MARK = 50


def to_letter(score: int) -> str:
    """Переводит балл (0-100) в буквенную оценку A/B/C/D/F."""
    return ("A" if score >= 90 else "B" if score >= 75 else
            "C" if score >= 60 else "D" if score >= 50 else "F")


def short_name(full_name: str) -> str:
    """Приводит полное имя к формату «Фамилия И.»."""
    parts = full_name.split()
    return f"{parts[0]} {parts[1][0]}." if len(parts) > 1 else parts[0]


print("Исходные баллы:", scores)

# (а) map() / filter() / lambda
passed_a = list(filter(lambda s: s >= PASS_MARK, scores))
letters_a = list(map(to_letter, passed_a))
print("\n(а) map/filter/lambda")
print("  Зачтённые баллы:", passed_a)
print("  Буквенные оценки:", letters_a)

# (б) генераторы списков
passed_b = [s for s in scores if s >= PASS_MARK]
letters_b = [to_letter(s) for s in passed_b]
print("\n(б) генераторы списков")
print("  Зачтённые баллы:", passed_b)
print("  Буквенные оценки:", letters_b)
print("  Результаты совпадают:",
      passed_a == passed_b and letters_a == letters_b)

# Сравнение читаемости:
# генератор списков читается как обычная фраза «s для s в scores, если
# s >= 50» и не требует lambda и обёртки list(); вариант map/filter удобен,
# когда функция-преобразователь уже есть (map(to_letter, ...)), но
# с lambda получается длиннее и менее наглядно.

print("\nИсходные имена:", names)
short = list(map(short_name, names))
print("Формат «Фамилия И.»:", short)
long_enough = list(filter(lambda n: len(n.split()[0]) >= 3, short))
print("Без фамилий короче 3 символов:", long_enough)
result = sorted(long_enough, key=lambda n: n.lower())
print("Отсортировано по алфавиту:", result)
