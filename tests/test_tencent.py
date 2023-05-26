from unittest.mock import Mock, patch

import pytest

from deep_translator import TencentTranslator
from deep_translator.exceptions import AuthorizationException


@patch("deep_translator.tencent.requests")
def test_simple_translation(mock_requests):
    translator = TencentTranslator(
        secret_id="this-is-an-valid-api-id",
        source="en",
        target="zh",
        secret_key="this-is-an-valid-api-key",
    )
    # Set the request response mock.
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"translations": [{"text": "hola"}]}
    mock_requests.get.return_value = mock_response
    translation = translator.translate("hello")
    assert translation == "你好"


@patch("deep_translator.tencent.requests.get")
def test_wrong_api_key(mock_requests):
    translator = TencentTranslator(
        secret_id="this-is-a-wrong-api-id",
        source="en",
        target="zh",
        secret_key="this-is-a-wrong-api-key",
    )
    # Set the response status_code only.
    mock_requests.return_value = Mock(status_code=403)
    with pytest.raises(AuthorizationException):
        translator.translate("Hello")
