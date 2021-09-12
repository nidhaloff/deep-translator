"""
Papago Translator API
"""
import json
from .constants import BASE_URLS, PAPAGO_LANGUAGE_TO_CODE
from .exceptions import LanguageNotSupportedException, TranslationNotFound, NotValidPayload
import requests
import warnings
import logging


class PapagoTranslator(object):
    """
    class that wraps functions, which use google translate under the hood to translate text(s)
    """
    _languages = PAPAGO_LANGUAGE_TO_CODE
    supported_languages = list(_languages.keys())

    def __init__(self, client_id=None, secret_key=None, source="auto", target="en", **_):
        """
        Args:
            client_id: str: client_id for use PapagoTranslator.
            secret_key: str: secret_key for use PapagoTranslator.
            source: str: source language to translate from.
            target: str: target language to translate to.
        Raises:
            Exception
        """
        if not client_id or not secret_key:
            raise Exception("Please pass your client id and secret key! visit the papago website for more infos")

        self.__base_url = BASE_URLS.get("PAPAGO_API")
        self.client_id = client_id
        self.secret_key = secret_key
        if self.is_language_supported(source, target):
            self._source, self._target = self._map_language_to_code(source.lower(), target.lower())

    @staticmethod
    def get_supported_languages(as_dict=False, **_):
        """
        Return the supported languages by the google translator
        Args:
            as_dict: bool: if True, the languages will be returned as a dictionary mapping languages to their abbreviations
        Returns:
            list or dict
        """
        return PapagoTranslator.supported_languages if not as_dict else PapagoTranslator._languages

    def _map_language_to_code(self, *languages):
        """
        Map language to its corresponding code (abbreviation) if the language was passed by its full name by the user.
        Args:
            languages: list of languages.
        Yields:
            str
        Raises:
            LanguageNotSupportedException if the language is not supported.
        Examples:
            PapagoTranslatorObject._map_language_to_code("ko", "uk", "en")
        """
        for language in languages:
            if language in self._languages.values() or language == 'auto':
                yield language
            elif language in self._languages.keys():
                yield self._languages[language]
            else:
                raise LanguageNotSupportedException(language)

    def is_language_supported(self, *languages):
        """
        Check if the language is supported by the translator
        Args:
            languages: list of languages.
        Returns:
            True
        Raises
            LanguageNotSupportedException
        Examples:
            PapagoTranslatorObject.is_language_supported("ko", "uk", "en")
        """

        all_supported_languages = [*self._languages.keys(), * self._languages.values()]

        for lang in languages:
            if lang != 'auto' and lang not in all_supported_languages:
                raise LanguageNotSupportedException(lang)
        return True

    def translate(self, text, **kwargs):
        """
        Function that uses Papago Translator to translate a word
        Args:
            text: str: word to translate.
        Keyword Args:
            requests_kwargs: arbitrary args for requests.post.
        Returns:
             str: translated text.
        Raises:
            Exception
            TranslationNotFound
        """

        payload = {
            "source": self._source,
            "target": self._target,
            "text": text
        }
        headers = {
            'X-Naver-Client-Id': self.client_id,
            'X-Naver-Client-Secret': self.secret_key,
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
        }
        response = requests.post(self.__base_url, headers=headers, data=payload, **kwargs.get("requests_kwargs", {}))
        if response.status_code != 200:
            raise Exception(f'Translation error! -> status code: {response.status_code}')
        res_body = json.loads(response.text)
        if "message" not in res_body:
            raise TranslationNotFound(text)

        msg = res_body.get("message")
        result = msg.get("result", None)
        if not result:
            raise TranslationNotFound(text)
        translated_text = result.get("translatedText")
        return translated_text

    def translate_file(self, path, **_):
        """
        Translate directly from file
        Args:
             path: str: path to the target file.
        Returns:
            str
        Raises:
            Exception
        """
        try:
            with open(path) as f:
                text = f.read().strip()
            return self.translate(text)
        except Exception as e:
            raise e

    def translate_sentences(self, sentences=None, **_):
        """
        Translate many sentences together. This makes sense if you have sentences with different languages
        and you want to translate all to unified language. This is handy because it detects
        automatically the language of each sentence and then translate it.

        Args:
            sentences: list of str: list of sentences to translate.
        Returns:
             list of all translated sentences.
        Raises:
            NotValidPayload
            Exception
        """
        warnings.warn("deprecated. Use the translate_batch function instead", DeprecationWarning, stacklevel=2)
        logging.warning("deprecated. Use the translate_batch function instead")
        if not sentences:
            raise NotValidPayload(sentences)

        translated_sentences = []
        try:
            for sentence in sentences:
                translated = self.translate(text=sentence)
                translated_sentences.append(translated)

            return translated_sentences

        except Exception as e:
            raise e

    def translate_batch(self, batch=None, **kwargs):
        """
        Translate a list of texts
        Args:
            batch: list: list of texts to translate.
            kwargs: dict: arbitrary args for PapagoTranslatorObject.translate
        Returns:
             list of translations
        Raises:
            Exception
        """
        if not batch:
            raise Exception("Enter your text list that you want to translate")
        arr = []
        for i, text in enumerate(batch):
            translated = self.translate(text, **kwargs)
            arr.append(translated)
        return arr


