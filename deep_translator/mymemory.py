"""
MyMemory Translator API
"""
import logging
import warnings

from .constants import BASE_URLS, GOOGLE_LANGUAGES_TO_CODES
from .exceptions import (NotValidPayload,
                         TranslationNotFound,
                         LanguageNotSupportedException,
                         RequestError,
                         TooManyRequests)
from .parent import BaseTranslator
import requests
from time import sleep


class MyMemoryTranslator(BaseTranslator):
    """
    Class that uses the MyMemory translator to translate texts
    """
    _languages = GOOGLE_LANGUAGES_TO_CODES
    supported_languages = list(_languages.keys())

    def __init__(self, source="auto", target="en", proxies=None, **kwargs):
        """
        Args:
            source: str: source language to translate from.
            target: str: target language to translate to.
            proxies
        """
        self.__base_url = BASE_URLS.get("MYMEMORY")
        self.proxies = proxies
        if self.is_language_supported(source, target):
            self._source, self._target = self._map_language_to_code(source.lower(), target.lower())
            self._source = self._source if self._source != 'auto' else 'Lao'

        self.email = kwargs.get('email', None)
        super(MyMemoryTranslator, self).__init__(base_url=self.__base_url,
                                                 source=self._source,
                                                 target=self._target,
                                                 payload_key='q',
                                                 langpair='{}|{}'.format(self._source, self._target))

    @staticmethod
    def get_supported_languages(as_dict=False, **_):
        """
        Return the supported languages by the google translator
        Args:
            as_dict: bool: if True, the languages will be returned as a dictionary mapping languages to their abbreviations
        Returns:
            list or dict
        """
        return MyMemoryTranslator.supported_languages if not as_dict else MyMemoryTranslator._languages

    def _map_language_to_code(self, *languages):
        """
        Map language to its corresponding code (abbreviation) if the language was passed by its full name by the user.
        Args:
            languages: list of languages.
        Yields:
            str
        Raises:
            Exception if the language is not supported.
        Examples:
            MyMemoryTranslatorObject._map_language_to_code("ko", "uk", "en")
        """
        for language in languages:
            if language in self._languages.values() or language == 'auto':
                yield language
            elif language in self._languages.keys():
                yield self._languages[language]
            else:
                raise LanguageNotSupportedException(language)

    def is_language_supported(self, *languages):
        """
        Check if the language is supported by the translator
        Args:
            languages: list of languages.
        Returns:
            True
        Raises
            LanguageNotSupportedException
        Examples:
            MyMemoryTranslatorObject.is_language_supported("ko", "uk", "en")
        """

        all_supported_languages = [*self._languages.keys(), *self._languages.values()]
        for lang in languages:
            if lang != 'auto' and lang not in all_supported_languages:
                raise LanguageNotSupportedException(lang)
        return True

    def translate(self, text, return_all=False, **kwargs):
        """
        Function that uses MyMemory translator to translate a word
        Args:
            text: str: text to translate.
            return_all: bool: set to True to return all synonym/similars of the translated text
        Keyword Args:
            requests_kwargs: arbitrary args for requests.get.
        Returns:
             str or list or None
        Raises:
            TooManyRequests
            RequestError
            TranslationNotFound
        """

        if self._validate_payload(text, max_chars=500):
            text = text.strip()

            if self.payload_key:
                self._url_params[self.payload_key] = text
            if self.email:
                self._url_params['de'] = self.email

            response = requests.get(self.__base_url,
                                    params=self._url_params,
                                    headers=self.headers,
                                    proxies=self.proxies,
                                    **kwargs.get("requests_kwargs", {}))

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

    def translate_sentences(self, sentences=None, **kwargs):
        """
        Translate many sentences together. This makes sense if you have sentences with different languages
        and you want to translate all to unified language. This is handy because it detects
        automatically the language of each sentence and then translate it.

        Args:
            sentences: list of str: list of sentences to translate.
        Returns:
             list of all translated sentences.
        Raises:
            NotValidPayload
            Exception
        """
        warn_msg = "deprecated. Use the translate_batch function instead"
        warnings.warn(warn_msg, DeprecationWarning, stacklevel=2)
        logging.warning(warn_msg)
        if not sentences:
            raise NotValidPayload(sentences)

        translated_sentences = []
        try:
            for sentence in sentences:
                translated = self.translate(text=sentence, **kwargs)
                translated_sentences.append(translated)

            return translated_sentences

        except Exception as e:
            raise e

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
            return self.translate(text=text)
        except Exception as e:
            raise e

    def translate_batch(self, batch=None, **kwargs):
        """
        Translate a list of texts
        Args:
            batch: list: list of texts to translate.
            kwargs: dict: arbitrary args for MyMemoryTranslatorObject.translate
        Returns:
             list of translations
        Raises:
            Exception
        """
        if not batch:
            raise Exception("Enter your text list that you want to translate")

        arr = []
        for text in batch:
            translated = self.translate(text, **kwargs)
            arr.append(translated)
            sleep(2)

        return arr
