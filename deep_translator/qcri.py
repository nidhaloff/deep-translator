"""
QCRI Translator API
"""

import requests
from .constants import BASE_URLS, QCRI_LANGUAGE_TO_CODE
from .exceptions import (ServerException, TranslationNotFound)


class QCRI(object):
    """
    Class that wraps functions, which use the QRCI translator under the hood to translate word(s)
    """

    def __init__(self, api_key=None, source="en", target="en", **_):
        """
        Args:
            api_key: str: your QCRI api key. Get one for free here https://mt.qcri.org/api/v1/ref
            source: str: source language to translate from.
            target: str: target language to translate to.
        Raises:
            ServerException
        """

        if not api_key:
            raise ServerException(401)
        self.__base_url = BASE_URLS.get("QCRI")
        self.source = source
        self.target = target
        self.api_key = api_key
        self.api_endpoints = {
            "get_languages": "getLanguagePairs",
            "get_domains": "getDomains",
            "translate": "translate",
        }

        self.params = {
            "key": self.api_key
        }

    def _get(self, endpoint, params=None, return_text=True, **kwargs):
        if not params:
            params = self.params
        try:
            res = requests.get(self.__base_url.format(endpoint=self.api_endpoints[endpoint]), params=params, **kwargs)
            return res.text if return_text else res
        except Exception as e:
            raise e

    @staticmethod
    def get_supported_languages(as_dict=False, **_):
        # Have no use for this as the format is not what we need
        # Save this for whenever
        # pairs = self._get("get_languages")
        # Using a this one instead
        return [*QCRI_LANGUAGE_TO_CODE.keys()] if not as_dict else QCRI_LANGUAGE_TO_CODE

    @property
    def languages(self):
        return self.get_supported_languages()

    def get_domains(self):
        domains = self._get("get_domains")
        return domains

    @property
    def domains(self):
        return self.get_domains()

    def translate(self, text, domain, **kwargs):
        """
        Function that uses Qcri translater to translate a word
        Args:
            text: str: text to translate.
            domain: str: domain for use Qcri trasnaltor
        Keyword Args:
            requests_kwargs: arbitrary args for requests.get.
        Returns:
             str: translated text.
        Raises:
            ServerException
            TranslationNotFound
        """
        params = {
            "key": self.api_key,
            "langpair": "{}-{}".format(self.source, self.target),
            "domain": domain,
            "text": text
        }
        try:
            response = self._get("translate", params=params, return_text=False, **kwargs.get("requests_kwargs", {}))
        except ConnectionError:
            raise ServerException(503)

        else:
            if response.status_code != 200:
                raise ServerException(response.status_code)
            res = response.json()
            translation = res.get("translatedText")
            if not translation:
                raise TranslationNotFound(text)
            return translation

    def translate_batch(self, batch, domain, **kwargs):
        """
        Translate a list of texts
        Args:
            batch: list: list of texts to translate.
            domain: str: domain for use QCRI Translator
            kwargs: dict: arbitrary args for PQCRIObject.translate
        Returns:
             list of translations
        Raises:
            Exception
        """
        return [self.translate(domain, text, **kwargs) for text in batch]
