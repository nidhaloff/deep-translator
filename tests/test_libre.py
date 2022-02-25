#!/usr/bin/env python

"""Tests for `deep_translator` package."""

import pytest
from deep_translator import exceptions, LibreTranslator
from deep_translator.constants import LIBRE_CODES_TO_LANGUAGES


@pytest.fixture
def libre():
    return LibreTranslator(source="en", target='fr')


def test_content(libre):
    """Sample pytest test function with the pytest fixture as an argument."""
    assert libre.translate(text='good') is not None


def test_inputs():
    with pytest.raises(exceptions.InvalidSourceOrTargetLanguage):
        LibreTranslator(source="", target="")

    with pytest.raises(exceptions.InvalidSourceOrTargetLanguage):
        LibreTranslator(source="auto", target="")

    with pytest.raises(exceptions.InvalidSourceOrTargetLanguage):
        LibreTranslator(source="", target="en")


def test_abbreviations_and_languages_mapping():
    for abb, lang in LIBRE_CODES_TO_LANGUAGES.items():
        l1 = LibreTranslator(abb)
        l2 = LibreTranslator(lang)
        assert l1._source == l2._source


def test_payload(libre):
    with pytest.raises(exceptions.NotValidPayload):
        libre.translate(123)

    with pytest.raises(exceptions.NotValidPayload):
        libre.translate({})

    with pytest.raises(exceptions.NotValidPayload):
        libre.translate([])


def test_one_character_words():
    assert LibreTranslator(source='es', target='en').translate('y') == 'and'


def test_translate_batch():
    words_to_translate = ['How are you', 'Good', 'Thank You']
    translated_words = ['¿Cómo estás?', 'Bien.', 'Gracias.']
    assert LibreTranslator(source='en', target='es').translate_batch((words_to_translate)) == translated_words


def test_translate_file():
    filePath = 'examples/test.txt'
    translatedText = 'Un párrafo es una serie de frases relacionadas que desarrollan una idea central, llamada el tema. Trate de pensar en los párrafos en términos de unidad temática: un párrafo es una frase o un grupo de oraciones que apoya una idea central y unificada. Los párrafos añaden una idea a la vez a su argumento más amplio.'
    assert LibreTranslator(source='en', target='es').translate_file(filePath) == translatedText
