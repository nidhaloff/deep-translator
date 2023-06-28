#!/usr/bin/env python

"""Tests for `deep_translator` package."""

import pytest

from deep_translator import GoogleTranslator, exceptions
from deep_translator.constants import GOOGLE_LANGUAGES_TO_CODES


@pytest.fixture
def google_translator():
    """Sample pytest fixture.
    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    return GoogleTranslator(target="en")


def test_content(google_translator):
    """Sample pytest test function with the pytest fixture as an argument."""
    assert google_translator.translate(text="좋은") == "good"


def test_abbreviations_and_languages_mapping():
    for abb, lang in GOOGLE_LANGUAGES_TO_CODES.items():
        g1 = GoogleTranslator(abb)
        g2 = GoogleTranslator(lang)
        assert g1._source == g2._source


def test_inputs():
    with pytest.raises(exceptions.InvalidSourceOrTargetLanguage):
        GoogleTranslator(source="", target="")

    with pytest.raises(exceptions.InvalidSourceOrTargetLanguage):
        GoogleTranslator(source="auto", target="")

    with pytest.raises(exceptions.InvalidSourceOrTargetLanguage):
        GoogleTranslator(source="", target="en")


def test_empty_text(google_translator):
    empty_txt = ""
    res = google_translator.translate(text=empty_txt)
    assert res == empty_txt


def test_payload(google_translator):
    with pytest.raises(exceptions.NotValidPayload):
        google_translator.translate(text={})

    with pytest.raises(exceptions.NotValidPayload):
        google_translator.translate(text=[])

    with pytest.raises(exceptions.NotValidLength):
        google_translator.translate("a" * 5001)


def test_one_character_words():
    assert (
        GoogleTranslator(source="es", target="en").translate("o") is not None
    )
