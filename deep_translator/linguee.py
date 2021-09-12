"""
Linguee Translator API
"""

from deep_translator.constants import BASE_URLS, LINGUEE_LANGUAGES_TO_CODES, LINGUEE_CODE_TO_LANGUAGE
from deep_translator.exceptions import (LanguageNotSupportedException,
                                        TranslationNotFound,
                                        NotValidPayload,
                                        ElementNotFoundInGetRequest,
                                        RequestError,
                                        TooManyRequests)
from deep_translator.parent import BaseTranslator
from bs4 import BeautifulSoup
import requests
from requests.utils import requote_uri


class LingueeTranslator(BaseTranslator):
    """
    Class that wraps functions, which use the linguee translator under the hood to translate word(s)
    """
    _languages = LINGUEE_LANGUAGES_TO_CODES
    supported_languages = list(_languages.keys())

    def __init__(self, source, target="en", proxies=None, **_):
        """
        Args:
            source: str: source language to translate from.
            target: str: target language to translate to.
            proxies
        """
        self.__base_url = BASE_URLS.get("LINGUEE")
        self.proxies = proxies

        if self.is_language_supported(source, target):
            self._source, self._target = self._map_language_to_code(source.lower(), target.lower())

        super().__init__(base_url=self.__base_url,
                         source=self._source,
                         target=self._target,
                         element_tag='a',
                         element_query={'class': 'dictLink featured'},
                         payload_key=None,  # key of text in the url
                         )

    @staticmethod
    def get_supported_languages(as_dict=False, **_):
        """
        return the supported languages by the linguee translator
        Args:
            as_dict: bool: if True, the languages will be returned as a dictionary mapping languages to their abbreviations.
        Returns:
            list or dict
        """
        return LingueeTranslator.supported_languages if not as_dict else LingueeTranslator._languages

    def _map_language_to_code(self, *languages, **_):
        """
        Map language to its corresponding code (abbreviation) if the language was passed by its full name by the user
        Args:
            languages: list of str: list of languages.
        Yields:
            str: language
        Raises:
            LanguageNotSupportedException
        """
        for language in languages:
            if language in self._languages.values():
                yield LINGUEE_CODE_TO_LANGUAGE[language]
            elif language in self._languages.keys():
                yield language
            else:
                raise LanguageNotSupportedException(language)

    def is_language_supported(self, *languages, **_):
        """
        Check if the language is supported by the translator
        Args:
            languages: list of str: list of languages.
        Returns:
             True
        Raises:
            LanguageNotSupportedException
        Examples:
            LingueeTranslatorObject.is_language_supported("ko", "uk", "en")
        """
        allSupportedLanguages = {*self._languages.values(), *self._languages.keys()}
        for lang in languages:
            if lang not in allSupportedLanguages:
                raise LanguageNotSupportedException(lang)
        return True

    def translate(self, word, return_all=False, **kwargs):
        """
        Function that uses linguee to translate a word
        Args:
            word: str: word to translate.
            return_all: bool: set to True to return all synonym of the translated word.
        Keyword Args:
            requests_kwargs: arbitrary args for requests.get.
        Returns:
             str: translated word
        """
        if self._validate_payload(word, max_chars=50):
            # %s-%s/translation/%s.html
            url = "{}{}-{}/translation/{}.html".format(self.__base_url, self._source, self._target, word)
            url = requote_uri(url)
            response = requests.get(url, proxies=self.proxies, **kwargs.get("requests_kwargs"))

            if response.status_code == 429:
                raise TooManyRequests()

            if response.status_code != 200:
                raise RequestError()
            soup = BeautifulSoup(response.text, 'html.parser')
            elements = soup.find_all(self._element_tag, self._element_query)
            if not elements:
                raise ElementNotFoundInGetRequest(elements)

            filtered_elements = []
            for el in elements:
                try:
                    pronoun = el.find('span', {'class': 'placeholder'}).get_text(strip=True)
                except AttributeError:
                    pronoun = ''
                filtered_elements.append(el.get_text(strip=True).replace(pronoun, ''))

            if not filtered_elements:
                raise TranslationNotFound(word)

            return filtered_elements if return_all else filtered_elements[0]

    def translate_words(self, words, **kwargs):
        """
        Translate a batch of words together by providing them in a list
        Args:
            words: list of str: list of words you want to translate.
            kwargs: dict: additional args for LingueeTranslatorObject.translate.
        Returns:
            list of translated words
        """
        if not words:
            raise NotValidPayload(words)

        translated_words = []
        for word in words:
            translated_words.append(self.translate(word=word, **kwargs))
        return translated_words
