"""Main module."""


from bs4 import BeautifulSoup
import requests
from models import BaseTranslator
from constants import  LANGUAGES_TO_CODES
from exceptions import LanguageNotSupportedException, NotValidPayload, ElementNotFoundInGetRequest, NotValidLength


class ParentTranslator(BaseTranslator):
    """
    class that serve as a parent translator class for other different translators
    """
    def __init__(self,
                 base_url=None,
                 source="auto",
                 target="en",
                 element_tag=None,
                 element_query=None,
                 **url_params):
        """
        @param source: source language to translate from
        @param target: target language to translate to
        """
        self.__base_url = base_url
        self._source = source
        self._target = target
        self._url_params = url_params
        self._element_tag = element_tag
        self._element_query = element_query
        super(ParentTranslator, self).__init__()

    def _validate_payload(self, payload):
        """
        validate the payload text to translate
        @param payload: text to translate
        @return: bool
        """
        if not payload or not isinstance(payload, str):
            return False

        return True

    def _check_length(self, payload, min_chars=0, max_chars=5000):
        return True if min_chars < len(payload) < max_chars else False

    def _validate_languages(self, languages):
        """

        @param languages: languages to validate
        @return: True or raise an exception
        """
        for lang in languages:
            if lang != 'auto' and lang not in LANGUAGES_TO_CODES.keys():
                if lang != 'auto' and lang not in LANGUAGES_TO_CODES.values():
                    raise LanguageNotSupportedException(lang)
        return True

    def translate(self, payload, payload_tag):
        """
        main function that uses google translate to translate a text
        @param payload: desired text to translate
        @param payload_tag: tag of the payload in the url parameters
        @return: str: translated text
        """

        if not self._validate_payload(payload):
            raise NotValidPayload(payload)

        if not self._check_length(payload):
            raise NotValidLength(payload)

        try:
            payload = payload.strip()

            if payload_tag in self._url_params.keys():
                self._url_params[payload_tag] = payload

            res = requests.get(self.__base_url, params=self._url_params)
            soup = BeautifulSoup(res.text, 'html.parser')
            element = soup.find(self._element_tag, self._element_query)
            if not element:
                raise ElementNotFoundInGetRequest(element)

            return element.get_text(strip=True)

        except Exception as e:
            print(e.args)
            raise

    def translate_file(self, path):
        try:
            with open(path) as f:
                text = f.read()

            return self.translate(payload=text)
        except Exception as e:
            raise e

    def translate_sentences(self, sentences=None):
        """
        translate many sentences together. This makes sense if you have sentences with different languages
        and you want to translate all to unified language. This is handy because it detects
        automatically the language of each sentence and then translate it.

        @param sentences: list of sentences to translate
        @return: list of all translated sentences
        """
        if not sentences:
            raise NotValidPayload

        translated_sentences = []
        try:
            for sentence in sentences:
                translated = self.translate(payload=sentence)
                translated_sentences.append(translated)

            return translated_sentences

        except Exception as e:
            raise e
