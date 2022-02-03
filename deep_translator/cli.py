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

    def __init__(self):
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

    def _get_translator(self, name):
        return self.translators_dict[name]

    def translate(self, args):
        """
        function used to provide translations from the parsed terminal arguments
        @param args: parsed terminal arguments
        @return: None
        """
        translator = self._get_translator(args.translator)
        res = translator.translate(args.text)
        print(" | Translation from {} to {} |".format(args.source, args.target))
        print("Translated text: \n {}".format(res))

    def get_supported_languages(self, args):
        """
        function used to return the languages supported by the translator service from the parsed terminal arguments
        @param args: parsed terminal arguments
        @return: None
        """
        translator = self._get_translator(args.translator)
        translator_supported_languages = translator.get_supported_languages(as_dict=True)
        print(f'Languages supported by \'{args.translator}\' are :\n')
        print(translator_supported_languages)
        sys.exit()



