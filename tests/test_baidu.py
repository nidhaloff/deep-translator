from unittest.mock import Mock, patch

import pytest

from deep_translator import BaiduTranslator
from deep_translator.exceptions import BaiduAPIerror


@patch("deep_translator.baidu.requests")
def test_simple_translation(mock_requests):
    translator = BaiduTranslator(
        secret_id="this-is-an-valid-api-id",
        secret_key="this-is-an-valid-api-key",
        source="en",
        target="zh",
    )
    # Set the request response mock.
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "from": "en",
        "to": "zh",
        "trans_result": [{"src": "hello", "dst": "你好"}],
    }
    mock_requests.post.return_value = mock_response
    translation = translator.translate("hello")
    assert translation == "你好"


@patch("deep_translator.baidu.requests.get")
def test_wrong_api_key(mock_requests):
    translator = BaiduTranslator(
        secret_id="this-is-a-wrong-api-id",
        secret_key="this-is-a-wrong-api-key",
        source="en",
        target="zh",
    )
    # Set the response status_code only.
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "error_code": "54001",
        "error_msg": "Invalid Sign",
    }
    mock_requests.post.return_value = mock_response
    with pytest.raises(BaiduAPIerror):
        translator.translate("Hello")
