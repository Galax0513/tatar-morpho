#!/usr/bin/env python3
"""
cli.py — командная строка для татарского морфоанализатора

Использование:
    python3 src/cli.py                         # интерактивный режим
    python3 src/cli.py китапларда              # анализ одного слова
    python3 src/cli.py --generate китап+N+Pl+Loc  # генерация
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from analyzer import analyze, generate

TAG_NAMES = {
    "N": "сущ.", "V": "гл.",
    "Sg": "ед.ч.", "Pl": "мн.ч.",
    "Nom": "именительный", "Gen": "притяжательный",
    "Dat": "Дательный", "Acc": "винительный",
    "Loc": "местный", "Abl": "исходный",
    "Imp": "повелительное", "Past": "прошедшее",
    "Pres": "настоящее", "Fut": "будущее",
    "Neg": "отрицание",
    "1Sg": "1л.ед.ч.", "2Sg": "2л.ед.ч.", "3Sg": "3л.ед.ч.",
    "1Pl": "1л.мн.ч.", "2Pl": "2л.мн.ч.", "3Pl": "3л.мн.ч.",
}

def format_tags(tags):
    return ", ".join(TAG_NAMES.get(t, t) for t in tags)


def print_analysis(word, results):
    print(f"\n  Слово: {word}")
    print("  " + "─" * 40)
    if not results:
        print("  ✗ Не распознано")
    else:
        for i, r in enumerate(results, 1):
            print(f"  Вариант {i}:")
            print(f"    Лемма: {r['lemma']}")
            print(f"    Теги:  {' + '.join(r['tags'])}")
            print(f"           ({format_tags(r['tags'])})")
    print()


def interactive_mode():
    print("=" * 50)
    print("  Морфологический анализатор татарского языка")
    print("=" * 50)
    print("Введите слово (или 'выход')")
    print()

    while True:
        try:
            line = input(">>> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nВсе")
            break

        if not line:
            continue
        if line.lower() in ("выход", "exit", "quit", "q"):
            print("Все")
            break

        if line.startswith("gen "):
            query = line[4:].strip()
            forms = generate(query)
            if forms:
                print(f"  {query} -> {', '.join(forms)}")
            else:
                print(f"  {query} -> не удалось сгенерировать")
            print()
            continue

        results = analyze(line)
        print_analysis(line, results)


def main():
    args = sys.argv[1:]
    if not args:
        if not sys.stdin.isatty():
            for line in sys.stdin:
                word = line.strip()
                if word:
                    print_analysis(word, analyze(word))
        else:
            interactive_mode()
        return

    if args[0] in ("--generate", "-g") and len(args) > 1:
        forms = generate(args[1])
        if forms:
            print(f"{args[1]} → {', '.join(forms)}")
        else:
            print(f"{args[1]} → не удалось сгенерировать")
        return

    for word in args:
        print_analysis(word, analyze(word))


if __name__ == "__main__":
    main()