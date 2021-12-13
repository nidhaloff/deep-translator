"""
LibreTranslate API
"""

import requests
from bs4 import BeautifulSoup
from requests.models import Response
from .parent import BaseTranslator
from .constants import BASE_URLS,LIBRE_LANGUAGES_TO_CODES, LIBRE_CODES_TO_LANGUAGES
from .exceptions import (ServerException,
                        TranslationNotFound,
                        LanguageNotSupportedException,
                        AuthorizationException)


class LibreTranslator(BaseTranslator):
    """
    class that wraps functions, which use libre translator under the hood to translate text(s)
    """
    _languages = LIBRE_LANGUAGES_TO_CODES
    supported_languages = list(_languages.keys())

    def __init__(self, base_url = BASE_URLS.get("LIBRE_FREE"), api_key="", source="auto", target="en", **kwargs):
        """
        @param source: source language to translate from
        List of LibreTranslate nedpoints can be found at : https://github.com/LibreTranslate/LibreTranslate#mirrors
        Some require an API key
        @param target: target language to translate to
        """
        if base_url == BASE_URLS.get("LIBRE") and not api_key:
            raise ServerException(401)
        self.__base_url = base_url
        self.api_key = api_key
        self.source = self._map_language_to_code(source)
        self.target = self._map_language_to_code(target)


    @staticmethod
    def get_supported_languages(as_dict=False, **kwargs):
        """
        return the supported languages by the libre translator
        @param as_dict: if True, the languages will be returned as a dictionary mapping languages to their abbreviations
        @return: list or dict
        """
        return [*LibreTranslator._languages.keys()] if not as_dict else LibreTranslator._languages
    
    def _map_language_to_code(self, language, **kwargs):
        """
        map language to its corresponding code (abbreviation) if the language was passed by its full name by the user
        @param language: a string for 1 language
        @return: mapped value of the language or raise an exception if the language is not supported
        """
        if language in self._languages.keys():
            return self._languages[language]
        elif language in self._languages.values():
            return language
        raise LanguageNotSupportedException(language)
    
    def _is_language_supported(self, language, **kwargs):
        """
        check if the language is supported by the translator
        @param language: a string for 1 language
        @return: bool or raise an Exception
        """
        return language == 'auto' or language in self._languages.keys() or language in self._languages.values()
    
    def translate(self, text, **kwargs):
        """
        function that uses microsoft translate to translate a text
        @param text: desired text to translate
        @return: str: translated text
        """
         # Create the request parameters.
        translate_endpoint = 'translate'
        params = {
            "q": text,
            "source": self.source,
            "target": self.target,
            "api_key": self.api_key
        }
        # Do the request and check the connection.
        try:
            response = requests.post(self.__base_url + translate_endpoint, params=params)
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
        return res['translatedText']
    
