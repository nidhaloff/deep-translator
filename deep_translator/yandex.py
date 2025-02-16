
# (C)oded by .NetXCore

import os
from typing import List, Optional

import requests

from deep_translator.base import BaseTranslator
from deep_translator.constants import BASE_URLS, YANDEX_ENV_VAR
from deep_translator.exceptions import (
    ApiKeyException,
    RequestError,
    ServerException,
    TooManyRequests,
    TranslationNotFound,
)
from deep_translator.validate import is_input_valid, request_failed


class YandexTranslator(BaseTranslator):
    """
    Class that wraps functions to use the Yandex Translator API v2.
    """

    def __init__(
        self,
        source: str = "en",
        target: str = "de",
        api_key: Optional[str] = os.getenv(YANDEX_ENV_VAR, None),
        folder_id: Optional[str] = None,  # Required for Yandex v2 API
        **kwargs
    ):
        """
        @param api_key: Your Yandex API key.
        @param folder_id: Your Yandex folder ID
        """
        if not api_key:
            raise ApiKeyException(YANDEX_ENV_VAR)
        self.api_key = api_key
        self.folder_id = folder_id
        self.api_version = "v2"
        self.api_endpoint = "translate"
        super().__init__(
            base_url=BASE_URLS.get("YANDEX"),
            source=source,
            target=target,
            **kwargs
        )

    def translate(
        self, text: str, proxies: Optional[dict] = None, **kwargs
    ) -> str:
        if is_input_valid(text):

            url = f"{self._base_url}/{self.api_version}/{self.api_endpoint}"

            headers = {
                "Authorization": f"Api-Key {self.api_key}",
                "Content-Type": "application/json",
            }
            body = {
                "sourceLanguageCode": self._source,
                "targetLanguageCode": self._target,
                "texts": [text],
                "folderId": self.folder_id,  # Required for v2 API
            }

            try:
                response = requests.post(
                    url, json=body, headers=headers, proxies=proxies
                )
                response.raise_for_status()  # Raise an exception for HTTP errors
            except requests.exceptions.RequestException as e:
                raise ServerException(str(e))

            data = response.json()

            if "translations" not in data:
                raise TranslationNotFound()

            return data["translations"][0]["text"]

    def translate_file(self, path: str, **kwargs) -> str:
        """
        Translate from a file.
        @param path: Path to file.
        @return: Translated text.
        """
        return self._translate_file(path, **kwargs)

    def translate_batch(self, batch: List[str], **kwargs) -> List[str]:
        """
        Translate a batch of texts.
        @param batch: List of texts to translate.
        @return: List of translations.
        """
        return self._translate_batch(batch, **kwargs)