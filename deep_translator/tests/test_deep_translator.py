#!/usr/bin/env python

"""Tests for `deep_translator` package."""

import pytest
from deep_translator import exceptions, GoogleTranslator


@pytest.fixture
def google_translator():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    return GoogleTranslator(target='en')


def test_content(google_translator):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string
    assert google_translator.translate(payload='좋은') == "good"


def test_inputs():
    with pytest.raises(exceptions.LanguageNotSupportedException):
        GoogleTranslator(source="", target="")

    with pytest.raises(exceptions.LanguageNotSupportedException):
        GoogleTranslator(source="auto", target="nothing")


def test_payload(google_translator):
    with pytest.raises(exceptions.NotValidPayload):
        google_translator.translate(payload="")
    with pytest.raises(exceptions.NotValidPayload):
        google_translator.translate(payload=123)


