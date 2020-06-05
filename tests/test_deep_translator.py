#!/usr/bin/env python

"""Tests for `deep_translator` package."""

import pytest
from deep_translator import exceptions, GoogleTranslator


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    translator = GoogleTranslator(target='en')
    assert translator.translate(payload='좋은') == "good"
    with pytest.raises(exceptions.LanguageNotSupportedException):
        GoogleTranslator(source="", target="")

    with pytest.raises(exceptions.LanguageNotSupportedException):
        GoogleTranslator(source="auto", target="nothing")


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string
