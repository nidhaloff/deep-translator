=====
Usage
=====

To use deep_translator in a project::

    from deep_translator import GoogleTranslator

    english_text = 'happy coding'

    # first create a GoogleTranslator object with source and target language
    # then use the translate function to translate a text.
    # All language are supported. Basic example:

    result_german = GoogleTranslator(source='auto', target='de').translate(payload=english_text)


    # Alternatively, you can pass languages by their name:

    result_german = GoogleTranslator(source='english', target='german').translate(payload=english_text)

    # soon also support for the PONS translator.

