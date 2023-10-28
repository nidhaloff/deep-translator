#!/usr/bin/env python

"""Tests for `deep_translator` package."""

import pytest

from deep_translator import GlosbeTranslator, exceptions
from deep_translator.constants import GLOSBE_LANGUAGE_TO_CODE


@pytest.fixture
def glosbe():
    return GlosbeTranslator(source="en", target="fr")


def test_inputs():
    with pytest.raises(exceptions.InvalidSourceOrTargetLanguage):
        GlosbeTranslator(source="", target="")

    with pytest.raises(exceptions.InvalidSourceOrTargetLanguage):
        GlosbeTranslator(source="auto", target="")

    with pytest.raises(exceptions.InvalidSourceOrTargetLanguage):
        GlosbeTranslator(source="", target="en")


def test_abbreviations_and_languages_mapping():
    for abb, lang in GLOSBE_LANGUAGE_TO_CODE.items():
        l1 = GlosbeTranslator(source=abb)
        l2 = GlosbeTranslator(source=lang)
        assert l1._source == l2._source


def test_payload(glosbe):
    with pytest.raises(exceptions.NotValidPayload):
        glosbe.translate({})

    with pytest.raises(exceptions.NotValidPayload):
        glosbe.translate([])
