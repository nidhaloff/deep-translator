#!/usr/bin/env python

"""Tests for `deep_translator` package."""

import pytest

from deep_translator import WikimediaMinTMachineTranslator, exceptions
from deep_translator.constants import WIKIMEDIA_MINT_LANGUAGE_TO_CODE


@pytest.fixture
def mint():
    return WikimediaMinTMachineTranslator(source="en", target="fr")


def test_inputs():
    with pytest.raises(exceptions.InvalidSourceOrTargetLanguage):
        WikimediaMinTMachineTranslator(source="", target="")

    with pytest.raises(exceptions.InvalidSourceOrTargetLanguage):
        WikimediaMinTMachineTranslator(source="auto", target="")

    with pytest.raises(exceptions.InvalidSourceOrTargetLanguage):
        WikimediaMinTMachineTranslator(source="", target="en")


def test_abbreviations_and_languages_mapping():
    for abb, lang in WIKIMEDIA_MINT_LANGUAGE_TO_CODE.items():
        l1 = WikimediaMinTMachineTranslator(source=abb)
        l2 = WikimediaMinTMachineTranslator(source=lang)
        assert l1._source == l2._source


def test_payload(mint):
    with pytest.raises(exceptions.NotValidPayload):
        mint.translate({})

    with pytest.raises(exceptions.NotValidPayload):
        mint.translate([])

