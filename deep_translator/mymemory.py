"""
mymemory translator API
"""
from .validate import is_empty, validate_input
from .constants import BASE_URLS
from .exceptions import (
                        TranslationNotFound,
                        RequestError,
                        TooManyRequests)
from .base import BaseTranslator
import requests


class MyMemoryTranslator(BaseTranslator):
    """
    class that uses the mymemory translator to translate texts
    """
    def __init__(self, source="auto", target="en", proxies=None, **kwargs):
        """
        @param source: source language to translate from
        @param target: target language to translate to
        """
        self.proxies = proxies
        self.email = kwargs.get('email', None)
        super().__init__(base_url=BASE_URLS.get("MYMEMORY"),
                         source=source,
                         target=target,
                         payload_key='q',
                        )

    def translate(self, text, return_all=False, **kwargs):
        """
        function that uses the mymemory translator to translate a text
        @param text: desired text to translate
        @type text: str
        @param return_all: set to True to return all synonym/similars of the translated text
        @return: str or list
        """
        if validate_input(text, max_chars=500):
            text = text.strip()
            if self._same_source_target() or is_empty(text):
                return text

            self._url_params['langpair'] = '{}|{}'.format(self._source, self._target)
            if self.payload_key:
                self._url_params[self.payload_key] = text
            if self.email:
                self._url_params['de'] = self.email

            response = requests.get(self._base_url,
                                    params=self._url_params,
                                    proxies=self.proxies)

            if response.status_code == 429:
                raise TooManyRequests()
            if response.status_code != 200:
                raise RequestError()

            data = response.json()
            if not data:
                TranslationNotFound(text)

            translation = data.get('responseData').get('translatedText')
            if translation:
                return translation

            elif not translation:
                all_matches = data.get('matches')
                matches = (match['translation'] for match in all_matches)
                next_match = next(matches)
                return next_match if not return_all else list(all_matches)

    def translate_file(self, path, **kwargs):
        """
         translate directly from file
         @param path: path to the target file
         @type path: str
         @param kwargs: additional args
         @return: str
         """
        return self._translate_file(path, **kwargs)

    def translate_batch(self, batch=None, **kwargs):
        """
        translate a list of texts
        @param batch: list of texts you want to translate
        @return: list of translations
        """
        return self._translate_batch(batch, **kwargs)
