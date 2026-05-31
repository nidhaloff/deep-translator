import argparse
import pymupdf
from deep_translator import (
    GoogleTranslator,
    ChatGptTranslator,
)
from pdf_translator import (
    COLOR_MAP,
    get_blocks,
    write_translated_page,
)

# Map of supported translators
TRANSLATORS = {
    'google': GoogleTranslator,
    'chatgpt': ChatGptTranslator,
}


def translate_pdf(input_file: str, source_lang: str, target_lang: str, layer: str = "Text",
                  translator_name: str = "google", text_color: str = "darkred", keep_original: bool = True):
    """
    Translate a PDF file from source language to target language

    Args:
        input_file: Path to input PDF file
        source_lang: Source language code (e.g. 'en', 'fr')
        target_lang: Target language code (e.g. 'ko', 'ja')
        layer: Name of the OCG layer (default: "Text")
        translator_name: Name of the translator to use (default: "google")
        text_color: Color of translated text (default: "darkred")
        keep_original: Whether to keep original text visible (default: True)
    """
    if translator_name not in TRANSLATORS:
        raise ValueError(
            f"Unsupported translator: {translator_name}. "
            f"Available translators: {', '.join(TRANSLATORS.keys())}"
        )

    translator = TRANSLATORS[translator_name](source=source_lang, target=target_lang)
    output_file = input_file.rsplit('.', 1)[0] + f'-{target_lang}.pdf'

    doc = pymupdf.open(input_file)

    # Optional content layer for the translation overlay
    ocg_trans = doc.add_ocg(layer, on=True)
    ocg_orig = None if keep_original else doc.add_ocg("Original", on=False)

    for page in doc:
        blocks = get_blocks(page)
        translated_texts = [translator.translate(b[4]) for b in blocks]
        write_translated_page(
            page,
            blocks,
            translated_texts,
            text_color=text_color,
            oc_trans=ocg_trans,
            oc_orig=ocg_orig,
        )

    doc.subset_fonts()
    doc.ez_save(output_file)
    print(f"Translated PDF saved as: {output_file}")


def main():
    """
    Examples:

        # Basic usage
        python translator_cli.py --source english --target zh-CN input.pdf

        # With custom color and hiding original text
        python translator_cli.py --source english --target zh-CN --color blue --no-original input.pdf

        # Using ChatGPT translator
        export OPENAI_API_KEY=sk-proj-xxxx
        export OPENAI_API_BASE=https://api.xxxx.com/v1
        export OPENAI_MODEL=default_model

        python translator_cli.py --source english --translator chatgpt --target zh-CN input.pdf

        # do not keep original text as an optional layer
        python translator_cli.py --source english --translator chatgpt --target zh-CN --no-original input.pdf

    The translated content is an optional content layer in the new PDF file.
    The layer can be toggled in Acrobat PDF Reader and Foxit Reader.
    """
    parser = argparse.ArgumentParser(description='Translate PDF documents.')
    parser.add_argument('input_file', help='Input PDF file path')
    parser.add_argument('--source', '-s', default='en',
                        help='Source language code (default: en)')
    parser.add_argument('--target', '-t', default='zh-CN',
                        help='Target language code (default: zh-CN)')
    parser.add_argument('--layer', '-l', default='Text',
                        help='Name of the OCG layer (default: Text)')
    parser.add_argument('--translator', '-tr', default='google',
                        choices=list(TRANSLATORS.keys()),
                        help='Translator to use (default: google)')
    parser.add_argument('--color', '-c', default='darkred',
                        choices=list(COLOR_MAP.keys()),
                        help='Color of translated text (default: darkred)')
    parser.add_argument('--no-original', action='store_true',
                        help='Do not keep original text in base layer (default: False)')

    args = parser.parse_args()

    try:
        translate_pdf(args.input_file, args.source, args.target, args.layer,
                      args.translator, args.color, not args.no_original)
    except Exception as e:
        print(f"Error: {str(e)}")
        exit(1)


if __name__ == "__main__":
    main()
