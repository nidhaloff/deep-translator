"""parent translator class"""

from .exceptions import NotValidPayload, NotValidLength, InvalidSourceOrTargetLanguage
from abc import ABC, abstractmethod
import string

class BaseTranslator(ABC):
    """
    Abstract class that serve as a parent translator for other different translators
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
        Args:
            base_url: str: base_url for send requests to a translator
            source: str: source language to translate from
            target: str: target language to translate to
            payload_key: str: payload_key for send requests to a translator
            element_tag: str: element_tag for send requests to a translator
            element_query: str: element_tag for send requests to a translator
            url_params: arbitrary args
        Raises:
            InvalidSourceOrTargetLanguage
        """
        if source == target:
            raise InvalidSourceOrTargetLanguage(source)

        self.__base_url = base_url
        self._source = source
        self._target = target
        self._url_params = url_params
        self._element_tag = element_tag
        self._element_query = element_query
        self.payload_key = payload_key
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) '
                                      'AppleWebit/535.19'
                                      '(KHTML, like Gecko) Chrome/18.0.1025.168 Safari/535.19'}
        super(BaseTranslator, self).__init__()

    @staticmethod
    def _validate_payload(payload, min_chars=1, max_chars=5000):
        """
        Validate the target text to translate
        Args:
            payload: str: text to translate.
            min_chars: int: minimum characters allowed
            max_chars: int: maximum characters allowed
        Returns:
            True
        Raises:
            NotValidPayload
            NotValidLength
        """

        if not payload or not isinstance(payload, str) or not payload.strip() or payload.isdigit():
            raise NotValidPayload(payload)

        # check if payload contains only symbols
        if all(i in string.punctuation for i in payload):
            raise NotValidPayload(payload)

        if not BaseTranslator.__check_length(payload, min_chars, max_chars):
            raise NotValidLength(payload, min_chars, max_chars)
        return True

    @staticmethod
    def __check_length(payload, min_chars, max_chars):
        """
        Check length of the provided target text to translate
        Args:
            payload: str: text to translate
            min_chars: int: minimum characters allowed
            max_chars: int: maximum characters allowed
        Returns:
            bool
        """
        return True if min_chars <= len(payload) < max_chars else False

    @abstractmethod
    def translate(self, text, **kwargs):
        """
        Translate a text using a translator under the hood and return the translated text
        check length of the provided target text to translate
        Args:
            text: str: text to translate.
            kwargs: dict: arbitrary args.
        Returns:
            str
        """
        return NotImplemented('You need to implement the translate method!')



