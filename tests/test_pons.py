#!/usr/bin/env python

"""Tests for `deep_translator` package."""

import pytest

from deep_translator import PonsTranslator, exceptions


@pytest.fixture
def pons():
    return PonsTranslator(source="english", target="french")


def test_content(pons):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string
    assert pons.translate(word="good") is not None


def test_inputs():
    with pytest.raises(exceptions.InvalidSourceOrTargetLanguage):
        PonsTranslator(source="", target="")

    with pytest.raises(exceptions.InvalidSourceOrTargetLanguage):
        PonsTranslator(source="auto", target="")

    with pytest.raises(exceptions.InvalidSourceOrTargetLanguage):
        PonsTranslator(source="", target="en")

    l1 = PonsTranslator("en", "fr")
    l2 = PonsTranslator("english", "french")
    assert l1._source == l2._source
    assert l1._target == l2._target


def test_payload(pons):
    with pytest.raises(exceptions.NotValidPayload):
        pons.translate({})

    with pytest.raises(exceptions.NotValidPayload):
        pons.translate([])

    with pytest.raises(exceptions.NotValidLength):
        pons.translate("a" * 51)
