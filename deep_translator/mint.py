"""
Wikimedia MinT translator API
"""

__copyright__ = "Copyright (C) 2020 Nidhal Baccouri"

from typing import List, Optional

import requests
import json

from deep_translator.base import BaseTranslator
from deep_translator.constants import BASE_URLS, WIKIMEDIA_MINT_LANGUAGE_TO_CODE
from deep_translator.exceptions import (
    RequestError,
    TooManyRequests,
    ServerException,
    TranslationNotFound
)
from deep_translator.validate import is_empty, is_input_valid, request_failed


class WikimediaMinTMachineTranslator(BaseTranslator):
    """
    class that wraps functions, which use Wikimedia Translate under the hood to translate text(s)
    """

    def __init__(
        self,
        source: str = "en",
        target: str = "es",
        proxies: Optional[dict] = None,
        **kwargs
    ):
        """
        @param source: source language to translate from
        @param target: target language to translate to
        """
        self.proxies = proxies
        super().__init__(
            base_url=BASE_URLS.get("WIKIMEDIA_MINT"),
            source=source,
            target=target,
            languages=WIKIMEDIA_MINT_LANGUAGE_TO_CODE,
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
            detail = kwargs.get("detail")
            if self._same_source_target() or is_empty(text):
                return text
            
            self._base_url += "/" + self._source
            self._base_url += "/" + self._target

            headers = {
                "Content-Type" : "application/json"
            }

            # Create the payload
            data = json.dumps({"text" : text})

            # Check the connection and get the response
            try:
                response = requests.post(
                    self._base_url, data=data, headers=headers, proxies=self.proxies
                )
            except ConnectionError:
                raise ServerException()

            if response.status_code in {502,400}:
                raise ServerException(response.status_code)
            elif response.status_code == 429:
                raise TooManyRequests()

            if request_failed(status_code=response.status_code):
                raise RequestError()

            # Get the response and check if it is not empty
            res = response.json()
            if not res:
                raise TranslationNotFound(text)

            return res['translation'] if not detail else res


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
