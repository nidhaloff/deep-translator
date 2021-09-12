"""
Microsoft Translator API
"""

# -*- coding: utf-8 -*-

import requests
import logging
import sys

from .constants import BASE_URLS, MICROSOFT_CODES_TO_LANGUAGES
from .exceptions import LanguageNotSupportedException, ServerException, MicrosoftAPIerror


class MicrosoftTranslator:
    """
    The class that wraps functions, which use the Microsoft translator under the hood to translate word(s)
    """

    _languages = MICROSOFT_CODES_TO_LANGUAGES
    supported_languages = list(_languages.values())

    def __init__(self, api_key=None, region=None, source=None, target=None, proxies=None, **kwargs):
        """
        Args:
            api_key: str: your Microsoft API key.
            region: str: your Microsoft Location.
            source: str: source language to translate from.
            target: str: target language to translate to.
            kwargs: arbitrary args.
            proxies
        """
        if not api_key:
            raise ServerException(401)
        else:
            self.api_key = api_key

        self.proxies = proxies
        self.headers = {
            "Ocp-Apim-Subscription-Key": self.api_key,
            "Content-type": "application/json",
        }
        # region is not required but very common and goes to headers if passed
        if region:
            self.region = region
            self.headers["Ocp-Apim-Subscription-Region"] = self.region

        if not target:
            raise ServerException(401)
        else:
            if type(target) is str:
                self.target = target.lower()
            else:
                self.target = [i.lower() for i in target]
            if self.is_language_supported(self.target):
                self.target = self._map_language_to_code(self.target)

        self.url_params = {'to': self.target, **kwargs}

        if source:
            self.source = source.lower()
            if self.is_language_supported(self.source):
                self.source = self._map_language_to_code(self.source)
            self.url_params['from'] = self.source

        self.__base_url = BASE_URLS.get("MICROSOFT_TRANSLATE")

    @staticmethod
    def get_supported_languages(as_dict=False, **_):
        """
        Return the supported languages by the Microsoft translator
        Args:
            as_dict: bool: if True, the languages will be returned as a dictionary mapping languages to their abbreviations
        Returns:
            list or dict
        """
        return MicrosoftTranslator.supported_languages if not as_dict else MicrosoftTranslator._languages

    def _map_language_to_code(self, language, **_):
        """
        Map language to its corresponding code (abbreviation) if the language was passed by its full name by the user.
        Args:
            language: list or str
        Yields:
            str
        Raises:
            LanguageNotSupportedException
        """
        if isinstance(language, str):
            language = [language]
        for lang in language:
            if lang in self._languages.values():
                yield lang
            elif lang in self._languages.keys():
                yield self._languages[lang]
            else:
                raise LanguageNotSupportedException(lang)

    def is_language_supported(self, language, **_):
        """
        Check if the language is supported by the translator
        Args:
            language: list or str
        Returns:
            True
        Raises:
            LanguageNotSupportedException
        """
        if type(language) is str:
            language = [language]
        all_supported_languages = [*self._languages.keys(), * self._languages.values()]
        for lang in language:
            if lang not in all_supported_languages:
                raise LanguageNotSupportedException(lang)
        return True

    def translate(self, text, **kwargs):
        """
        Function that uses microsoft translate to translate a text
        Args:
            text: str: desired text to translate.
        Keyword Args:
            requests_kwargs: arbitrary args for requests.get.
        Returns:
            str: translated text.
        Raises:
            MicrosoftAPIerror
        """
        # a body must be a list of dicts to process multiple texts;
        # I have not added multiple text processing here since it is covered by the translate_batch method
        valid_microsoft_json = [{'text': text}]
        try:
            requested = requests.post(self.__base_url,
                                      params=self.url_params,
                                      headers=self.headers,
                                      json=valid_microsoft_json,
                                      proxies=self.proxies,
                                      **kwargs.get("requests_kwargs", {}))
        except requests.exceptions.RequestException:
            exc_type, value, traceback = sys.exc_info()
            logging.warning(f"Returned error: {exc_type.__name__}")

        # Where Microsoft API responds with an api error, it returns a dict in response.json()
        if isinstance(requested.json(), dict):
            error_message = requested.json()['error']
            raise MicrosoftAPIerror(error_message)
        # Where it responds with a translation, its response.json() is a list e.g. [{'translations': [{'text': 'Hello world!', 'to': 'en'}]}]
        elif isinstance(requested.json(), list):
            all_translations = [i['text'] for i in requested.json()[0]['translations']]
            return "\n".join(all_translations)

    def translate_file(self, path, **_):
        """
        Translate directly from file
        Args:
             path: str: path to the target file.
        Returns:
            str
        Raises:
            Exception
        """
        try:
            with open(path) as f:
                text = f.read().strip()
            return self.translate(text)
        except Exception as e:
            raise e

    def translate_batch(self, batch, **kwargs):
        """
        translate a list of texts
        Args:
            batch: list: list of texts to translate.
            kwargs: dict: arbitrary args for MicrosoftTranslatorObject.translate
        Returns:
             list of translations
        """
        return [self.translate(text, **kwargs) for text in batch]
