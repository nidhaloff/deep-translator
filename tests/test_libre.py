#!/usr/bin/env python

"""Tests for `deep_translator` package."""

import pytest

from deep_translator import LibreTranslator, exceptions
from deep_translator.constants import LIBRE_LANGUAGES_TO_CODES


@pytest.fixture
def libre():
    return LibreTranslator(source="en", target="fr", api_key="some_key")


def test_inputs():
    with pytest.raises(exceptions.InvalidSourceOrTargetLanguage):
        LibreTranslator(source="", target="", api_key="some_key")

    with pytest.raises(exceptions.InvalidSourceOrTargetLanguage):
        LibreTranslator(source="auto", target="", api_key="some_key")

    with pytest.raises(exceptions.InvalidSourceOrTargetLanguage):
        LibreTranslator(source="", target="en", api_key="some_key")


def test_abbreviations_and_languages_mapping():
    for abb, lang in LIBRE_LANGUAGES_TO_CODES.items():
        l1 = LibreTranslator(source=abb, api_key="some_key")
        l2 = LibreTranslator(source=lang, api_key="some_key")
        assert l1._source == l2._source


def test_payload(libre):
    with pytest.raises(exceptions.NotValidPayload):
        libre.translate({})

    with pytest.raises(exceptions.NotValidPayload):
        libre.translate([])
