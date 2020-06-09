"""Main module."""

from deep_translator.exceptions import NotValidPayload
from abc import ABC, abstractmethod


class BaseTranslator(ABC):
    """
    class that serve as a parent translator class for other different translators
    """
    def __init__(self,
                 base_url=None,
                 source="auto",
                 target="en",
                 payload_key=None,
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
        self.payload_key = payload_key
        super(BaseTranslator, self).__init__()

    def validate_payload(self, payload):
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

    @abstractmethod
    def translate(self, payload, **kwargs):
        pass

    def translate_file(self, path, **kwargs):
        try:
            with open(path) as f:
                text = f.read()

            return self.translate(payload=text)
        except Exception as e:
            raise e

    def translate_sentences(self, sentences=None, **kwargs):
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
