"""Main module."""

from deep_translator.exceptions import NotValidPayload, NotValidLength
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

    @staticmethod
    def _validate_payload(payload, min_chars=1, max_chars=5000):
        """
        validate the payload text to translate
        @param payload: text to translate
        @return: bool
        """

        if not payload or not isinstance(payload, str):
            raise NotValidPayload(payload)
        if not BaseTranslator.__check_length(payload, min_chars, max_chars):
            raise NotValidLength
        return True

    @staticmethod
    def __check_length(payload, min_chars, max_chars):
        return True if min_chars < len(payload) < max_chars else False

    @abstractmethod
    def translate(self, payload, **kwargs):
        pass

