import requests

from .validate import is_empty
from .constants import BASE_URLS, DEEPL_LANGUAGE_TO_CODE
from .exceptions import (ServerException,
                         TranslationNotFound,
                         AuthorizationException)
from .base import BaseTranslator


class DeeplTranslator(BaseTranslator):
    """
    class that wraps functions, which use the DeeplTranslator translator under the hood to translate word(s)
    """

    def __init__(self, api_key=None, source="de", target="en", use_free_api=True, **kwargs):
        """
        @param api_key: your DeeplTranslator api key.
        Get one here: https://www.deepl.com/docs-api/accessing-the-api/
        @param source: source language
        @param target: target language
        """
        if not api_key:
            raise ServerException(401)
        self.version = 'v2'
        self.api_key = api_key
        if use_free_api:
            self._base_url = BASE_URLS.get(
                "DEEPL_FREE").format(version=self.version)
        else:
            self._base_url = BASE_URLS.get(
                "DEEPL").format(version=self.version)
        super().__init__(source=source,
                         target=target,
                         languages=DEEPL_LANGUAGE_TO_CODE)

    def translate(self, text, **kwargs):
        """
        @param text: text to translate
        @return: translated text
        """
        if self._same_source_target() or is_empty(text):
            return text

        # Create the request parameters.
        translate_endpoint = 'translate'
        params = {
            "auth_key": self.api_key,
            "source_lang": self._source,
            "target_lang": self._target,
            "text": text
        }
        # Do the request and check the connection.
        try:
            response = requests.get(
                self._base_url + translate_endpoint, params=params)
        except ConnectionError:
            raise ServerException(503)
        # If the answer is not success, raise server exception.
        if response.status_code == 403:
            raise AuthorizationException(self.api_key)
        elif response.status_code != 200:
            raise ServerException(response.status_code)
        # Get the response and check is not empty.
        res = response.json()
        if not res:
            raise TranslationNotFound(text)
        # Process and return the response.
        return res['translations'][0]['text']

    def translate_file(self, path, **kwargs):
        return self._translate_file(path, **kwargs)

    def translate_batch(self, batch, **kwargs):
        """
        @param batch: list of texts to translate
        @return: list of translations
        """
        return self._translate_batch(batch, **kwargs)


if __name__ == '__main__':
    d = DeeplTranslator(target="de")
    t = d.translate("I have no idea")
    print("text: ", t)
