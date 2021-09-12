"""
DeepL Translator API
"""
import requests
from .constants import BASE_URLS, DEEPL_LANGUAGE_TO_CODE
from .exceptions import (ServerException,
                         TranslationNotFound,
                         LanguageNotSupportedException,
                         AuthorizationException)


class DeepL(object):
    """
    class that wraps functions, which use the DeepL translator under the hood to translate word(s)
    """
    _languages = DEEPL_LANGUAGE_TO_CODE

    def __init__(self, api_key=None, source="en", target="en", use_free_api=True, **_):
        """
        Args:
            api_key: str: your DeepL api key, get one here https://www.deepl.com/docs-api/accessing-the-api/.
            source: str: source language to translate from.
            target: str: target language to translate to.
            use_free_api: bool: set to True if you are using a free api key.
        Raises:
            ServerException
        """
        if not api_key:
            raise ServerException(401)
        self.version = 'v2'
        self.api_key = api_key
        self.source = self._map_language_to_code(source)
        self.target = self._map_language_to_code(target)
        if use_free_api:
            self.__base_url = BASE_URLS.get("DEEPL_FREE").format(version=self.version)
        else:
            self.__base_url = BASE_URLS.get("DEEPL").format(version=self.version)

    def translate(self, text, **kwargs):
        """
        Function that uses DeepL to translate a word
        Args:
            text: str: word to translate.
        Keyword Args:
            requests_kwargs: arbitrary args for requests.get.
        Returns:
             str: translated text.
        Raises:
            ServerException
            AuthorizationException
            TranslationNotFound
        """
        # Create the request parameters.
        translate_endpoint = 'translate'
        params = {
            "auth_key": self.api_key,
            "source_lang": self.source,
            "target_lang": self.target,
            "text": text
        }
        # Do the request and check the connection.
        try:
            response = requests.get(self.__base_url + translate_endpoint, params=params,
                                    **kwargs.get("requests_kwargs", {}))
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

    def translate_batch(self, batch, **kwargs):
        """
        Args:
            batch: list: list of texts to translate.
            kwargs: dict: arbitrary args for DeepLObject.translate
        Returns:
             list of translations
        """
        return [self.translate(text, **kwargs) for text in batch]

    @staticmethod
    def get_supported_languages(as_dict=False, **_):
        return [*DeepL._languages.keys()] if not as_dict else DeepL._languages

    def _is_language_supported(self, lang, **_):
        # The language is supported when is in the dictionary.
        return lang == 'auto' or lang in self._languages.keys() or lang in self._languages.values()

    def _map_language_to_code(self, lang, **_):
        if lang in self._languages.keys():
            return self._languages[lang]
        elif lang in self._languages.values():
            return lang
        raise LanguageNotSupportedException(lang)


if __name__ == '__main__':
    d = DeepL(target="de")
    t = d.translate("I have no idea")
    print("text: ", t)
