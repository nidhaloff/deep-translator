##################
deep_translator
##################


.. image:: https://img.shields.io/pypi/v/deep_translator.svg
        :target: https://pypi.python.org/pypi/deep_translator
.. image:: https://img.shields.io/travis/nidhaloff/deep_translator.svg
        :target: https://travis-ci.com/nidhaloff/deep_translator
.. image:: https://readthedocs.org/projects/deep-translator/badge/?version=latest
        :target: https://deep-translator.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status
.. image:: https://img.shields.io/pypi/l/deep-translator
        :target: https://pypi.python.org/pypi/deep_translator

.. image:: https://img.shields.io/pypi/dm/deep-translator
        :target: https://pypi.python.org/pypi/deep_translator
.. image:: https://img.shields.io/pypi/status/deep-translator
        :target: https://pypi.python.org/pypi/deep_translator
.. image:: https://img.shields.io/pypi/wheel/deep-translator
        :target: https://pypi.python.org/pypi/deep_translator

.. image:: https://img.shields.io/github/last-commit/nidhaloff/gpx_converter
        :alt: GitHub last commit
        :target: https://pypi.python.org/pypi/deep_translator

.. image:: https://img.shields.io/twitter/url?url=https%3A%2F%2Ftwitter.com%2FNidhalBaccouri
        :alt: Twitter URL
        :target: https://twitter.com/NidhalBaccouri

.. image:: https://img.shields.io/badge/$-buy%20me%20a%20coffee-ff69b4.svg?style=social
   :target: https://www.buymeacoffee.com/nidhaloff?new=1


=======================
Translation for humans
=======================

A flexible **FREE** and **UNLIMITED** tool to translate between different languages in a simple way using multiple translators.


* Free software: MIT license
* Documentation: https://deep-translator.readthedocs.io.

==========
Motivation
==========

I needed to translate a text using python. It was hard to find a simple way to do it.
There are other libraries that can be used for this task, but most of them
are **buggy, not free, limited, not supported anymore or complex to use.**

Therefore, I decided to build this simple tool. It is 100% free, unlimited, easy to use and provide
support for all languages.

Basically, my goal was to integrate support for multiple famous translators
in this tool.

======================
When you should use it
======================

- If you want to translate text using python
- If you want to translate from a file
- If you want to get translations from many sources and not only one
- If you want to automate translations
- If you want to compare different translations
- If you want to detect language automatically

======================
Why you should use it
======================

- High level of abstraction
- Automatic language detection
- Easy to use and extend
- It's the only python tool that integrates many translators
- Stable
- Support for most famous universal translators

========
Features
========

* Support for google translate
* Support for Pons translator (pons.com)
* Support for the Linguee translator
* Support for the Mymemory translator
* Automatic single language detection
* Batch language detection
* Translate directly from a text file
* Get multiple translation for a word
* Automate the translation of different paragraphs in different languages
* Translate directly from terminal (version >= 1.1.0)

=============
Installation
=============

Install the stable release:

.. code-block:: console

    $ pip install -U deep_translator

take a look at the docs if you want to install from source.

=====
Usage
=====

In this section, demos on how to use all different integrated translators in this tool are provided.
This includes the google, pons, linguee and mymemory translator (at least for now). Perhaps more
translators will be integrated in the future.

Imports
--------

.. code-block:: python

    from deep_translator import (GoogleTranslator,
                                 PonsTranslator,
                                 LingueeTranslator,
                                 MyMemoryTranslator,
                                 single_detection,
                                 batch_detection)


Check Supported Languages
---------------------------

.. note::

    You can check the supported languages of each translator by calling the
    get_supported_languages function as a static method.

.. code-block:: python

    # default return type is a list
    langs_list = GoogleTranslator.get_supported_languages()  # output: [arabic, french, english etc...]

    # alternatively, you can the dictionary containing languages mapped to their abbreviation
    langs_dict = GoogleTranslator.get_supported_languages(as_dict=True)  # output: {arabic: ar, french: fr, english:en etc...}

Language Detection
------------------

.. note::

    You can also detect language automatically. Notice that this package is free and my goal is to keep it free.
    Therefore, you will need to get your own api_key if you want to use the language detection function.
    I figured out you can get one for free here: https://detectlanguage.com/documentation

- Single Text Detection

.. code-block:: python

    lang = single_detection('bonjour la vie', api_key='your_api_key')
    print(lang) # output: fr

- Batch Detection

.. code-block:: python

    lang = batch_detection(['bonjour la vie', 'hello world'], api_key='your_api_key')
    print(lang) # output: [fr, en]



Google Translate
-----------------

.. code-block:: python

    text = 'happy coding'

- You can use automatic language detection to detect the source language:

.. code-block:: python

    translated = GoogleTranslator(source='auto', target='german').translate(text=text)

- You can pass languages by name:

.. code-block:: python

    translated = GoogleTranslator(source='english', target='german').translate(text=text)

- Alternatively, you can pass languages by their abbreviation:

.. code-block:: python

    translated = GoogleTranslator(source='en', target='de').translate(text=text)

- Translate from a file:

.. code-block:: python

    translated = GoogleTranslator(source='auto', target='german').translate_file('path/to/file')

- Automate translation by detecting the source language and translate it automatically to the desired language

.. code-block:: python

    # or maybe you have many sentences in different languages and want to automate the translation process
    translated = GoogleTranslator(source='auto', target='de').translate_sentences([your_list_of_sentences])



PONS Translator
----------------

.. note::

    You can pass the languages by the name or by abbreviation just like
    previous examples using GoogleTranslate

.. code-block:: python

    word = 'awesome'

- Simple Translation

.. code-block:: python

    translated_word = PonsTranslator(source='english', target='french').translate(word)

    # pass language by their abbreviation
    translated_word = PonsTranslator(source='en', target='fr').translate(word)

- Return all synonyms or words that matches

.. code-block:: python

    # set the argument return_all to True if you want to get all synonyms of the word to translate
    translated_word = PonsTranslator(source='english', target='french').translate(word, return_all=True)



Linguee Translator
-------------------


.. code-block:: python

    word = 'good'

- Simple Translation

.. code-block:: python

    translated_word = LingueeTranslator(source='english', target='french').translate(word)

    # pass language by their abbreviation
    translated_word = LingueeTranslator(source='en', target='fr').translate(word)

- Return all synonyms or words that matches

.. code-block:: python

    # set the argument return_all to True if you want to get all synonyms of the word to translate
    translated_word = LingueeTranslator(source='english', target='french').translate(word, return_all=True)


Mymemory Translator
--------------------

.. note::

    You can use the automatic language detection with mymemory by passing
    "auto" as a value for the source language

.. code-block:: python

    text = 'Keep it up. You are awesome'

    translated = MyMemoryTranslator(source='auto', target='french').translate(text)

Usage from Terminal
--------------------

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

Side Hint
----------

Generally, I find the google and mymemory translators suitable for translating sentences, whereas
the pons and linguee translators are good choices if you want to translate words.

========
Links
========
Check this article on medium to know why you should use the deep-translator package and how to translate text using python.
https://medium.com/@nidhalbacc/how-to-translate-text-with-python-9d203139dcf5


==========
Next Steps
==========

Take a look in the examples folder for more :)
Contributions are always welcome.
Read the Contribution guildlines `Here <https://deep-translator.readthedocs.io/en/latest/contributing.html/>`_

===========================
The Translator++ mobile app
===========================

.. image:: assets/app-icon.png
    :width: 100
    :alt: Icon of the app


After developing the deep_translator, I realised how cool this would be if I can use it as an app on my mobile phone.
Sure, there is google translate, pons and linguee apps etc.. but isn't it cooler to make an app where all these
translators are integrated?

Long story short, I started working on the app. I decided to use the `kivy framework <https://kivy.org/#home/>`_ since
I wanted to code in python and to develop a cross platform app.
I open sourced the `Translator++ app <https://github.com/nidhaloff/deep-translator-app/>`_ on my github too.
Feel free to take a look at the code or make a pull request ;)

.. note::
    The Translator++ app is based on the deep_translator package. I just built the app to prove the capabilities
    of the deep_translator package ;)

I published the first release on google play store on 02-08-2020

Here are some screenshots:

- Phone

.. image:: assets/translator1.jpg
    :width: 30%
    :height: 200
    :alt: screenshot1
.. image:: assets/translator2.jpg
    :width: 30%
    :height: 200
    :alt: screenshot2
.. image:: assets/spinner.jpg
    :width: 30%
    :height: 200
    :alt: spinner

- Tablet:

.. image:: assets/hz_view.png
    :width: 100%
    :height: 300
    :alt: screenshot3

