=====
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
