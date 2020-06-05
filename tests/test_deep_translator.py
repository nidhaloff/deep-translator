#!/usr/bin/env python

"""Tests for `deep_translator` package."""

import pytest


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    pass
    # with pytest.raises(LanguageNotSupportedException):
    #     GoogleTranslator(source="", target="")
    #
    # with pytest.raises(LanguageNotSupportedException):
    #     GoogleTranslator(source="auto", target="nothing")


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string
