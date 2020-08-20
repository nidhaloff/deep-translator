"""
Yandex translator API
"""
import requests
from requests import exceptions
from deep_translator.constants import BASE_URLS
from deep_translator.exceptions import (RequestError,
                                        YandexDefaultException, TranslationNotFound)


class YandexTranslator(object):
    """
    class that wraps functions, which use the yandex translator under the hood to translate word(s)
    """

    def __init__(self, api_key=None):
        """
        @param api_key: your yandex api key
        """
        if not api_key:
            raise YandexDefaultException(401)
        self.__base_url = BASE_URLS.get("YANDEX")

        self.api_key = api_key
        self.api_version = "v1.5"
        self.api_endpoints = {
            "langs": "getLangs",
            "detect": "detect",
            "translate": "translate",
        }

    def get_supported_languages(self):
        return set(x.split("-")[0] for x in self.dirs)

    @property
    def languages(self):
        return self.get_supported_languages()

    @property
    def dirs(self, proxies=None):

        try:
            url = self.__base_url.format(version=self.api_version, endpoint="getLangs")
            print("url: ", url)
            response = requests.get(url, params={"key": self.api_key}, proxies=proxies)
        except requests.exceptions.ConnectionError:
            raise YandexDefaultException(503)
        else:
            data = response.json()

        if response.status_code != 200:
            raise YandexDefaultException(response.status_code)
        return data.get("dirs")


def detect(self, text, proxies=None):
    response = None
    params = {
        "text": text,
        "format": "plain",
        "key": self.api_key,
    }
    try:
        url = self.__base_url.format(version=self.api_version, endpoint="detect")
        response = requests.post(url, data=params, proxies=proxies)

    except RequestError:
        raise
    except ConnectionError:
        raise YandexDefaultException(503)
    except ValueError:
        raise YandexDefaultException(response.status_code)
    else:
        response = response.json()
    language = response['lang']
    status_code = response['code']
    if status_code != 200:
        raise RequestError()
    elif not language:
        raise YandexDefaultException(501)
    return language


def translate(self, text, lang, proxies=None):
    params = {
        "text": text,
        "format": "plain",
        "lang": lang,
        "key": self.api_key
    }
    try:
        url = self.__base_url.format(version=self.api_version, endpoint="translate")
        response = requests.post(url, data=params, proxies=proxies)
    except ConnectionError:
        raise YandexDefaultException(503)
    else:
        response = response.json()
    if response['code'] != 200:
        raise YandexDefaultException(response['code'])
    if not response['text']:
        raise TranslationNotFound()

    return response['text']
