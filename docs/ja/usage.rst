=======
使い方
=======

.. code-block:: python

    from deep_translator import GoogleTranslator, PonsTranslator, LingueeTranslator, MyMemoryTranslator

    english_text = 'happy coding'

    result_german = GoogleTranslator(source='auto', target='de').translate(text=english_text)

    # 言語を名前で指定することもできます:
    translated = GoogleTranslator(source='english', target='german').translate(text=english_text)

    # テキストファイルを翻訳したい場合
    translated = GoogleTranslator(source='auto', target='german').translate_file('path/to/file')

    # 複数の言語の文章の翻訳を自動化したい場合
    translated = GoogleTranslator(source='auto', target='de').translate_sentences(your_list_of_sentences)


Ponsを利用することも出来ます: Pons.com


.. code-block:: python

    word = 'good'
    translated_word = PonsTranslator(source='english', target='french').translate(word)

    # 翻訳する単語の同義語を全て取得したい場合は、return_allにTrueを指定してください。
    translated_word = PonsTranslator(source='english', target='french').translate(word, return_all=True)


deep_translatorのバージョン1.0.0以上でLingueeをサポートしています:


.. code-block:: python

    word = 'good'
    translated_word = LingueeTranslator(source='english', target='french').translate(word)

    # 翻訳する単語の同義語を全て取得したい場合は、return_allにTrueを指定してください。
    translated_word = LingueeTranslator(source='english', target='french').translate(word, return_all=True)


Mymemoryはバージョン1.0.2以上でサポートされています:

.. code-block:: python

    word = 'good'
    translated_word = MyMemoryTranslator(source='english', target='french').translate(word)


ターミナルでの使用方法
====================

ターミナルからdeep_translatorをすぐに使用できます。使用するには、使用する翻訳サービス、翻訳元の言語、翻訳先の言語、翻訳するテキストなどを引数に指定する必要があります。
たとえば、Google翻訳を使用するには、引数として「google」を指定します。引数を変更することで、サポートされている他の翻訳サービスに切り替えることも可能です。ドキュメントを読んで、このツールでサポートされている翻訳サービスを確認してください。

.. code-block:: console

    $ deep_translator --translator "google" --source "english" --target "german" --text "happy coding"

以下のように短く記述することもできます:

.. code-block:: console

    $ deep_translator -trans "google" -src "english" -tg "german" -txt "happy coding"

翻訳元と翻訳先の言語を省略形で引数に指定することも出来ます。

.. code-block:: console

    $ deep_translator -trans "google" -src "en" -tg "de" -txt "happy coding"
