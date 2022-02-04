"""Console script for deep_translator."""

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
import argparse


class CLI(object):

    translators_dict = None
    translator = None

    def __init__(self, custom_args=None):
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
        self.custom_args = custom_args
        self.args = self.parse_args()

        translator_class = self.translators_dict.get(self.args.translator, None)
        if not translator_class:
            raise Exception(f"Translator {self.args.translator} is not supported."
                            f"Supported translators: {list(self.translators_dict.keys())}")
        self.translator = translator_class(source=self.args.source, target=self.args.target)

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

    def parse_args(self):
        """
        function responsible for parsing terminal arguments and provide them for further use in the translation process
        """
        parser = argparse.ArgumentParser(add_help=True,
                                         description="Official CLI for deep-translator",
                                         usage="dt --help")

        parser.add_argument('--translator',
                            '-trans',
                            default='google',
                            type=str,
                            help="name of the translator you want to use")
        parser.add_argument('--source',
                            '-src',
                            default='auto',
                            type=str,
                            help="source language to translate from")
        parser.add_argument('--target',
                            '-tg',
                            type=str,
                            help="target language to translate to")
        parser.add_argument('--text',
                            '-txt',
                            type=str,
                            help="text you want to translate")
        parser.add_argument('--languages',
                            '-lang',
                            action='store_true',
                            help="all the languages available with the translator"
                                 "Run the command deep_translator -trans <translator service> -lang")
        parsed_args = parser.parse_args(self.custom_args) if self.custom_args else parser.parse_args()
        print(f"parsed args: {parsed_args}")
        return parsed_args

    def run(self):
        if self.args.languages:
            self.get_supported_languages()
        else:
            self.translate()
