"""Main module."""

from bs4 import BeautifulSoup
import requests
from models import BaseTranslator
from constants import BASE_URLS, LANGUAGES_TO_CODES
from exceptions import LanguageNotSupportedException, NotValidPayload


class GoogleTranslator(BaseTranslator):

    def __init__(self, source="auto", target="en"):
        self.__base_url = BASE_URLS.get("GOOGLE_TRANSLATE")
        super(GoogleTranslator, self).__init__()

        if self._validate_languages([source.lower(), target.lower()]):
            self._source = self._map_language_to_code(source.lower())
            self._target = self._map_language_to_code(target.lower())

    def _validate_payload(self, payload):
        if not isinstance(payload, str):
            return False
        elif not payload:
            return False
        elif len(payload) > 5000:
            return False
        else:
            return True

    def _map_language_to_code(self, language):

        if language in LANGUAGES_TO_CODES.values() or language == 'auto':
            return language
        elif language in LANGUAGES_TO_CODES.keys():
            return LANGUAGES_TO_CODES[language]
        else:
            raise LanguageNotSupportedException(language)

    def _validate_languages(self, languages):
        for lang in languages:
            if lang != 'auto' and lang not in LANGUAGES_TO_CODES.keys():
                if lang != 'auto' and lang not in LANGUAGES_TO_CODES.values():
                    raise LanguageNotSupportedException(lang)
        return True

    def translate(self, payload):

        valid = self._validate_payload(payload)
        if not valid:
            raise NotValidPayload(payload)

        try:
            payload = payload.strip()
            params = {
                      "hl": self._target,
                      "sl": self._source,
                      "q": payload
            }

            res = requests.get(self.__base_url, params=params)
            soup = BeautifulSoup(res.text, 'html.parser')
            res = soup.find("div", {"class": "t0"})
            return res.get_text(strip=True)

        except Exception as e:
            print(e.args)
            raise


