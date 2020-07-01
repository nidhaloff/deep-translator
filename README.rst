===============
deep_translator
===============


.. image:: https://img.shields.io/pypi/v/deep_translator.svg
        :target: https://pypi.python.org/pypi/deep_translator

.. image:: https://img.shields.io/travis/nidhaloff/deep_translator.svg
        :target: https://travis-ci.com/nidhaloff/deep_translator

.. image:: https://readthedocs.org/projects/deep-translator/badge/?version=latest
        :target: https://deep-translator.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status




A flexible python tool to translate between different languages in a simple way.


* Free software: MIT license
* Documentation: https://deep-translator.readthedocs.io.

Motivation
-----------
I needed to translate a text using python. It was hard to find a simple way to do it.
There are other libraries that can be used for this task, but somehow,most of them
are buggy, not supported anymore or complex.

Therefore, I decided to build this simple tool, it is clean and easy to use and provide
support for all languages since it uses google translate under the hood.
More features are coming soon, mainly support for the PONS translator and others.

Basically, my goal is to integrate support for multiple famous translators
in this tool.

Features
--------

* Support for google translate
* Support for Pons translator (pons.com)
* Support for the Linguee translator
* Translate directly from a text file
* Get multiple translation for a word
* Automate the translation of different paragraphs in different languages


Usage
=====

.. code-block:: python

    from deep_translator import GoogleTranslator, PonsTranslator, LingueeTranslator

    english_text = 'happy coding'

    result_german = GoogleTranslator(source='auto', target='de').translate(payload=english_text)

    # Alternatively, you can pass languages by their name:
    translated = GoogleTranslator(source='english', target='german').translate(payload=english_text)

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


Alternatively deep_translator now supports the Linguee translator:


.. code-block:: python

    word = 'good'
    translated_word = LingueeTranslator(source='english', target='french').translate(word)

    # set the argument return_all to True if you want to get all synonyms of the word to translate
    translated_word = PonsTranslator(source='english', target='french').translate(word, return_all=True)

Take a look in the examples folder for more :)

Please contribute and give me a feedback if you found the package useful/helpful or you are using it :)
