=====
Usage
=====


In this section, demos on how to use all different integrated translators are provided.

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
                                 YandexTranslator,
                                 DeepL,
                                 QCRI,
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

- You can pass languages by name or by abbreviation:

.. code-block:: python

    translated = GoogleTranslator(source='auto', target='german').translate(text=text)

    # Alternatively, you can pass languages by their abbreviation:
    translated = GoogleTranslator(source='en', target='de').translate(text=text)

- Translate batch of texts

.. code-block:: python

    texts = ["hallo welt", "guten morgen"]

    # the translate_sentences function is deprecated, use the translate_batch function instead
    translated = GoogleTranslator('de', 'en').translate_batch(texts)

- Translate from a file:

.. code-block:: python

    translated = GoogleTranslator(source='auto', target='german').translate_file('path/to/file')

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

- Translate batch of texts

.. code-block:: python

    texts = ["hallo welt", "guten morgen"]

    # the translate_sentences function is deprecated, use the translate_batch function instead
    translated = MyMemoryTranslator('de', 'en').translate_batch(texts)

- Translate from file

.. code-block:: python

    path = "your_file.txt"

    translated = MyMemoryTranslator(source='en', target='fr').translate_file(path)


DeepL Translator
-----------------

.. note::

    In order to use the DeepL translator, you need to generate an api key. Visit https://www.deepl.com/en/docs-api/
    for more information

- Simple translation

.. code-block:: python

    text = 'Keep it up. You are awesome'

    translated = DeepL("your_api_key").translate(text)

- Translate batch of texts

.. code-block:: python

    texts = ["hallo welt", "guten morgen"]

    # the translate_sentences function is deprecated, use the translate_batch function instead
    translated = DeepL("your_api_key").translate_batch(texts)

QCRI Translator
--------------------

.. note::

    In order to use the QCRI translator, you need to generate a free api key. Visit https://mt.qcri.org/api/
    for more information

- Check languages

.. code-block:: python

    # as a property
    print("language pairs: ", QCRI("your_api_key").languages)

- Check domains

.. code-block:: python

    # as a property
    print("domains: ", QCRI("your_api_key").domains)

- Text translation

.. code-block:: python

    text = 'Education is great'

    translated = QCRI("your_api_key").translate(source='en', target='ar', domain="news", text=text)
    # output -> التعليم هو عظيم

    # see docs for batch translation and more.

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

Yandex Translator
------------------

.. note::

    You need to require an **private api key** if you want to use the yandex translator.
    visit the official website for more information about how to get one

- Language detection

.. code-block:: python

    lang = YandexTranslator('your_api_key').detect('Hallo, Welt')
    print(f"language detected: {lang}")  # output -> language detected: 'de'

- Text translation

.. code-block:: python

    # with auto detection | meaning provide only the target language and let yandex detect the source
    translated = YandexTranslator('your_api_key').translate(source="auto", target="en", text='Hallo, Welt')
    print(f"translated text: {translated}")  # output -> translated text: Hello world

    # provide source and target language explicitly
    translated = YandexTranslator('your_api_key').translate(source="de", target="en", text='Hallo, Welt')
    print(f"translated text: {translated}")  # output -> translated text: Hello world

- File translation

.. code-block:: python

    translated = YandexTranslator('your_api_key').translate_file(source="auto", target="en", path="path_to_your_file")

- Batch translation

.. code-block:: python

    translated = YandexTranslator('your_api_key').translate_batch(source="auto", target="de", batch=["hello world", "happy coding"])

Libre Translator
---------------------

.. note::

    Libre translate has multiple  `mirrors <https://github.com/LibreTranslate/LibreTranslate#mirrors>`_ which can be used for the API endpoint.
    Some require an API key to be used. By default the base url is set to `libretranslate.de <https://libretranslate.de/>`_ . 
    This can be set using the "base_url" input parameter.

.. code-block:: python

    text = 'laufen'
    translated = LibreTranslator(source='auto', target='en', base_url = 'https://libretranslate.com/', api_key = 'your_api_key').translate(text=text)  # output: run


- You can pass languages by name or by abbreviation:

.. code-block:: python

    translated = LibreTranslator(source='german', target='english').translate(text=text)

    # Alternatively, you can pass languages by their abbreviation:
    translated = LibreTranslator(source='de', target='en').translate(text=text)


- Translate batch of texts

.. code-block:: python

    texts = ["hallo welt", "guten morgen"]
    translated = LibreTranslator(source='auto', target='en').translate_batch(texts)

- Translate from a file:

.. code-block:: python

    translated = LibreTranslator(source='auto', target='en').translate_file('path/to/file')

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
