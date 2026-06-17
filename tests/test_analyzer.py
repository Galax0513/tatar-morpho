#!/usr/bin/env python3
"""
test_analyzer.py — золотой набор тестов

Запуск:
    python3 -m pytest tests/test_analyzer.py -v
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from analyzer import analyze


def assert_has_parse(word, expected_lemma, expected_tags):
    """Проверить, что среди разборов есть нужный вариант."""
    results = analyze(word)
    assert results, f"'{word}' не распознано (пустой результат)"

    for r in results:
        if r["lemma"] == expected_lemma and r["tags"] == expected_tags:
            return

    actual = [(r["lemma"], r["tags"]) for r in results]
    pytest.fail(
        f"'{word}': ожидали ({expected_lemma}, {expected_tags}),\n"
        f"  получили: {actual}"
    )


def assert_not_recognized(word):
    results = analyze(word)
    assert results == [], f"'{word}' неожиданно распознано: {results}"


# ============================================================
# СУЩЕСТВИТЕЛЬНЫЕ — ЗАДНЕРЯДНЫЕ
# ============================================================

class TestNounsBack:

    def test_kitap_nom(self):
        assert_has_parse("китап", "китап", ["N", "Nom"])

    def test_kitap_pl_nom(self):
        assert_has_parse("китаплар", "китап", ["N", "Pl", "Nom"])

    def test_kitap_loc(self):
        assert_has_parse("китапта", "китап", ["N", "Loc"])

    def test_kitap_pl_loc(self):
        assert_has_parse("китапларда", "китап", ["N", "Pl", "Loc"])

    def test_kitap_abl(self):
        assert_has_parse("китаптан", "китап", ["N", "Abl"])

    def test_kitap_pl_abl(self):
        assert_has_parse("китаплардан", "китап", ["N", "Pl", "Abl"])

    def test_kitap_gen(self):
        assert_has_parse("китапның", "китап", ["N", "Gen"])

    def test_kitap_dat(self):
        assert_has_parse("китапка", "китап", ["N", "Dat"])

    def test_kitap_acc(self):
        assert_has_parse("китапны", "китап", ["N", "Acc"])

    # --- бала ---

    def test_bala_nom(self):
        assert_has_parse("бала", "бала", ["N", "Nom"])

    def test_bala_pl(self):
        assert_has_parse("балалар", "бала", ["N", "Pl", "Nom"])

    def test_bala_loc(self):
        assert_has_parse("балада", "бала", ["N", "Loc"])

    def test_bala_abl(self):
        assert_has_parse("баладан", "бала", ["N", "Abl"])

    def test_bala_gen(self):
        assert_has_parse("баланың", "бала", ["N", "Gen"])

    def test_bala_dat(self):
        assert_has_parse("балага", "бала", ["N", "Dat"])

    def test_bala_acc(self):
        assert_has_parse("баланы", "бала", ["N", "Acc"])

    # --- урман ---

    def test_urman_loc(self):
        assert_has_parse("урманда", "урман", ["N", "Loc"])

    def test_urman_dat(self):
        assert_has_parse("урманга", "урман", ["N", "Dat"])

    # --- таш ---

    def test_tash_loc(self):
        assert_has_parse("ташта", "таш", ["N", "Loc"])

    def test_tash_dat(self):
        assert_has_parse("ташка", "таш", ["N", "Dat"])

    def test_tash_abl(self):
        assert_has_parse("таштан", "таш", ["N", "Abl"])


# ============================================================
# СУЩЕСТВИТЕЛЬНЫЕ — ПЕРЕДНЕРЯДНЫЕ
# ============================================================

class TestNounsFront:

    def test_ostal_nom(self):
        assert_has_parse("өстәл", "өстәл", ["N", "Nom"])

    def test_ostal_pl(self):
        assert_has_parse("өстәлләр", "өстәл", ["N", "Pl", "Nom"])

    def test_ostal_loc(self):
        assert_has_parse("өстәлдә", "өстәл", ["N", "Loc"])

    def test_ostal_abl(self):
        assert_has_parse("өстәлдән", "өстәл", ["N", "Abl"])

    def test_ostal_gen(self):
        assert_has_parse("өстәлнең", "өстәл", ["N", "Gen"])

    def test_ostal_dat(self):
        assert_has_parse("өстәлгә", "өстәл", ["N", "Dat"])

    def test_ostal_acc(self):
        assert_has_parse("өстәлне", "өстәл", ["N", "Acc"])

    # --- эт ---

    def test_et_nom(self):
        assert_has_parse("эт", "эт", ["N", "Nom"])

    def test_et_pl(self):
        assert_has_parse("этләр", "эт", ["N", "Pl", "Nom"])

    def test_et_loc(self):
        assert_has_parse("эттә", "эт", ["N", "Loc"])

    def test_et_dat(self):
        assert_has_parse("эткә", "эт", ["N", "Dat"])

    # --- мәктәп ---

    def test_maktap_loc(self):
        assert_has_parse("мәктәптә", "мәктәп", ["N", "Loc"])

    def test_maktap_pl(self):
        assert_has_parse("мәктәпләр", "мәктәп", ["N", "Pl", "Nom"])

    # --- күл ---

    def test_kul_loc(self):
        assert_has_parse("күлдә", "күл", ["N", "Loc"])

    def test_kul_dat(self):
        assert_has_parse("күлгә", "күл", ["N", "Dat"])


# ============================================================
# ГЛАГОЛЫ — ЗАДНЕРЯДНЫЕ
# ============================================================

class TestVerbsBack:

    def test_bar_imp(self):
        assert_has_parse("бар", "бар", ["V", "Imp", "2Sg"])

    def test_bar_past_3sg(self):
        assert_has_parse("барды", "бар", ["V", "Past", "3Sg"])

    def test_bar_past_1sg(self):
        assert_has_parse("бардым", "бар", ["V", "Past", "1Sg"])

    def test_bar_past_2sg(self):
        assert_has_parse("бардың", "бар", ["V", "Past", "2Sg"])

    def test_bar_past_3pl(self):
        assert_has_parse("бардылар", "бар", ["V", "Past", "3Pl"])

    def test_bar_pres_3sg(self):
        assert_has_parse("бара", "бар", ["V", "Pres", "3Sg"])

    def test_bar_pres_1sg(self):
        assert_has_parse("барам", "бар", ["V", "Pres", "1Sg"])

    def test_yaz_past(self):
        assert_has_parse("язды", "яз", ["V", "Past", "3Sg"])


# ============================================================
# ГЛАГОЛЫ — ПЕРЕДНЕРЯДНЫЕ
# ============================================================

class TestVerbsFront:

    def test_kil_imp(self):
        assert_has_parse("кил", "кил", ["V", "Imp", "2Sg"])

    def test_kil_past_3sg(self):
        assert_has_parse("килде", "кил", ["V", "Past", "3Sg"])

    def test_kil_past_1sg(self):
        assert_has_parse("килдем", "кил", ["V", "Past", "1Sg"])

    def test_kil_pres_3sg(self):
        assert_has_parse("килә", "кил", ["V", "Pres", "3Sg"])

    def test_kil_pres_1sg(self):
        assert_has_parse("киләм", "кил", ["V", "Pres", "1Sg"])

    def test_kur_past(self):
        assert_has_parse("күрде", "күр", ["V", "Past", "3Sg"])


# ============================================================
# ГЛАГОЛЫ — ОТРИЦАНИЕ
# ============================================================

class TestVerbsNeg:

    def test_bar_neg_past(self):
        assert_has_parse("бармады", "бар", ["V", "Neg", "Past", "3Sg"])

    def test_kil_neg_past(self):
        assert_has_parse("килмәде", "кил", ["V", "Neg", "Past", "3Sg"])

    def test_bar_neg_imp(self):
        assert_has_parse("барма", "бар", ["V", "Neg", "Imp", "2Sg"])

    def test_kil_neg_imp(self):
        assert_has_parse("килмә", "кил", ["V", "Neg", "Imp", "2Sg"])


# ============================================================
# АССИМИЛЯЦИЯ СОГЛАСНЫХ
# ============================================================

class TestAssimilation:

    def test_after_p(self):
        assert_has_parse("китапта", "китап", ["N", "Loc"])

    def test_after_t(self):
        assert_has_parse("атта", "ат", ["N", "Loc"])

    def test_after_ch(self):
        assert_has_parse("агачта", "агач", ["N", "Loc"])

    def test_after_sh_dat(self):
        assert_has_parse("ташка", "таш", ["N", "Dat"])

    def test_after_l(self):
        assert_has_parse("өстәлдә", "өстәл", ["N", "Loc"])

    def test_after_n(self):
        assert_has_parse("урманда", "урман", ["N", "Loc"])

    def test_after_vowel(self):
        assert_has_parse("балада", "бала", ["N", "Loc"])

    def test_after_vowel_dat(self):
        assert_has_parse("балага", "бала", ["N", "Dat"])


# ============================================================
# СИНГАРМОНИЗМ
# ============================================================

class TestHarmony:

    def test_back_pl(self):
        assert_has_parse("китаплар", "китап", ["N", "Pl", "Nom"])

    def test_front_pl(self):
        assert_has_parse("өстәлләр", "өстәл", ["N", "Pl", "Nom"])

    def test_back_gen(self):
        assert_has_parse("китапның", "китап", ["N", "Gen"])

    def test_front_gen(self):
        assert_has_parse("өстәлнең", "өстәл", ["N", "Gen"])

    def test_back_past(self):
        assert_has_parse("барды", "бар", ["V", "Past", "3Sg"])

    def test_front_past(self):
        assert_has_parse("килде", "кил", ["V", "Past", "3Sg"])


# ============================================================
# ПОЛНАЯ ПАРАДИГМА
# ============================================================

class TestFullParadigm:

    def test_kitap_sg(self):
        cases = {
            "китап": ["N", "Nom"],
            "китапның": ["N", "Gen"],
            "китапка": ["N", "Dat"],
            "китапны": ["N", "Acc"],
            "китапта": ["N", "Loc"],
            "китаптан": ["N", "Abl"],
        }
        for form, tags in cases.items():
            assert_has_parse(form, "китап", tags)

    def test_kitap_pl(self):
        cases = {
            "китаплар": ["N", "Pl", "Nom"],
            "китапларның": ["N", "Pl", "Gen"],
            "китапларга": ["N", "Pl", "Dat"],
            "китапларны": ["N", "Pl", "Acc"],
            "китапларда": ["N", "Pl", "Loc"],
            "китаплардан": ["N", "Pl", "Abl"],
        }
        for form, tags in cases.items():
            assert_has_parse(form, "китап", tags)

    def test_ostal_sg(self):
        cases = {
            "өстәл": ["N", "Nom"],
            "өстәлнең": ["N", "Gen"],
            "өстәлгә": ["N", "Dat"],
            "өстәлне": ["N", "Acc"],
            "өстәлдә": ["N", "Loc"],
            "өстәлдән": ["N", "Abl"],
        }
        for form, tags in cases.items():
            assert_has_parse(form, "өстәл", tags)


# ============================================================
# КРАЕВЫЕ СЛУЧАИ
# ============================================================

class TestEdgeCases:

    def test_empty(self):
        assert analyze("") == []

    def test_none(self):
        assert analyze(None) == []

    def test_whitespace(self):
        assert analyze("   ") == []

    def test_unknown(self):
        assert analyze("qqqqq") == []

    def test_digits(self):
        assert analyze("12345") == []

    def test_case_insensitive(self):
        r1 = analyze("китап")
        r2 = analyze("Китап")
        assert r1
        assert r2
        assert {r["lemma"] for r in r1} == {r["lemma"] for r in r2}