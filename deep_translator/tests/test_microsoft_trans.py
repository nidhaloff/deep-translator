#!/usr/bin/env python

"""Tests for `deep_translator` package."""

import pytest
from unittest.mock import patch
import requests

from deep_translator import exceptions, MicrosoftTranslator


# mocked request.post
@patch.object(requests, 'post')
def test_microsoft_successful_post_mock(mock_request_post):
    returned_json = [{'translations': [{'text': 'See you later!', 'to': 'en'}]}]
    def res():
        r = requests.Response()
        def json_func():
            return returned_json
        r.json = json_func
        return r
    mock_request_post.return_value = res()
    assert MicrosoftTranslator(api_key="an_api_key", target="en").translate("auf wiedersehen!") == "See you later!"


def test_MicrosoftAPIerror():
    with pytest.raises(exceptions.MicrosoftAPIerror):
        MicrosoftTranslator(api_key="empty", target="en").translate("text")


# the remaining tests are actual requests to Microsoft API and use an api key
# if APIkey variable is None, they are skipped

APIkey = None


@pytest.mark.skipif(APIkey is None, reason="api_key is not provided")
def test_microsoft_successful_post_onetarget():
    posted = MicrosoftTranslator(api_key=APIkey, target="en").translate("auf wiedersehen!")
    assert isinstance(posted, str)


@pytest.mark.skipif(APIkey is None, reason="api_key is not provided")
def test_microsoft_successful_post_twotargets():
    posted = MicrosoftTranslator(api_key=APIkey, target=["en", "ru"]).translate("auf wiedersehen!")
    assert isinstance(posted, str)


@pytest.mark.skipif(APIkey is None, reason="api_key is not provided")
def test_incorrect_target_attributes():
    with pytest.raises(exceptions.ServerException):
        MicrosoftTranslator(api_key=APIkey, target="")
    with pytest.raises(exceptions.ServerException):
        MicrosoftTranslator(api_key="", target="nothing")


@pytest.mark.skipif(APIkey is None, reason="api_key is not provided")
def test_abbreviations():
    m1 = MicrosoftTranslator(api_key=APIkey, source="en", target="fr")
    m2 = MicrosoftTranslator(api_key=APIkey, source="English", target="French")
    assert ''.join(m1.source) == ''.join(m2.source)
    assert ''.join(m1.target) == ''.join(m2.target)
