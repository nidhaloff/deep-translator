"""
LibreTranslate API
"""

from requests.models import Response
from .parent import BaseTranslator
import requests
from bs4 import BeautifulSoup
from .constants import LIBRE_LANGUAGES_TO_CODES, LIBRE_CODES_TO_LANGUAGES


class LibreTranslator(BaseTranslator):
    """
    class that wraps functions, which use libre translator under the hood to translate text(s)
    """

    def __init__(self, base_url, api_key, source="auto", target="en", proxies=None, **kwargs):
        """
        @param source: source language to translate from
        @param target: target language to translate to
        """
        _languages = LIBRE_LANGUAGES_TO_CODES
        supported_languages = list(_languages.keys())
        return None
    
    @staticmethod
    def get_supported_languages(as_dict=False, **kwargs):
        """
        return the supported languages by the libre translator
        @param as_dict: if True, the languages will be returned as a dictionary mapping languages to their abbreviations
        @return: list or dict
        """
        return None
    
    def _map_language_to_code(self, *languages):
        """
        map language to its corresponding code (abbreviation) if the language was passed by its full name by the user
        @param languages: list of languages
        @return: mapped value of the language or raise an exception if the language is not supported
        """
        return None
    
    def is_language_supported(self, language, **kwargs):
        """
        check if the language is supported by the translator
        @param language: a string (if 1 lang) or a list (if multiple langs)
        @return: bool or raise an Exception
        """
    
    def translate(self, text, **kwargs):
        """
        function that uses microsoft translate to translate a text
        @param text: desired text to translate
        @return: str: translated text
        """
        return None
    
response = requests.post("https://libretranslate.de/detect",data={'q': 'bonjour'})
soup = BeautifulSoup(response.text, 'html.parser')
print(soup)