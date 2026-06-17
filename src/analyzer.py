#!/usr/bin/env python3
"""
analyzer.py — функция analyze(word) → список разборов

Граница между Ролью 1 (лингвистическое ядро) и Ролью 2 (приложение).

Формат результата:
    [
        {
            "lemma": "китап",
            "tags":  ["N", "Pl", "Loc"],
            "raw":   "китап+N+Pl+Loc"
        },
        ...
    ]
"""

import json
import os
import sys
from typing import List, Dict

_FST_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "fst")
_JSON_PATH = os.path.join(_FST_DIR, "tatar.json")

_FORMS_CACHE = None


def _load_forms() -> dict:
    """Загрузить словарь форм из JSON. При необходимости — собрать."""
    global _FORMS_CACHE

    if _FORMS_CACHE is not None:
        return _FORMS_CACHE

    if not os.path.exists(_JSON_PATH):
        print("Словарь не найден, запускаем сборку")
        sys.path.insert(0, _FST_DIR)
        from build import build
        build()

    if not os.path.exists(_JSON_PATH):
        raise FileNotFoundError(
            f"Файл не найден: {_JSON_PATH}\n"
            f"Запустите: python3 fst/build.py"
        )

    with open(_JSON_PATH, "r", encoding="utf-8") as f:
        _FORMS_CACHE = json.load(f)

    return _FORMS_CACHE


def analyze(word: str) -> List[Dict]:
    """
    Морфологический анализ слова.
    """
    # Защита от мусора
    if not word or not isinstance(word, str):
        return []

    word = word.strip()
    if not word:
        return []

    word_lower = word.lower()

    forms = _load_forms()

    if word_lower in forms:
        return forms[word_lower]

    return []


def generate(lemma_with_tags: str) -> List[str]:
    if not lemma_with_tags or not isinstance(lemma_with_tags, str):
        return []

    forms = _load_forms()
    results = []

    for surface, entries in forms.items():
        for entry in entries:
            if entry["raw"] == lemma_with_tags:
                if surface not in results:
                    results.append(surface)

    return results

if __name__ == "__main__":
    if len(sys.argv) > 1:
        word = sys.argv[1]
    else:
        word = input("Введите слово: ").strip()

    results = analyze(word)
    if not results:
        print(f"'{word}' — не распознано")
    else:
        for r in results:
            print(f"  лемма: {r['lemma']}")
            print(f"  теги:  {r['tags']}")
            print(f"  raw:   {r['raw']}")
            print()