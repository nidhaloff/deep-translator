"""
Google Translator API
"""

from .constants import BASE_URLS, GOOGLE_LANGUAGES_TO_CODES, GOOGLE_LANGUAGES_SECONDARY_NAMES
from .exceptions import TooManyRequests, LanguageNotSupportedException, TranslationNotFound, NotValidPayload, \
    RequestError
from .parent import BaseTranslator
from bs4 import BeautifulSoup
import requests
from time import sleep
import warnings
import logging


class GoogleTranslator(BaseTranslator):
    """
    Class that wraps functions, which use google translate under the hood to translate text(s)
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
        self.__base_url = BASE_URLS.get("GOOGLE_TRANSLATE")
        self.proxies = proxies

        # code snippet that converts the language into lower-case and skip lower-case conversion for abbreviations
        # since abbreviations like zh-CN if converted to lower-case will result into error
        #######################################
        source_lower = source
        target_lower = target
        if source not in self._languages.values():
            source_lower = source.lower()
        if target not in self._languages.values():
            target_lower = target.lower()
        #######################################

        if self.is_language_supported(source_lower, target_lower):
            self._source, self._target = self._map_language_to_code(source_lower, target_lower)

        super(GoogleTranslator, self).__init__(base_url=self.__base_url,
                                               source=self._source,
                                               target=self._target,
                                               element_tag='div',
                                               element_query={"class": "t0"},
                                               payload_key='q',  # key of text in the url
                                               tl=self._target,
                                               sl=self._source,
                                               **kwargs)

        self._alt_element_query = {"class": "result-container"}

    @staticmethod
    def get_supported_languages(as_dict=False, **_):
        """
        Return the supported languages by the google translator
        Args:
            as_dict: bool: if True, the languages will be returned as a dictionary mapping languages to their abbreviations
        Returns:
            list or dict
        """
        return GoogleTranslator.supported_languages if not as_dict else GoogleTranslator._languages

    @staticmethod
    def is_secondary(lang):
        """
        Function to check if lang is a secondary name of any primary language
        Args:
            lang: str: language name
        Returns:
            False or str
        """
        for primary_name, secondary_names in GOOGLE_LANGUAGES_SECONDARY_NAMES.items():
            if lang in secondary_names:
                return primary_name
        return False

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
            GoogleTranslatorObject._map_language_to_code("ko", "uk", "en")
        """

        for language in languages:
            if language in self._languages.values() or language == 'auto':
                yield language
            elif language in self._languages.keys():
                yield self._languages[language]
            else:
                yield self._languages[self.is_secondary(language)]

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
            GoogleTranslatorObject.is_language_supported("ko", "uk", "en")
        """

        all_supported_languages = [*self._languages.keys(), * self._languages.values()]

        for lang in languages:
            if lang != 'auto' and lang not in all_supported_languages:
                if self.is_secondary(lang) is False:
                    raise LanguageNotSupportedException(lang)
        return True

    def translate(self, text, **kwargs):
        """
        Function that uses Google Translate to translate a word
        Args:
            text: str: text to translate.
        Keyword Args:
            requests_kwargs: arbitrary args for requests.get.
        Returns:
             str: translated text.
        Raises:
            TooManyRequests
            RequestError
            TranslationNotFound
        """

        if self._validate_payload(text):
            text = text.strip()

            if self.payload_key:
                self._url_params[self.payload_key] = text

            response = requests.get(self.__base_url,
                                    params=self._url_params,
                                    proxies=self.proxies,
                                    **kwargs.get("requests_kwargs", {}))
            if response.status_code == 429:
                raise TooManyRequests()

            if response.status_code != 200:
                raise RequestError()

            soup = BeautifulSoup(response.text, 'html.parser')

            element = soup.find(self._element_tag, self._element_query)

            if not element:
                element = soup.find(self._element_tag, self._alt_element_query)
                if not element:
                    raise TranslationNotFound(text)
            if element.get_text(strip=True) == text.strip():
                to_translate_alpha = ''.join(ch for ch in text.strip() if ch.isalnum())
                translated_alpha = ''.join(ch for ch in element.get_text(strip=True) if ch.isalnum())
                if to_translate_alpha and translated_alpha and to_translate_alpha == translated_alpha:
                    self._url_params["tl"] = self._target
                    if "hl" not in self._url_params:
                        return text.strip()
                    del self._url_params["hl"]
                    return self.translate(text)

            else:
                return element.get_text(strip=True)

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

    def translate_sentences(self, sentences=None, **_):
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
        warnings.warn("deprecated. Use the translate_batch function instead", DeprecationWarning, stacklevel=2)
        logging.warning("deprecated. Use the translate_batch function instead")
        if not sentences:
            raise NotValidPayload(sentences)

        translated_sentences = []
        try:
            for sentence in sentences:
                translated = self.translate(text=sentence)
                translated_sentences.append(translated)

            return translated_sentences

        except Exception as e:
            raise e

    def translate_batch(self, batch=None, **kwargs):
        """
        Translate a list of texts
        Args:
            batch: list: list of texts to translate.
            kwargs: dict: arbitrary args for GoogleTranslatorObject.translate
        Returns:
             list of translations
        Raises:
            Exception
        """
        if not batch:
            raise Exception("Enter your text list that you want to translate")

        print("Please wait.. This may take a couple of seconds because deep_translator sleeps "
              "for two seconds after each request in order to not spam the google server.")
        arr = []
        for i, text in enumerate(batch):
            translated = self.translate(text, **kwargs)
            arr.append(translated)
            print("sentence number ", i + 1, " has been translated successfully")
            sleep(2)

        return arr


if __name__ == '__main__':
    translator = GoogleTranslator(source='ru', target='uk')
    t = translator.translate("Я разработчик")  # => "I am a developer"
    print(t)
