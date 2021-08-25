#!/usr/bin/env python

"""Tests for `deep_translator` package."""

import pytest
from deep_translator import exceptions, GoogleTranslator
from deep_translator.constants import GOOGLE_CODES_TO_LANGUAGES, test_text_standard, TRANSLATED_RESULTS
import random

@pytest.fixture
def google_translator():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    return GoogleTranslator(target='en')

def case_sensitivity_checks():
    test_lang = 'Czech'
    test_text = 'Hi, the sky is dark while the moon is white. Hurrah!! Denver is a city name in Colorado.'
    translated_text = 'Ahoj, obloha je tmavá, zatímco měsíc je bílý. Hurá!! Denver je název města v Coloradu.'
    test_cases = []
    n = len(test_lang)
    mx = 1 << n
    test = test_lang.lower()
    for i in range(mx):
        combination = [k for k in test_lang]
        for j in range(n):
            if (((i >> j) & 1) == 1):
                combination[j] = test_lang[j].upper()
        temp = ""
        for i in combination:
            temp += i
        test_cases.append(temp)
    random_cases = 5
    random_test_cases = random.sample(test_cases, random_cases)  # randomly choosing any five cases since list is in order of 2^n containing all cases
    for case in random_test_cases:
        assert GoogleTranslator(source='en', target=case).translate(test_text) == translated_text

def multiple_names_lang_checks():
    assert GoogleTranslator(source='en', target='burMeSe').translate("Hello") == 'မင်္ဂလာပါ'
    assert GoogleTranslator(source='en', target='Oriya').translate("What's up?") == 'କଣ ଚାଲିଛି?'
    assert GoogleTranslator(source='en', target='kurManJi').translate("Nice is dice.") == 'Xweş xweş e.'

def test_random_tranlations_cases_multiple_names():
    random_sample_size = 5
    d = dict.fromkeys(list(TRANSLATED_RESULTS.keys()))
    random_lang_names = random.sample(d.keys(), random_sample_size)
    random_subset_dict = {k: TRANSLATED_RESULTS[k] for k in random_lang_names}
    for lang, translation in random_subset_dict.items():
        assert GoogleTranslator(source='en', target=lang).translate(test_text_standard) == translation

    case_sensitivity_checks()
    multiple_names_lang_checks()

def test_content(google_translator):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string
    assert google_translator.translate(text='좋은') == "good"

def test_abbreviations_and_languages_mapping():
    for abb, lang in GOOGLE_CODES_TO_LANGUAGES.items():
        if(abb!= 'en'):
            g1 = GoogleTranslator(abb)
            g2 = GoogleTranslator(lang)
            assert g1._source == g2._source

def test_inputs():
    with pytest.raises(exceptions.LanguageNotSupportedException):
        GoogleTranslator(source="", target="")

    with pytest.raises(exceptions.LanguageNotSupportedException):
        GoogleTranslator(source="auto", target="nothing")

def test_payload(google_translator):

    with pytest.raises(exceptions.NotValidPayload):
        google_translator.translate(text="")
        google_translator.translate(text='1234')
        google_translator.translate(text='{}')
        google_translator.translate(text='%@')

    with pytest.raises(exceptions.NotValidPayload):
        google_translator.translate(text=123)

    with pytest.raises(exceptions.NotValidPayload):
        google_translator.translate(text={})

    with pytest.raises(exceptions.NotValidPayload):
        google_translator.translate(text=[])

    with pytest.raises(exceptions.NotValidLength):
        google_translator.translate("a"*5001)

    #for _ in range(1):
    #assert google_translator.translate(text='좋은') == "good"

def test_one_character_words():
    assert GoogleTranslator(source='es', target='en').translate('o') == 'or'
