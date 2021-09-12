"""
Pons Translator API
"""
from bs4 import BeautifulSoup
import requests
from .constants import BASE_URLS, PONS_LANGUAGES_TO_CODES, PONS_CODES_TO_LANGUAGES
from .exceptions import (LanguageNotSupportedException,
                         TranslationNotFound,
                         NotValidPayload,
                         ElementNotFoundInGetRequest,
                         RequestError,
                         TooManyRequests)
from .parent import BaseTranslator
from requests.utils import requote_uri


class PonsTranslator(BaseTranslator):
    """
    Class that uses PONS translator to translate words
    """
    _languages = PONS_LANGUAGES_TO_CODES
    supported_languages = list(_languages.keys())

    def __init__(self, source, target="en", proxies=None, **_):
        """
        Args:
            source: str: source language to translate from.
            target: str: target language to translate to.
            proxies
        """
        self.__base_url = BASE_URLS.get("PONS")
        self.proxies = proxies
        if self.is_language_supported(source, target):
            self._source, self._target = self._map_language_to_code(source, target)

        super().__init__(base_url=self.__base_url,
                         source=self._source,
                         target=self._target,
                         payload_key=None,
                         element_tag='div',
                         element_query={"class": "target"}
                         )

    @staticmethod
    def get_supported_languages(as_dict=False, **_):
        """
        Return the supported languages by the google translator
        Args:
            as_dict: bool: if True, the languages will be returned as a dictionary mapping languages to their abbreviations
        Returns:
            list or dict
        """
        return PonsTranslator.supported_languages if not as_dict else PonsTranslator._languages

    def _map_language_to_code(self, *languages, **_):
        """
        Map language to its corresponding code (abbreviation) if the language was passed by its full name by the user.
        Args:
            languages: list of languages.
        Yields:
            str
        Raises:
            Exception if the language is not supported.
        Examples:
            PonsTranslatorObject._map_language_to_code("ko", "uk", "en")
        """
        for language in languages:
            if language in self._languages.values():
                yield PONS_CODES_TO_LANGUAGES[language]
            elif language in self._languages.keys():
                yield language
            else:
                raise LanguageNotSupportedException(language)

    def is_language_supported(self, *languages, **_):
        """
        Check if the language is supported by the translator
        Args:
            languages: list of languages.
        Returns:
            True
        Raises
            LanguageNotSupportedException
        Examples:
            PonsTranslatorObject.is_language_supported("ko", "uk", "en")
        """

        all_supported_languages = [*self._languages.keys(), *self._languages.values()]

        for lang in languages:
            if lang not in all_supported_languages:
                raise LanguageNotSupportedException(lang)
        return True

    def translate(self, word, return_all=False, **kwargs):
        """
        Function that uses Pons translator to translate a word
        Args:
            word: str: word to translate.
            return_all: bool: set to True to return all synonym/similar of the translated text
        Keyword Args:
            requests_kwargs: arbitrary args for requests.get.
        Returns:
             str or list or None
        Raises:
            TooManyRequests
            RequestError
            ElementNotFoundInGetRequest
            TranslationNotFound
        """
        if self._validate_payload(word, max_chars=50):
            url = "{}{}-{}/{}".format(self.__base_url, self._source, self._target, word)
            url = requote_uri(url)
            response = requests.get(url, proxies=self.proxies, **kwargs.get("requests_kwargs", {}))

            if response.status_code == 429:
                raise TooManyRequests()

            if response.status_code != 200:
                raise RequestError()

            soup = BeautifulSoup(response.text, 'html.parser')
            elements = soup.findAll(self._element_tag, self._element_query)

            if not elements:
                raise ElementNotFoundInGetRequest(word)

            filtered_elements = []
            for el in elements:
                temp = ''
                for e in el.findAll('a'):
                    if e.parent.name == 'div':
                        if e and "/translate/{}-{}/".format(self._target, self._source) in e.get('href'):
                            temp += e.get_text() + ' '
                filtered_elements.append(temp)

            if not filtered_elements:
                raise ElementNotFoundInGetRequest(word)

            word_list = [word for word in filtered_elements if word and len(word) > 1]

            if not word_list:
                raise TranslationNotFound(word)

            return word_list if return_all else word_list[0]

    def translate_words(self, words, **kwargs):
        """
        Translate a batch of words together by providing them in a list
        Args:
            words: list: list of texts to translate.
            kwargs: dict: dict of arg for PonsTranslatorObject.translate
        Returns:
             list of translations
        Raises:
            NotValidPayload
        """
        if not words:
            raise NotValidPayload(words)

        translated_words = []
        for word in words:
            translated_words.append(self.translate(word=word, **kwargs))
        return translated_words
