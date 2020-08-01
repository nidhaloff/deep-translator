=====
Usage
=====

.. code-block:: python

    from deep_translator import GoogleTranslator, PonsTranslator, LingueeTranslator, MyMemoryTranslator

    english_text = 'happy coding'

    result_german = GoogleTranslator(source='auto', target='de').translate(text=english_text)

    # Alternatively, you can pass languages by their name:
    translated = GoogleTranslator(source='english', target='german').translate(text=english_text)

    # or maybe you want to translate a text file ?
    translated = GoogleTranslator(source='auto', target='german').translate_file('path/to/file')

    # or maybe you have many sentences in different languages and want to automate the translation process
    translated = GoogleTranslator(source='auto', target='de').translate_sentences(your_list_of_sentences)


or maybe you would like to use the Pons translator: Pons.com


.. code-block:: python

    word = 'good'
    translated_word = PonsTranslator(source='english', target='french').translate(word)

    # set the argument return_all to True if you want to get all synonyms of the word to translate
    translated_word = PonsTranslator(source='english', target='french').translate(word, return_all=True)


Alternatively deep_translator (version >= 1.0.0) supports the Linguee translator:


.. code-block:: python

    word = 'good'
    translated_word = LingueeTranslator(source='english', target='french').translate(word)

    # set the argument return_all to True if you want to get all synonyms of the word to translate
    translated_word = LingueeTranslator(source='english', target='french').translate(word, return_all=True)


The mymemory translator is also supported for version >= 1.0.2:

.. code-block:: python

    word = 'good'
    translated_word = MyMemoryTranslator(source='english', target='french').translate(word)


Usage from Terminal
====================

For a quick access, you can use the deep_translator from terminal. For this to work, you need to provide
the right arguments, which are the translator you want to use, source language, target language and the text
you want to translate.

For example, provide "google" as an argument to use the google translator. Alternatively you can use
the other supported translators. Just read the documentation to have an overview about the supported
translators in this library.

.. code-block:: console

    $ deep_translator --translator "google" --source "english" --target "german" --text "happy coding"

Or you can go for the short version:

.. code-block:: console

    $ deep_translator -trans "google" -src "english" -tg "german" -txt "happy coding"

If you want, you can also pass the source and target language by their abbreviation

.. code-block:: console

    $ deep_translator -trans "google" -src "en" -tg "de" -txt "happy coding"
