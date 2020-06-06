"""Main module."""


from bs4 import BeautifulSoup
import requests
from models import BaseTranslator
from constants import BASE_URLS, LANGUAGES_TO_CODES, CODES_TO_LANGUAGES
from exceptions import LanguageNotSupportedException, NotValidPayload, ElementNotFoundInGetRequest, NotValidLength
from parent import ParentTranslator
import string


class GoogleTranslator(ParentTranslator):
    """
    class that uses google translate to translate texts
    """
    def __init__(self, source="auto", target="en"):
        """
        @param source: source language to translate from
        @param target: target language to translate to
        """
        self.__base_url = BASE_URLS.get("GOOGLE_TRANSLATE")

        if self._validate_languages([source.lower(), target.lower()]):
            self._source = self._map_language_to_code(source.lower())
            self._target = self._map_language_to_code(target.lower())

        super(GoogleTranslator, self).__init__(base_url=self.__base_url,
                                               source=self._source,
                                               target=self._target,
                                               element_tag='div',
                                               element_query={"class": "t0"},
                                               hl=self._target,
                                               sl=self._source,
                                               q=None)

    def _map_language_to_code(self, language):
        """

        @param language: type of language
        @return: mapped value of the language or raise an exception if the language is not supported
        """
        if language in LANGUAGES_TO_CODES.values() or language == 'auto':
            return language
        elif language in LANGUAGES_TO_CODES.keys():
            return LANGUAGES_TO_CODES[language]
        else:
            raise LanguageNotSupportedException(language)

    def translate(self, payload, payload_tag='q', **kwargs):
        return super().translate(payload, payload_tag)


class PonsTranslator(ParentTranslator):
    """
    class that uses PONS translator to translate words
    """
    def __init__(self, source="french", target="english"):
        """
        @param source: source language to translate from
        @param target: target language to translate to
        """
        self.__base_url = BASE_URLS.get("PONS")

        if self._validate_languages([source.lower(), target.lower()]):
            self._source = self._map_language_to_code(source.lower())
            self._target = self._map_language_to_code(target.lower())

        super().__init__(base_url=self.__base_url,
                         source=self._source,
                         target=self._target,
                         element_tag='div',
                         element_query={"class": "target"}
                         )

    def _map_language_to_code(self, language):
        """

        @param language: type of language
        @return: mapped value of the language or raise an exception if the language is not supported
        """
        if language in LANGUAGES_TO_CODES.values():
            return CODES_TO_LANGUAGES[language]
        elif language in LANGUAGES_TO_CODES.keys():
            return language
        else:
            raise LanguageNotSupportedException(language)

    def _validate_languages(self, languages):
        """

        @param languages: languages to validate
        @return: True or raise an exception
        """
        for lang in languages:
            if lang not in LANGUAGES_TO_CODES.keys():
                if lang not in LANGUAGES_TO_CODES.values():
                    raise LanguageNotSupportedException(lang)
        return True

    def translate(self, payload, payload_tag=None, **kwargs):
        from requests.utils import quote
        url = "{}{}-{}/{}".format(self.__base_url, self._source, self._target, quote(payload))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        elements = soup.findAll(self._element_tag, self._element_query)
        # elements = soup.body.find_all('a')
        eof = []
        for el in elements:
            temp = ''
            for e in el.findAll('a'):
                if e.parent.name == 'div':
                    if e and "/translate/{}-{}/".format(self._target, self._source) in e.get('href'):
                        temp += e.get_text() + ' '
            eof.append(temp)

        return [word for word in eof if word and len(word) > 1]


if __name__ == '__main__':
    # res = GoogleTranslator(source='auto', target='french').translate(payload="A paragraph is a series of related sentences developing a central idea, called the topic. Try to think about paragraphs in terms of thematic unity: a paragraph is a sentence or a group of sentences that supports one central, unified idea. Paragraphs add one idea at a time to your broader argument.")
    # res = GoogleTranslator(source='auto', target='french').translate_text(path='../examples/test.txt')
    # res = GoogleTranslator(source='auto', target='french').translate_sentences([
    #     "this is good",
    #     "das Wetter ist schön",
    #     "un verme verde in un bicchiere verde"
    # ])
    res = PonsTranslator(source="english", target="arabic").translate(payload='good')
    print(res)
