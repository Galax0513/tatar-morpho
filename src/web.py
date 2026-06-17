#!/usr/bin/env python3
"""
web.py — веб-интерфейс морфологического анализатора (Flask)

Два режима:
    "Разобрать"  - словоформа -> разбор (analyze) + членение на морфемы
    "Построить"  - разбор -> словоформа (generate)

Запуск:
    python3 src/web.py
затем открыть в браузере http://127.0.0.1:5000
"""

import os
import sys
from flask import Flask, render_template, request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from analyzer import analyze, generate  # noqa: E402

app = Flask(__name__)

# ============================================================
# РАСШИФРОВКА ТЕГОВ
# ============================================================

# Подписи к пометам. Незнакомый тег покажем как есть
TAG_LABELS = {
    "N": "существительное",
    "V": "глагол",
    "Pl": "множественное число",
    "Nom": "именительный падеж",
    "Gen": "притяжательный падеж (чей)",
    "Dat": "направительный падеж (куда/кому)",
    "Acc": "винительный падеж (кого/что)",
    "Loc": "местный падеж (где)",
    "Abl": "исходный падеж (откуда)",
    "Neg": "отрицание",
    "Imp": "повелительное наклонение",
    "Past": "прошедшее время",
    "Pres": "настоящее время",
    "1Sg": "1 лицо, ед. ч.",
    "2Sg": "2 лицо, ед. ч.",
    "3Sg": "3 лицо, ед. ч.",
    "1Pl": "1 лицо, мн. ч.",
    "2Pl": "2 лицо, мн. ч.",
    "3Pl": "3 лицо, мн. ч.",
}

# Гласные татарского по ряду для подсветки сингармонизма
BACK_VOWELS = set("аоуы")     # твёрдый ряд
FRONT_VOWELS = set("әөүеиэ")  # мягкий ряд


def describe_tags(tags):
    """Превратить список тегов в пары (тег, расшифровка) для вывода."""
    return [(tag, TAG_LABELS.get(tag, tag)) for tag in tags]


def split_morphemes(word, lemma):
    """Разбить словоформу на корень и аффиксальную часть.

    Корень — это лемма, всё остальное в слове — аффиксы.
    Возвращает словарь {"root": ..., "affix": ...}.
    """
    word_lower = word.lower()
    if word_lower.startswith(lemma):
        # Корень берём из исходного слова (сохраняя регистр), хвост — аффиксы
        return {"root": word[:len(lemma)], "affix": word[len(lemma):]}
    return {"root": word, "affix": ""}


def mark_harmony(text):
    """Разметить буквы по ряду гласных для подсветки сингармонизма.

    Возвращает список пар (буква, класс), где класс — "back", "front" или "".
    """
    marked = []
    for ch in text:
        low = ch.lower()
        if low in BACK_VOWELS:
            marked.append((ch, "back"))
        elif low in FRONT_VOWELS:
            marked.append((ch, "front"))
        else:
            marked.append((ch, ""))
    return marked


# ============================================================
# РЕЖИМЫ ОБРАБОТКИ
# ============================================================

def do_analyze(word):
    """Режим разбора: словоформа -> список разборов с членением и тегами."""
    results = []
    for parse in analyze(word):
        morphemes = split_morphemes(word, parse["lemma"])
        results.append({
            "lemma": parse["lemma"],
            "tags": describe_tags(parse["tags"]),
            "root_marked": mark_harmony(morphemes["root"]),
            "affix_marked": mark_harmony(morphemes["affix"]),
            "has_affix": bool(morphemes["affix"]),
        })
    return results


def do_generate(text):
    """Режим генерации: разбор -> список словоформ.

    В URL знак "+" может прийти как пробел, поэтому возвращаем
    пробелы обратно в "+" перед обращением к ядру.
    """
    query = text.replace(" ", "+")
    return generate(query)


# ============================================================
# МАРШРУТЫ
# ============================================================

@app.route("/", methods=["GET"])
def index():
    """Главная страница: форма ввода и результат в выбранном режиме."""
    text = request.args.get("word", "").strip()
    mode = request.args.get("mode", "analyze")
    if mode not in ("analyze", "generate"):
        mode = "analyze"

    analyses = None
    forms = None

    if text:
        if mode == "generate":
            forms = do_generate(text)
        else:
            analyses = do_analyze(text)

    return render_template(
        "index.html",
        word=text,
        mode=mode,
        analyses=analyses,
        forms=forms,
    )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
