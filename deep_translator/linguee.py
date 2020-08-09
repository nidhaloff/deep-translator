from deep_translator.constants import BASE_URLS, LINGUEE_LANGUAGES_TO_CODES, LINGUEE_CODE_TO_LANGUAGE
from deep_translator.exceptions import LanguageNotSupportedException, TranslationNotFound, NotValidPayload, ElementNotFoundInGetRequest
from deep_translator.parent import BaseTranslator
from bs4 import BeautifulSoup
import requests
from requests.utils import requote_uri


class LingueeTranslator(BaseTranslator):
    _languages = LINGUEE_LANGUAGES_TO_CODES
    supported_languages = list(_languages.keys())

    def __init__(self, source, target="en"):
        """
        @param source: source language to translate from
        @param target: target language to translate to
        """
        self.__base_url = BASE_URLS.get("LINGUEE")

        if self.is_language_supported(source, target):
            self._source, self._target = self._map_language_to_code(source.lower(), target.lower())

        super().__init__(base_url=self.__base_url,
                         source=self._source,
                         target=self._target,
                         element_tag='a',
                         element_query={'class': 'dictLink featured'},
                         payload_key=None,  # key of text in the url
                        )

    @staticmethod
    def get_supported_languages(as_dict=False):
        return LingueeTranslator.supported_languages if not as_dict else LingueeTranslator._languages

    def _map_language_to_code(self, *languages, **kwargs):
        """
        @param language: type of language
        @return: mapped value of the language or raise an exception if the language is not supported
        """
        for language in languages:
            if language in LINGUEE_LANGUAGES_TO_CODES.values():
                yield LINGUEE_CODE_TO_LANGUAGE[language]
            elif language in LINGUEE_LANGUAGES_TO_CODES.keys():
                yield language
            else:
                raise LanguageNotSupportedException(language)

    def is_language_supported(self, *languages, **kwargs):
        for lang in languages:
            if lang not in LINGUEE_LANGUAGES_TO_CODES.keys():
                if lang not in LINGUEE_LANGUAGES_TO_CODES.values():
                    raise LanguageNotSupportedException(lang)
        return True

    def translate(self, word, return_all=False, **kwargs):

        if self._validate_payload(word):
            # %s-%s/translation/%s.html
            url = "{}{}-{}/translation/{}.html".format(self.__base_url, self._source, self._target, word)
            url = requote_uri(url)
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            elements = soup.find_all(self._element_tag, self._element_query)
            if not elements:
                raise ElementNotFoundInGetRequest(elements)

            filtered_elements = []
            for el in elements:
                try:
                    pronoun = el.find('span', {'class': 'placeholder'}).get_text(strip=True)
                except AttributeError:
                    pronoun = ''
                filtered_elements.append(el.get_text(strip=True).replace(pronoun, ''))

            if not filtered_elements:
                raise TranslationNotFound(word)

            return filtered_elements if return_all else filtered_elements[0]

    def translate_words(self, words, **kwargs):
        if not words:
            raise NotValidPayload(words)

        translated_words = []
        for word in words:
            translated_words.append(self.translate(payload=word))
        return translated_words


