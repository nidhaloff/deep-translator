from unittest.mock import Mock, patch

import pytest

from deep_translator.deepl import DeeplTranslator
from deep_translator.exceptions import AuthorizationException


@patch("deep_translator.deepl.requests")
def test_simple_translation(mock_requests):
    translator = DeeplTranslator(
        api_key="imagine-this-is-an-valid-api-key", source="en", target="es"
    )
    # Set the request response mock.
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"translations": [{"text": "hola"}]}
    mock_requests.get.return_value = mock_response
    translation = translator.translate("hello")
    assert translation == "hola"


@patch("deep_translator.deepl.requests.get")
def test_wrong_api_key(mock_requests):
    translator = DeeplTranslator(
        api_key="this-is-a-wrong-api-key!", source="en", target="es"
    )
    # Set the response status_code only.
    mock_requests.return_value = Mock(status_code=403)
    with pytest.raises(AuthorizationException):
        translator.translate("Hello")
