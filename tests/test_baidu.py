from unittest.mock import Mock, patch

import pytest

from deep_translator import BaiduTranslator
from deep_translator.exceptions import BaiduAPIerror


@patch("deep_translator.baidu.requests")
def test_simple_translation(mock_requests):
    translator = BaiduTranslator(
        appid="this-is-an-valid-appid",
        appkey="this-is-an-valid-appkey",
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
        appid="this-is-a-wrong-appid",
        appkey="this-is-a-wrong-appkey",
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


# the remaining tests are actual requests to Baidu translator API and use appid and appkey
# if appid and appkey variable is None, they are skipped

appid = None
appkey = None


@pytest.mark.skipif(
    appid is None or appkey is None,
    reason="appid or appkey is not provided",
)
def test_baidu_successful_post_onetarget():
    posted = BaiduTranslator(
        appid=appid, appkey=appkey, source="en", target="zh"
    ).translate("Hello! How are you?")
    assert isinstance(posted, str)
