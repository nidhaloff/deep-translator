****************
deep_translator
****************


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
自然言語の翻訳ツール
=======================

複数の翻訳サービスを使って、簡単な方法で異なる言語間で柔軟に翻訳を **無料** かつ **無制限** に行えるツールです

* フリーソフトウェア: MIT ライセンス
* ドキュメント: https://deep-translator.readthedocs.io.

==========
開発の動機
==========

Pythonを使用してテキストを別の言語に翻訳するタスクがありました。しかし、それを行う簡単な方法を見つけるのは困難でした。なぜなら、このタスクに適用できるライブラリはいくつか存在しますが、それらのほとんどはバグが多いか、無料ではないか、何らかの制約があるか、全ての言語をサポートしていないか、使用するのが簡単ではありませんでした。

そこで、このタスクを簡単に行えるツールを作成することにしました。100％無料で無制限で使いやすく、すべての言語をサポートしています。

このツールの目的は、複数の有名な翻訳サービスをこのツールに統合することにあります。


======================
使用例
======================

- Pythonを使用してテキストを翻訳したい場合
- ファイルのテキストを翻訳したい場合
- 1つだけでなく、多くのソースから翻訳結果を取得したい場合
- 翻訳を自動化したい場合
- 異なる翻訳結果を比較したい場合
- 言語を自動検出したい場合

======================
このツールの強み
======================

- 高度な抽象化が施されている
- 言語を自動で検出する
- 拡張と使用が簡単である
- 多くの翻訳サービスを統合して扱える唯一のpythonツールである
- 安定している
- 有名な翻訳サービスをサポートしている

========
機能
========

* google翻訳のサポート
* Pons  (pons.com)のサポート
* Linguee のサポート
* Mymemory のサポート
* 自動言語検出
* テキストファイルから直接翻訳する
* 単語の複数の翻訳結果を取得する
* 異なる言語の異なる段落の翻訳を自動化する
* コマンドラインから直接翻訳する（バージョン1.1.0以上）

===============
インストール方法
===============

ツールの安定版をインストールする方法です:

.. code-block:: console

    $ pip install -U deep_translator

ソースからインストールを行いたい場合、ドキュメントを参照してください。

=======
使い方
=======

このセクションでは、このツールで様々な統合トランスレータを利用するデモを行います。このデモでは、google、pons、linguee、mymemoryの翻訳サービスを扱います（現時点）。将来的には、より多くの翻訳サービスを統合する予定です。

==========
インポート
==========

.. code-block:: python

    from deep_translator import (GoogleTranslator,
                                 PonsTranslator,
                                 LingueeTranslator,
                                 MyMemoryTranslator,
                                 detect_language)


サポートされている言語を確認する
============================

ポイント

  　関数get_supported_languagesを静的メソッドとして呼び出すことにより、各翻訳サービスでサポートしている言語を確認できます。

.. code-block:: python

    # デフォルトではリストを返します
    langs_list = GoogleTranslator.get_supported_languages()  # output: [arabic, french, english etc...]

    # 言語の省略形を辞書型にまとめて返すことも出来ます
    langs_dict = GoogleTranslator.get_supported_languages(as_dict=True)  # output: {arabic: ar, french: fr, english:en etc...}

言語検出
===================

ポイント

言語を自動的に検出することもできます。当然、このパッケージは無料です。言語検出機能を無料で使用する場合は、個人でapi_keyを取得する必要があります。ここで無料で入手することができます:https://detectlanguage.com/documentation

.. code-block:: python

    lang = detect_language('bonjour la vie', api_key='your_api_key')
    print(lang) # output: fr


Google 翻訳
=================

.. code-block:: python

    text = 'happy coding'

- ソースの言語に自動検出を使用できます:

.. code-block:: python

    translated = GoogleTranslator(source='auto', target='german').translate(text=text)

- ソースの言語の種類を指定することも出来ます:

.. code-block:: python

    translated = GoogleTranslator(source='english', target='german').translate(text=text)

- 言語名は省略形で指定することも可能です:

.. code-block:: python

    translated = GoogleTranslator(source='en', target='de').translate(text=text)

- ファイルから翻訳を行うことも出来ます:

.. code-block:: python

    translated = GoogleTranslator(source='auto', target='german').translate_file('path/to/file')


- ソースの言語を検出し、望んだ言語に自動翻訳することが出来ます。

.. code-block:: python

    # または、異なる言語の文章の翻訳を自動化したい時にも利用できます。
    translated = GoogleTranslator(source='auto', target='de').translate_sentences([your_list_of_sentences])




PONS
===============

ポイント

Google翻訳同様に言語の名前を指定して翻訳することが出来ます。省略形で指定することも可能です。

.. code-block:: python

    word = 'awesome'

- 簡単な翻訳方法

.. code-block:: python

    translated_word = PonsTranslator(source='english', target='french').translate(word)

    # 言語の省略形を指定する
    translated_word = PonsTranslator(source='en', target='fr').translate(word)


- 全ての同義語か一致する単語を返す

.. code-block:: python

    # 翻訳結果の全ての同義語を取得したい場合、引数にreturn_allにTrueを指定してください
    translated_word = LingueeTranslator(source='english', target='french').translate(word, return_all=True)



Linguee
===================


.. code-block:: python

    word = 'good'

- 簡単な翻訳方法

.. code-block:: python

    translated_word = LingueeTranslator(source='english', target='french').translate(word)

    # 言語の省略形を指定する
    translated_word = LingueeTranslator(source='en', target='fr').translate(word)

- 全ての同義語か一致する単語を返す

.. code-block:: python

    # 翻訳結果の全ての同義語を取得したい場合、引数にreturn_allにTrueを指定してください
    translated_word = LingueeTranslator(source='english', target='french').translate(word, return_all=True)


Mymemory
====================

ポイント

sourceに"auto"を渡すことでmymemoryの自動言語検出を使用できます。

.. code-block:: python

    text = 'Keep it up. You are awesome'

    translated = MyMemoryTranslator(source='auto', target='french').translate(text)

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


ヒント
==========

一般的に、google翻訳とmymemoryは文章に翻訳に適していますが、ponsとlingueeは単語の翻訳に適しています。

========
リンク
========

deep_translatorの使用目的やpythonで翻訳をする方法を確認するために以下のmediumの記事を確認してください。

https://medium.com/@nidhalbacc/how-to-translate-text-with-python-9d203139dcf5

===============================
スマートフォンアプリ Translator++
===============================

.. image:: ../../assets/app-icon.png
    :width: 100
    :alt: Icon of the app


deep_translatorを開発しみて、スマートフォンのアプリとして使用できれば便利なのではないかと思い立ちました。
google翻訳やpons、lingueeの個々のアプリは存在しますが、これらを統合して使用できるアプリを作れば便利ではないでしょうか。

それを出発点として、アプリの開発を開始しました。Pythonで作成しつつ、クロスプラットフォームのアプリを開発したかったので、`kivy フレームワーク <https://kivy.org/#home/>`_ を使用することにしました。
`Translator++ app <https://github.com/nidhaloff/deep-translator-app/>`_ もgithubでオープンソースとして公開しています。自由に編集やプルリクエストを行ってください;）

ポイント

Translator++はdeep_translatorパッケージがベースになっています。このアプリはパッケージの機能を試すために開発されています。

02-08-2020にGoogle Playで初公開されました。

スクリーンショット:

- スマートフォン :

.. image:: ../../assets/translator1.jpg
    :width: 30%
    :height: 200
    :alt: screenshot1
.. image:: ../../assets/translator2.jpg
    :width: 30%
    :height: 200
    :alt: screenshot2
.. image:: ../../assets/spinner.jpg
    :width: 30%
    :height: 200
    :alt: spinner

- タブレット:

.. image:: ../../assets/hz_view.png
    :width: 100%
    :height: 300
    :alt: screenshot3

=======================
次のステップに進むためには
=======================

詳細は examples フォルダを確認してください。
コントリビュートはいつでも歓迎しています。このパッケージが便利だと感じた方や使っている方がいたら、遠慮なくプルリクエストをしてフィードバックをください！
