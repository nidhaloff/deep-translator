
from bs4 import BeautifulSoup
import requests
from deep_translator.constants import BASE_URLS, PONS_LANGUAGES_TO_CODES, PONS_CODES_TO_LANGUAGES
from deep_translator.exceptions import LanguageNotSupportedException, ElementNotFoundInGetRequest, NotValidPayload
from deep_translator.parent import BaseTranslator
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

        if self.is_language_supported(source, target):
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
            if language in PONS_LANGUAGES_TO_CODES.values():
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

    def translate(self, word, **kwargs):

        if self._validate_payload(word):
            url = "{}{}-{}/{}".format(self.__base_url, self._source, self._target, quote(word))
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
                            if not kwargs.get('return_all'):
                                return temp
                eof.append(temp)

            if 'return_all' in kwargs and kwargs.get('return_all'):
                return [word for word in eof if word and len(word) > 1]

    def translate_words(self, words, **kwargs):
        if not words:
            raise NotValidPayload(words)

        translated_words = []
        for word in words:
            translated_words.append(self.translate(payload=word))
        return translated_words


if __name__ == '__main__':

    # res = GoogleTranslator(source='auto', target='french').translate_text(path='../examples/test.txt')
    # res = GoogleTranslator(source='auto', target='french').translate_sentences([
    #     "this is good",
    #     "das Wetter ist schön",
    #     "un verme verde in un bicchiere verde"
    # ])
    # res = PonsTranslator(source="en", target="ar").translate(payload='good')
    res = PonsTranslator(source="en", target="ar").translate_words(words=('good', 'cute', 'angry'))
    print(res)
