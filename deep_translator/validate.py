
from .exceptions import NotValidPayload, NotValidLength
import string


def is_empty(text: str):
    return text == ""


def validate_input(text: str, min_chars: int = 0, max_chars: int = 5000):
    """
    validate the target text to translate
    @param min_chars: min characters
    @param max_chars: max characters
    @param text: text to translate
    @return: bool
    """

    if not isinstance(text, str) or text.isdigit():
        raise NotValidPayload(text)
    if not min_chars <= len(text) < max_chars:
        raise NotValidLength(text, min_chars, max_chars)

    return True
