from unittest.mock import Mock, patch

import pytest

from deep_translator import TencentTranslator
from deep_translator.exceptions import TencentAPIerror


@patch("deep_translator.tencent.requests")
def test_simple_translation(mock_requests):
    translator = TencentTranslator(
        secret_id="imagine-this-is-an-valid-secret-id",
        secret_key="imagine-this-is-an-valid-secret-key",
        source="en",
        target="zh",
    )
    # Set the request response mock.
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "Response": {
            "TargetText": "你好",
            "Source": "en",
            "Target": "zh",
            "RequestId": "000ee211-f19e-4a34-a214-e2bb1122d248",
        }
    }
    mock_requests.get.return_value = mock_response
    translation = translator.translate("hello")
    assert translation == "你好"


@patch("deep_translator.tencent.requests")
def test_wrong_api_key(mock_requests):
    translator = TencentTranslator(
        secret_id="imagine-this-is-a-wrong-secret-id",
        secret_key="imagine-this-is-a-wrong-secret-id",
        source="en",
        target="zh",
    )

    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "Response": {
            "Error": {
                "Code": "AuthFailure.SignatureFailure",
                "Message": "The provided credentials could not be validated. \
                Please check your signature is correct.",
            },
            "RequestId": "ed93f3cb-f35e-473f-b9f3-0d451b8b79c6",
        }
    }
    mock_requests.get.return_value = mock_response
    with pytest.raises(TencentAPIerror):
        translator.translate("Hello")
