import requests
from deep_translator.constants import BASE_URLS, DEEPL_LANGUAGE_TO_CODE
from deep_translator.exceptions import (ServerException,
                                        TranslationNotFound,
                                        LanguageNotSupportedException,
                                        AuthorizationException)


class DeepL(object):
    """
    class that wraps functions, which use the DeepL translator under the hood to translate word(s)
    """
    _languages = DEEPL_LANGUAGE_TO_CODE

    def __init__(self, api_key=None):
        """
        @param api_key: your DeepL api key.
        Get one here: https://www.deepl.com/docs-api/accessing-the-api/
        """
        if not api_key:
            raise ServerException(401)
        self.version = 'v2'
        self.api_key = api_key
        self.__base_url = BASE_URLS.get("DEEPL").format(version=self.version)

    def translate(self, source, target, text):
        # Create the request parameters.
        translate_endpoint = 'translate'
        params = {
            "auth_key": self.api_key,
            "target_lang": self._map_language_to_code(target),
            "source_lang": self._map_language_to_code(source),
            "text": text
        }
        # Do the request and check the connection.
        try:
            response = requests.get(self.__base_url + translate_endpoint, params=params)
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

    def translate_batch(self, source, target, batch):
        """
        translate a batch of texts
        @param source: source language
        @param target: target language
        @param batch: list of texts to translate
        @return: list of translations
        """
        return [self.translate(source, target, text) for text in batch]

    def _is_language_supported(self, lang):
        # The language is supported when is in the dicionary.
        return lang == 'auto' or lang in self._languages.keys() or lang in self._languages.values()

    def _map_language_to_code(self, lang):
        if lang in self._languages.keys():
            return self._languages[lang]
        elif lang in self._languages.values():
            return lang
        raise LanguageNotSupportedException(lang)
