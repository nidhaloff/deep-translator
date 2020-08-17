#!/usr/bin/env python

"""Tests for `deep_translator` package."""

import pytest
from deep_translator import exceptions, PonsTranslator


@pytest.fixture
def pons():
    return PonsTranslator(source="en", target='fr')


def test_content(pons):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string
    assert pons.translate(word='good') is not None


def test_inputs():
    with pytest.raises(exceptions.LanguageNotSupportedException):
        pons(source="", target="")

    with pytest.raises(exceptions.LanguageNotSupportedException):
        pons(source="auto", target="nothing")


def test_payload(pons):

    with pytest.raises(exceptions.NotValidPayload):
        pons.translate("")

    with pytest.raises(exceptions.NotValidPayload):
        pons.translate(123)

    with pytest.raises(exceptions.NotValidPayload):
        pons.translate({})

    with pytest.raises(exceptions.NotValidPayload):
        pons.translate([])
