
from deep_translator.constants import BASE_URLS, GOOGLE_LANGUAGES_TO_CODES
from deep_translator.exceptions import LanguageNotSupportedException, ElementNotFoundInGetRequest, NotValidPayload, NotValidLength
from deep_translator.parent import BaseTranslator
from bs4 import BeautifulSoup
import requests


class GoogleTranslator(BaseTranslator):
    """
    class that uses google translate to translate texts
    """

    def __init__(self, source="auto", target="en"):
        """
        @param source: source language to translate from
        @param target: target language to translate to
        """
        self.__base_url = BASE_URLS.get("GOOGLE_TRANSLATE")

        if self.is_language_supported(source, target):
            self._source, self._target = self._map_language_to_code(source.lower(), target.lower())

        super(GoogleTranslator, self).__init__(base_url=self.__base_url,
                                               source=self._source,
                                               target=self._target,
                                               element_tag='div',
                                               element_query={"class": "t0"},
                                               payload_key='q',  # key of payload in the url
                                               hl=self._target,
                                               sl=self._source)

    def _map_language_to_code(self, *languages, **kwargs):
        """

        @param language: type of language
        @return: mapped value of the language or raise an exception if the language is not supported
        """
        for language in languages:
            if language in GOOGLE_LANGUAGES_TO_CODES.values() or language == 'auto':
                yield language
            elif language in GOOGLE_LANGUAGES_TO_CODES.keys():
                yield GOOGLE_LANGUAGES_TO_CODES[language]
            else:
                raise LanguageNotSupportedException(language)

    def is_language_supported(self, *languages, **kwargs):
        for lang in languages:
            if lang != 'auto' and lang not in GOOGLE_LANGUAGES_TO_CODES.keys():
                if lang != 'auto' and lang not in GOOGLE_LANGUAGES_TO_CODES.values():
                    raise LanguageNotSupportedException(lang)
        return True

    def translate(self, payload, **kwargs):
        """
        main function that uses google translate to translate a text
        @param payload: desired text to translate
        @return: str: translated text
        """

        if self._validate_payload(payload):
            payload = payload.strip()

            if self.payload_key:
                self._url_params[self.payload_key] = payload

            response = requests.get(self.__base_url, params=self._url_params)
            soup = BeautifulSoup(response.text, 'html.parser')
            element = soup.find(self._element_tag, self._element_query)
            if not element:
                raise ElementNotFoundInGetRequest(element)

            return element.get_text(strip=True)

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
            raise NotValidPayload(sentences)

        translated_sentences = []
        try:
            for sentence in sentences:
                translated = self.translate(payload=sentence)
                translated_sentences.append(translated)

            return translated_sentences

        except Exception as e:
            raise e


if __name__ == '__main__':
    res = GoogleTranslator(source="auto", target="de").translate(payload='this is a good day')
    print(res)
