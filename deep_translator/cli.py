"""Console script for deep_translator."""
import sys

from .google_trans import GoogleTranslator
from .mymemory import MyMemoryTranslator
from .pons import PonsTranslator
from .linguee import LingueeTranslator
from .yandex import YandexTranslator
from .deepl import DeepL
from .qcri import QCRI
from .papago import PapagoTranslator
from .microsoft import MicrosoftTranslator
from .libre import LibreTranslator


class CLI(object):

    translators_dict = None
    translator = None

    def __init__(self, args):
        self.translators_dict = {
            'google': GoogleTranslator,
            'pons': PonsTranslator,
            'linguee': LingueeTranslator,
            'mymemory': MyMemoryTranslator,
            'deepl': DeepL,
            'libre': LibreTranslator,
            'yandex': YandexTranslator,
            'microsoft': MicrosoftTranslator,
            'qcri': QCRI,
            'papago': PapagoTranslator
        }
        self.args = args
        translator_class = self.translators_dict.get(self.args.translator, None)
        if not translator_class:
            raise Exception(f"Translator {self.args.translator} is not supported."
                            f"Supported translators: {list(self.translators_dict.keys())}")
        self.translator = translator_class(source=args.source, target=args.target)

    def translate(self):
        """
        function used to provide translations from the parsed terminal arguments
        @return: None
        """
        res = self.translator.translate(self.args.text)
        print("Translation from {} to {}".format(self.args.source, self.args.target))
        print("-"*50)
        print("Translation result: {}".format(res))

    def get_supported_languages(self):
        """
        function used to return the languages supported by the translator service from the parsed terminal arguments
        @return: None
        """

        translator_supported_languages = self.translator.get_supported_languages(as_dict=True)
        print(f'Languages supported by \'{self.args.translator}\' are :\n')
        print(translator_supported_languages)



