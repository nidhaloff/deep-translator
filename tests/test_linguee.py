#!/usr/bin/env python

"""Tests for `deep_translator` package."""

import pytest

from deep_translator import LingueeTranslator, exceptions


@pytest.fixture
def linguee():
    return LingueeTranslator(source="english", target="german")


def test_content(linguee):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string
    assert linguee.translate(word="good") is not None


def test_inputs():
    with pytest.raises(exceptions.InvalidSourceOrTargetLanguage):
        LingueeTranslator(source="", target="")

    with pytest.raises(exceptions.InvalidSourceOrTargetLanguage):
        LingueeTranslator(source="auto", target="")

    with pytest.raises(exceptions.InvalidSourceOrTargetLanguage):
        LingueeTranslator(source="", target="en")

    with pytest.raises(exceptions.LanguageNotSupportedException):
        LingueeTranslator(source="en", target="fr")

    ling_translate = LingueeTranslator("english", "french")
    assert ling_translate._source == "english"
    assert ling_translate._target == "french"


def test_payload(linguee):
    with pytest.raises(exceptions.NotValidPayload):
        linguee.translate({})

    with pytest.raises(exceptions.NotValidPayload):
        linguee.translate([])

    with pytest.raises(exceptions.NotValidLength):
        linguee.translate("a" * 51)
