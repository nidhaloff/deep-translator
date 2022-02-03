
import argparse
from .cli import CLI


def main():
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
                        help="name of the translator you want to use",
                        required=True)
    parser.add_argument('--source',
                        '-src',
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

    args = parser.parse_args()

    cli = CLI()
    if args.languages:
        cli.get_supported_languages(args)
    else:
        cli.translate(args)


if __name__ == "__main__":
    main()
