#!/usr/bin/env python3
"""
build.py — генерирует все словоформы и сохраняет в JSON
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lexicon import NOUNS, VERBS
from morphology import (
    NOUN_PLURAL, NOUN_CASES,
    VERB_NEGATION, VERB_TENSES,
    VERB_PERSON_IMP, VERB_PERSON_PAST, VERB_PERSON_PRES,
)
from phonology import apply_suffix, resolve_Abl


def add_entry(forms, surface, lemma, tags):
    """Добавить запись в словарь форм."""
    raw = lemma + "+" + "+".join(tags)
    entry = {"lemma": lemma, "tags": tags, "raw": raw}
    if surface not in forms:
        forms[surface] = []
    forms[surface].append(entry)


def apply_case(stem, case_tag, case_template):
    """Применить падежный суффикс, с учётом особого Abl."""
    if case_template == "__ABL__":
        return stem + resolve_Abl(stem)
    elif case_template:
        return apply_suffix(stem, case_template)
    else:
        return stem


def build_noun_forms():
    forms = {}

    for lemma in sorted(NOUNS):
        #  ед число
        for case_tag, case_template in NOUN_CASES.items():
            surface = apply_case(lemma, case_tag, case_template)
            add_entry(forms, surface, lemma, ["N", case_tag])

        # мн число
        pl_surface = apply_suffix(lemma, NOUN_PLURAL["template"])

        for case_tag, case_template in NOUN_CASES.items():
            surface = apply_case(pl_surface, case_tag, case_template)
            add_entry(forms, surface, lemma, ["N", "Pl", case_tag])

    return forms


def build_verb_forms():
    forms = {}

    for lemma in sorted(VERBS):
        neg_variants = [
            ([], lemma),
        ]
        neg_surface = apply_suffix(lemma, VERB_NEGATION["template"])
        neg_variants.append((["Neg"], neg_surface))

        for neg_tags, stem_after_neg in neg_variants:
            for tense_tag, tense_template in VERB_TENSES.items():
                if tense_template:
                    tense_surface = apply_suffix(stem_after_neg, tense_template)
                else:
                    tense_surface = stem_after_neg

                if tense_tag == "Imp":
                    person_set = VERB_PERSON_IMP
                elif tense_tag == "Past":
                    person_set = VERB_PERSON_PAST
                else:
                    person_set = VERB_PERSON_PRES

                for person_tag, person_template in person_set.items():
                    if person_template:
                        full_surface = apply_suffix(tense_surface, person_template)
                    else:
                        full_surface = tense_surface

                    tags = ["V"] + neg_tags + [tense_tag, person_tag]
                    add_entry(forms, full_surface, lemma, tags)

    return forms


def build():
    print("=" * 60)
    print("сборка татарского морфологического словаря")

    print("\n[1/3] генерируем формы существительных")
    noun_forms = build_noun_forms()
    noun_count = sum(len(v) for v in noun_forms.values())
    print(f"  → {len(noun_forms)} словоформ, {noun_count} разборов")

    print("\n[2/3] генерируем формы глаголов")
    verb_forms = build_verb_forms()
    verb_count = sum(len(v) for v in verb_forms.values())
    print(f"  → {len(verb_forms)} словоформ, {verb_count} разборов")

    print("\n[3/3] Объединяю и сохраняю...")
    all_forms = {}
    for d in [noun_forms, verb_forms]:
        for surface, entries in d.items():
            if surface not in all_forms:
                all_forms[surface] = []
            all_forms[surface].extend(entries)

    output_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "tatar.json"
    )
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_forms, f, ensure_ascii=False, indent=2)

    total_forms = len(all_forms)
    total_analyses = sum(len(v) for v in all_forms.values())

    print(f"\n{'=' * 60}")
    print(f"  Словоформ:  {total_forms}")
    print(f"  Разборов:   {total_analyses}")
    print(f"{'=' * 60}")

    print("\nБыстрый тест:")
    test_words = ["китапларда", "борында", "борыннан", "борынга",
                  "килде", "бармады", "өстәлдә", "бардың", "язды"]
    for word in test_words:
        if word in all_forms:
            for entry in all_forms[word]:
                print(f"  ✓ {word} → {entry['raw']}")
        else:
            print(f"  ✗ {word} → НЕ НАЙДЕНО")

    return all_forms


if __name__ == "__main__":
    build()