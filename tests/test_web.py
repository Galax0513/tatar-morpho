#!/usr/bin/env python3
"""
test_web.py — тесты веб-интерфейса (Flask)

Проверяем, что страница открывается, разбирает слова и корректно
ведёт себя на краевых случаях.

Запуск:
    python3 -m pytest tests/test_web.py -v
"""

import os
import sys
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from web import app, describe_tags  # noqa: E402


@pytest.fixture
def client():
    """Тестовый клиент Flask."""
    app.config["TESTING"] = True
    return app.test_client()


# ============================================================
# СТРАНИЦА ОТКРЫВАЕТСЯ
# ============================================================

class TestPageLoads:

    def test_index_status(self, client):
        assert client.get("/").status_code == 200

    def test_index_has_form(self, client):
        html = client.get("/").data.decode("utf-8")
        assert "<form" in html
        assert 'name="word"' in html


# ============================================================
# РАЗБОР СЛОВ ОТОБРАЖАЕТСЯ
# ============================================================

class TestAnalysisRendered:

    def test_noun_shown(self, client):
        html = client.get("/?word=китапларда").data.decode("utf-8")
        assert "китап" in html
        assert "местный падеж" in html

    def test_verb_shown(self, client):
        html = client.get("/?word=килде").data.decode("utf-8")
        assert "кил" in html
        assert "прошедшее время" in html

    def test_unknown_shown(self, client):
        html = client.get("/?word=qqqqq").data.decode("utf-8")
        assert "не распознано" in html


# ============================================================
# ГЕНЕРАЦИЯ ОТОБРАЖАЕТСЯ
# ============================================================

class TestGenerationRendered:

    def test_generate_noun(self, client):
        html = client.get("/?mode=generate&word=китап+N+Pl+Loc").data.decode("utf-8")
        assert "китапларда" in html

    def test_generate_verb(self, client):
        html = client.get("/?mode=generate&word=кил+V+Past+3Sg").data.decode("utf-8")
        assert "килде" in html

    def test_generate_bad_query(self, client):
        html = client.get("/?mode=generate&word=мусор+X").data.decode("utf-8")
        assert "не удалось построить" in html

    def test_generate_tolerates_spaces(self, client):
        # "+" в URL приходит как пробел, и генерация должна всё равно работать.
        html = client.get("/?mode=generate&word=кил V Past 3Sg").data.decode("utf-8")
        assert "килде" in html


# ============================================================
# КРАЕВЫЕ СЛУЧАИ
# ============================================================

class TestEdgeCases:

    def test_empty_query(self, client):
        # Без слова - страница открывается, результатов нет.
        html = client.get("/?word=").data.decode("utf-8")
        assert "не распознано" not in html

    def test_digits(self, client):
        html = client.get("/?word=12345").data.decode("utf-8")
        assert "не распознано" in html

    def test_case_insensitive(self, client):
        lower = client.get("/?word=китап").data.decode("utf-8")
        upper = client.get("/?word=КИТАП").data.decode("utf-8")
        assert ("китап" in lower) and ("китап" in upper)

    def test_whitespace_trimmed(self, client):
        html = client.get("/?word=  китап  ").data.decode("utf-8")
        assert "китап" in html


# ============================================================
# РАСШИФРОВКА ТЕГОВ
# ============================================================

class TestDescribeTags:

    def test_known_tags(self):
        pairs = describe_tags(["N", "Pl", "Loc"])
        assert ("N", "существительное") in pairs
        assert ("Loc", "местный падеж (где)") in pairs

    def test_unknown_tag_passthrough(self):
        # Незнакомый тег возвращается как есть, без падения.
        assert describe_tags(["XYZ"]) == [("XYZ", "XYZ")]

    def test_empty(self):
        assert describe_tags([]) == []
