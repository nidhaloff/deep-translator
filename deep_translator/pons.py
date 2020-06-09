from __future__ import absolute_import
from bs4 import BeautifulSoup
import requests
from constants import BASE_URLS, PONS_LANGUAGES_TO_CODES, PONS_CODES_TO_LANGUAGES
from exceptions import LanguageNotSupportedException, ElementNotFoundInGetRequest
from parent import BaseTranslator
from requests.utils import quote


class PonsTranslator(BaseTranslator):
    """
    class that uses PONS translator to translate words
    """
    def __init__(self, source="french", target="english"):
        """
        @param source: source language to translate from
        @param target: target language to translate to
        """
        self.__base_url = BASE_URLS.get("PONS")

        if self.is_language_supported(source, target, translator='pons'):
            self._source, self._target = self._map_language_to_code(source, target)

        super().__init__(base_url=self.__base_url,
                         source=self._source,
                         target=self._target,
                         payload_key=None,
                         element_tag='div',
                         element_query={"class": "target"}
                         )

    def _map_language_to_code(self, *languages, **kwargs):
        """

        @param language: type of language
        @return: mapped value of the language or raise an exception if the language is not supported
        """
        for language in languages:
            if language in PONS_LANGUAGES_TO_CODES.values() or language == 'auto':
                yield PONS_CODES_TO_LANGUAGES[language]
            elif language in PONS_LANGUAGES_TO_CODES.keys():
                yield language
            else:
                raise LanguageNotSupportedException(language)

    def is_language_supported(self, *languages, **kwargs):
        for lang in languages:
            if lang not in PONS_LANGUAGES_TO_CODES.keys():
                if lang not in PONS_LANGUAGES_TO_CODES.values():
                    raise LanguageNotSupportedException(lang)
        return True

    def translate(self, payload, **kwargs):

        url = "{}{}-{}/{}".format(self.__base_url, self._source, self._target, quote(payload))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        elements = soup.findAll(self._element_tag, self._element_query)
        if not elements:
            raise ElementNotFoundInGetRequest(elements)

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
