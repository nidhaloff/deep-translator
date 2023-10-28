"""
google translator API
"""

__copyright__ = "Copyright (C) 2020 Nidhal Baccouri"

from typing import List, Optional

import requests

from deep_translator.base import BaseTranslator
from deep_translator.constants import BASE_URLS, GLOSBE_LANGUAGE_TO_CODE
from deep_translator.exceptions import (
    RequestError,
    TooManyRequests,
    ServerException,
    TranslationNotFound
)
from deep_translator.validate import is_empty, is_input_valid, request_failed


class GlosbeTranslator(BaseTranslator):
    """
    class that wraps functions, which use Glosbe Translate under the hood to translate text(s)
    """

    def __init__(
        self,
        source: str = "en",
        target: str = "pl",
        proxies: Optional[dict] = None,
        **kwargs
    ):
        """
        @param source: source language to translate from
        @param target: target language to translate to
        """
        self.proxies = proxies
        super().__init__(
            base_url=BASE_URLS.get("GLOSBE"),
            source=source,
            target=target,
            languages=GLOSBE_LANGUAGE_TO_CODE,
            **kwargs
        )

    def translate(self, text: str, **kwargs) -> str:
        """
        function to translate a text
        @param text: desired text to translate
        @return: str: translated text
        """
        if is_input_valid(text):
            text = text.strip()
            if self._same_source_target() or is_empty(text):
                return text
            
            self._url_params["targetLang"] = self._target
            self._url_params["sourceLang"] = self._source

            headers = {
                "Content-Type" : "text/plain"
            }

            # Check the connection and get the response
            try:
                response = requests.post(
                    self._base_url, params=self._url_params, data=text, headers=headers, proxies=self.proxies
                )
            except ConnectionError:
                raise ServerException()
            
            if response.status_code == 415:
                raise ServerException(response.status_code)
            elif response.status_code == 429:
                raise TooManyRequests()

            if request_failed(status_code=response.status_code):
                raise RequestError()

            # Get the response and check if it is not empty
            res = response.json()
            if not res:
                raise TranslationNotFound(text)

            return res['translation']


    def translate_file(self, path: str, **kwargs) -> str:
        """
        translate directly from file
        @param path: path to the target file
        @type path: str
        @param kwargs: additional args
        @return: str
        """
        return self._translate_file(path, **kwargs)

    def translate_batch(self, batch: List[str], **kwargs) -> List[str]:
        """
        translate a list of texts
        @param batch: list of texts you want to translate
        @return: list of translations
        """
        return self._translate_batch(batch, **kwargs)
