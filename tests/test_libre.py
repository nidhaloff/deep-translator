#!/usr/bin/env python

"""Tests for `deep_translator` package."""

import pytest
from deep_translator import exceptions, LibreTranslator


@pytest.fixture
def libre():
    return LibreTranslator(source="en", target='fr')


def test_content(libre):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string
    assert libre.translate(text='good') is not None


def test_inputs():
    with pytest.raises(exceptions.LanguageNotSupportedException):
        LibreTranslator(source="", target="")

    with pytest.raises(exceptions.LanguageNotSupportedException):
        LibreTranslator(source="auto", target="nothing")

    l1 = LibreTranslator("en", "fr")
    l2 = LibreTranslator("english", "french")
    assert l1.source == l2.source
    assert l1.target == l2.target


def test_payload(libre):
    with pytest.raises(exceptions.NotValidPayload):
        libre.translate("")

    with pytest.raises(exceptions.NotValidPayload):
        libre.translate(123)

    with pytest.raises(exceptions.NotValidPayload):
        libre.translate({})

    with pytest.raises(exceptions.NotValidPayload):
        libre.translate([])


def test_one_character_words():
    assert LibreTranslator(source='es', target='en').translate('y') == 'and'
