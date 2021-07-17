"""Console script for deep_translator."""

import click
from .google_trans import GoogleTranslator
from .mymemory import MyMemoryTranslator
from .deepl import DeepL
from .qcri import QCRI
from .linguee import LingueeTranslator
from .pons import PonsTranslator
from .yandex import YandexTranslator
from .microsoft import MicrosoftTranslator
from .papago import PapagoTranslator

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])

@click.command(name='Deep Translator', context_settings=CONTEXT_SETTINGS, no_args_is_help=True)
@click.argument(
    'translator', 
    required=True, 
    default='google', 
    type=str)
@click.option(
    "--source", 
    "-src", 
    required=True, 
    type=str, 
    help="source language to translate from")
@click.option(
    "--target", 
    "-tgt", 
    required=True, 
    type=str, 
    help="target language to translate to")
@click.option(
    "--text", 
    "-txt", 
    type=str,
    required = True,
    prompt="Enter the text you want to translate",
    help="text you want to translate")
@click.option(
    "--api-key",
    type=str,
    help="required for DeepL, QCRI, Yandex, Microsoft and Papago translators")
@click.option(
    "--languages",
    "-lang",
    is_flag=True,
    help="list all the languages available with the translator."
    " Run with deep_translator <translator service> -lang",)
def main(translator, source, target, text, api_key, languages):
    """
    Use TRANSLATOR to translate source material into another language.
    Available translators include: Google, MyMemory, QCRI, Linguee, Pons, Yandex, Microsoft (Bing), and Papago.\n
    \f
    function responsible for parsing terminal arguments and provide them for
    further use in the translation process
    """
    api_key_required = ["deepl", "qcri", "yandex", "microsoft", "papago"]
    if translator in api_key_required and not api_key:
        click.echo(
            "This translator requires an api key provided through --api-key"
        )
    elif languages:
        print_supported_languages(translator, api_key)
    else:
        translate(translator, source, target, text, api_key)

def translate(translator, source, target, text, api_key):
    """
    function used to provide translations from the parsed terminal arguments
    @param translator: translator name parsed from terminal arguments
    @param source: source language parsed from terminal arguments
    @param target: target language parsed from terminal arguments
    @param text: text that will be translated parsed from terminal arguments
    @param api_key: api key for translators that requires them
    @return: None
    """
    if translator == "google":
        translator = GoogleTranslator(source=source, target=target)
    elif translator == "mymemory":
        translator = MyMemoryTranslator(source=source, target=target)
    elif translator == "deepl":
        translator = DeepL(source=source, target=target, api_key=api_key)
    elif translator == "qcri":
        translator = QCRI(source=source, target=target, api_key=api_key)
    elif translator == "linguee":
        translator = LingueeTranslator(source=source, target=target)
    elif translator == "pons":
        translator = PonsTranslator(source=source, target=target)
    elif translator == "yandex":
        translator = YandexTranslator(
            source=source,
            target=target,
            api_key=api_key
        )
    elif translator == "microsoft":
        translator = MicrosoftTranslator(
            source=source,
            target=target,
            api_key=api_key
        )
    elif translator == "papago":
        translator = PapagoTranslator(
            source=source,
            target=target,
            api_key=api_key
        )
    else:
        click.echo(
            "The given translator is not supported."
            " Please use a translator supported by the deep_translator tool"
        )
        return

    res = translator.translate(text)
    click.echo(f" | Translation from {source} to {target} |")
    click.echo(f"Translated text: \n {res}")

def print_supported_languages(requested_translator, api_key):
    """
    function used to print the languages supported by the translator service
    from the parsed terminal arguments
    @param args: parsed terminal arguments
    @return: None
    """
    translator = None
    if requested_translator == "google":
        translator = GoogleTranslator
    elif requested_translator == "mymemory":
        translator = MyMemoryTranslator
    elif requested_translator == "qcri":
        translator = QCRI(api_key=api_key)
    elif requested_translator == "linguee":
        translator = LingueeTranslator
    elif requested_translator == "pons":
        translator = PonsTranslator
    elif requested_translator == "yandex":
        translator = YandexTranslator(api_key=api_key)
    elif requested_translator == "microsoft":
        translator = MicrosoftTranslator(api_key=api_key)
    elif requested_translator == "papago":
        translator = PapagoTranslator(api_key=api_key)
    else:
        click.echo(
            "The given translator is not supported."
            " Please use a translator supported by the deep_translator tool"
        )
        return

    supported_languages = translator.get_supported_languages(as_dict=True)
    click.echo(f"Languages supported by '{requested_translator}' are :")
    for k, v in supported_languages.items():
        click.echo(f"|- {k}: {v}")

if __name__ == "__main__":
    main()