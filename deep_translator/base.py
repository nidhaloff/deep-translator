"""base translator class"""

from .constants import GOOGLE_LANGUAGES_TO_CODES
from abc import ABC, abstractmethod


class BaseTranslator(ABC):
    """
    Abstract class that serve as a base translator for other different translators
    """
    def __init__(self,
                 base_url=None,
                 source="auto",
                 target="en",
                 payload_key=None,
                 element_tag=None,
                 element_query=None,
                 languages=None,
                 **url_params):
        """
        @param source: source language to translate from
        @param target: target language to translate to
        """
        self._base_url = base_url
        self.languages: dict = GOOGLE_LANGUAGES_TO_CODES if not languages else languages
        self.supported_languages: list = list(self.languages.keys())
        self._source, self._target = self._map_language_to_code(source, target)
        self._url_params = url_params
        self._element_tag = element_tag
        self._element_query = element_query
        self.payload_key = payload_key
        super().__init__()

    def _type(self):
        return self.__class__.__name__

    def _map_language_to_code(self, *languages):
        """
        map language to its corresponding code (abbreviation) if the language was passed by its full name by the user
        @param languages: list of languages
        @return: mapped value of the language or raise an exception if the language is not supported
        """
        for language in languages:
            if language in self.languages.values() or language == 'auto':
                yield language
            elif language in self.languages.keys():
                yield self.languages[language]

    def _same_source_target(self):
        return self._source == self._target

    def get_supported_languages(self, as_dict=False, **kwargs):
        """
        return the supported languages by the google translator
        @param as_dict: if True, the languages will be returned as a dictionary mapping languages to their abbreviations
        @return: list or dict
        """
        return self.supported_languages if not as_dict else self.languages

    def is_language_supported(self, language, **kwargs):
        """
        check if the language is supported by the translator
        @param language: a string for 1 language
        @return: bool or raise an Exception
        """
        if language == 'auto' or language in self.languages.keys() or language in self.languages.values():
            return True
        else:
            return False

    @abstractmethod
    def translate(self, text, **kwargs):
        """
        translate a text using a translator under the hood and return the translated text
        @param text: text to translate
        @param kwargs: additional arguments
        @return: str
        """
        return NotImplemented('You need to implement the translate method!')

    def _translate_file(self, path, **kwargs):
        """
        translate directly from file
        @param path: path to the target file
        @type path: str
        @param kwargs: additional args
        @return: str
        """
        try:
            with open(path, 'r', encoding='utf-8') as f:
                text = f.read().strip()
            return self.translate(text)
        except Exception as e:
            raise e

    def _translate_batch(self, batch=None, **kwargs):
        """
        translate a list of texts
        @param batch: list of texts you want to translate
        @return: list of translations
        """
        if not batch:
            raise Exception("Enter your text list that you want to translate")
        arr = []
        for i, text in enumerate(batch):
            translated = self.translate(text, **kwargs)
            arr.append(translated)
        return arr
