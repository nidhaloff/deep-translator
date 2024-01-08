import requests
import json
from typing import List, Optional, Union
from deep_translator.base import BaseTranslator
from deep_translator.constants import GOOGLE_LANGUAGES_TO_CODES
from deep_translator.exceptions import (
    NotValidPayload,
    RequestError,
    TooManyRequests,
    TranslationNotFound,
)


class PonsAPITranslator(BaseTranslator):
    def __init__(
        self,
        source: str,
        target: str = "en",
        proxies: Optional[dict] = None,
        **kwargs,
    ):
        self.proxies = proxies
        super().__init__(
            base_url="https://api.pons.com/text-translation-web/v4/translate?locale=en",
            languages=GOOGLE_LANGUAGES_TO_CODES,
            source=source,
            target=target,
            **kwargs,
        )

    def translate(self, word: str, **kwargs) -> str:
        headers = {
            'accept': '*/*',
            'content-type': 'application/json',
        }
        data = {
            "impressionId": "48bff56e-aa3f-4463-adb7-8282500be5a4",  # this might need to be dynamic or removed
            "targetLanguage": self._target,
            "text": word,
            "sourceLanguage": self._source
        }
        response = requests.post(self._base_url, headers=headers, json=data, proxies=self.proxies)

        if response.status_code == 429:
            raise TooManyRequests()

        if not response.ok:
            raise RequestError()

        response_data = response.json()
        if "text" in response_data:
            return response_data["text"]

        raise TranslationNotFound(word)

    def translate_words(self, words: List[str], **kwargs) -> List[str]:
        if not words:
            raise NotValidPayload(words)

        return [self.translate(word=word, **kwargs) for word in words]
