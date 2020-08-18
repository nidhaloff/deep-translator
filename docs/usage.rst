=====
Usage
=====


In this section, demos on how to use all different integrated translators in this tool are provided.
This includes the google, pons, linguee and mymemory translator (at least for now). Perhaps more
translators will be integrated in the future.

.. note::

    You can always pass the languages by the name or by abbreviation.

    *Example*: If you want to use english as a source or target language, you can pass **english** or **en** as an argument

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

    translated = GoogleTranslator(source='auto', target='de').translate(text=text)

- You can pass languages by name:

.. code-block:: python

    translated = GoogleTranslator(source='auto', target='german').translate(text=text)

- Alternatively, you can pass languages by their abbreviation:

.. code-block:: python

    translated = GoogleTranslator(source='en', target='de').translate(text=text)

- Translate from a file:

.. code-block:: python

    translated = GoogleTranslator(source='auto', target='german').translate_file('path/to/file')

- Automate translation by detecting the source language and translate it automatically to the desired language

.. code-block:: python

    # this is useful if you have many sentences in different languages and want to automate the translation process
    translated = GoogleTranslator(source='auto', target='de').translate_sentences([your_list_of_sentences])


Mymemory Translator
--------------------

.. note::

    As in google translate, you can use the automatic language detection with mymemory by using "auto" as an
    argument for the source language. However, this feature in the mymemory translator is not so powerful as
    in google translate.

- Simple translation

.. code-block:: python

    text = 'Keep it up. You are awesome'

    translated = MyMemoryTranslator(source='auto', target='french').translate(text)

- Translate a list of sentences or paragraphs

.. code-block:: python

    texts = ["hallo welt", "guten morgen"]
    translated = MyMemoryTranslator('de', 'english').translate_sentences(texts)

- Translate from file

.. code-block:: python

    path = "your_file.txt"

    translated = MyMemoryTranslator(source='en', target='fr').translate_file(path)



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

- Translate a batch of words

.. code-block:: python

    translated_words = LingueeTranslator(source='english', target='french').translate_words(["good", "awesome"])

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

- Translate a batch of words

.. code-block:: python

    translated_words = LingueeTranslator(source='english', target='french').translate_words(["good", "awesome"])

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
