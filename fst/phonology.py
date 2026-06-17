#!/usr/bin/env python3
"""
phonology.py — фонологические правила татарского языка

1. Нёбный сингармонизм (гласные)
2. Ассимиляция согласных (звонкость)
3. Назальная ассимиляция:
   - н + л → нн (борын + лар → борыннар)
   - н + д → нн в Abl (борын + дан → борыннан)
"""

BACK_CARRIERS = set("аоуыяюАОУЫЯЮ")
FRONT_CARRIERS = set("әөүеиӘӨҮЕИ")
ALL_VOWEL_CARRIERS = BACK_CARRIERS | FRONT_CARRIERS

BACK_VOWELS = set("аоуыАОУЫ")
FRONT_VOWELS = set("әөүеиӘӨҮЕИ")
ALL_VOWELS = BACK_VOWELS | FRONT_VOWELS

VOICELESS = set("пткчшщфхцһПТКЧШЩФХЦҺ")


def get_last_vowel_carrier(stem: str) -> str:
    for ch in reversed(stem):
        if ch in ALL_VOWEL_CARRIERS:
            return ch
    return ""


def is_back(stem: str) -> bool:
    return get_last_vowel_carrier(stem) in BACK_CARRIERS


def is_front(stem: str) -> bool:
    return get_last_vowel_carrier(stem) in FRONT_CARRIERS


def ends_with_voiceless(stem: str) -> bool:
    return bool(stem) and stem[-1] in VOICELESS


def ends_with_vowel(stem: str) -> bool:
    return bool(stem) and stem[-1] in ALL_VOWELS


def ends_with_n(stem: str) -> bool:
    return bool(stem) and stem[-1] in ("н", "Н")


def resolve_A(stem: str) -> str:
    return "а" if is_back(stem) else "ә"


def resolve_I(stem: str) -> str:
    return "ы" if is_back(stem) else "е"


def resolve_D(stem: str) -> str:
    if ends_with_voiceless(stem):
        return "т"
    return "д"


def resolve_G(stem: str) -> str:
    if ends_with_voiceless(stem):
        return "к"
    return "г"


def resolve_Abl(stem: str) -> str:
    """Исходный падеж: н+д → нн (борыннан), иначе обычные правила."""
    a = "а" if is_back(stem) else "ә"
    if ends_with_n(stem):
        return "н" + a + "н"
    elif ends_with_voiceless(stem):
        return "т" + a + "н"
    else:
        return "д" + a + "н"


def apply_suffix(stem: str, suffix_template: str) -> str:
    """
    Применить шаблон суффикса к основе.

    Обрабатывает:
    - {A} → а/ә, {I} → ы/е, {D} → д/т, {G} → г/к
    - Ассимиляция н+л → нн (автоматически)
    """
    current_stem = stem
    result = []
    i = 0

    while i < len(suffix_template):
        if suffix_template[i] == "{":
            j = suffix_template.index("}", i)
            code = suffix_template[i + 1:j]

            if code == "A":
                ch = resolve_A(current_stem)
            elif code == "I":
                ch = resolve_I(current_stem)
            elif code == "D":
                ch = resolve_D(current_stem)
            elif code == "G":
                ch = resolve_G(current_stem)
            else:
                ch = suffix_template[i:j + 1]

            result.append(ch)
            current_stem = current_stem + ch
            i = j + 1
        else:
            result.append(suffix_template[i])
            current_stem = current_stem + suffix_template[i]
            i += 1

    # Собираем результат
    suffix_str = "".join(result)

    # === Ассимиляция на стыке основы и суффикса ===
    # н + л → нн
    if stem and stem[-1] in ("н", "Н") and suffix_str and suffix_str[0] == "л":
        suffix_str = "н" + suffix_str[1:]

    return stem + suffix_str