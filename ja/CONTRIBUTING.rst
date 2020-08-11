.. highlight:: shell

============
コントリビュートする方法
============

このプロジェクトではあなたのコントリビュートを歓迎します！どんなに小さい貢献でも、コントリビューターとしてプロジェクトを支援することができます。

次の方法でコントリビュートすることができます。

コントリビュートの種類
----------------------

バグの報告
~~~~~~~~~~~

もしバグを発見したらhttps://github.com/nidhaloff/deep_translator/issues でバクを報告してください。

バグを報告する際にはトラブルシューティングしやすいように、以下の項目を含めて投稿するようにしてください。

* バグの発生したOSの種類とOSバージョンの情報
* ソフトウェアの設定などのローカル環境の情報
* バグを再現するための詳細な手順

バグの修正
~~~~~~~~

このリポジトリのイシューを見ることで、バグの情報を確認できます。
"bug" と "help wanted"でタグ付けされているものは、誰でもバグを修正にしてコントリビュートすることができます。

追加機能の実装
~~~~~~~~~~~~~~~~~~

このリポジトリのイシューを見ることで、実装待ちの機能が確認できます。
"enhancement" と "help wanted"でタグ付けされているものは、誰でも実装してコントリビュートすることができます。

ドキュメントの作成
~~~~~~~~~~~~~~~~~~~

deep_translator は、deep_translator の公式ドキュメントの一部、docstrings、あるいはウェブ上のブログ記事や記事など、常により多くのドキュメントを求めています。


新しい機能の提案
~~~~~~~~~~~~~~~

新しい提案をするには https://github.com/nidhaloff/deep_translator/issues に投稿してください。

新しい機能を提案するときには、以下の項目を留意してください:

* 新しい機能の動作をできるだけ詳しく説明してください。 
* 実装しやすいように機能の規模は限定するようにしてください。
* このプロジェクトがボランティアから成り立っていることと、コントリビュートを歓迎する精神を忘れないでください。
  

開発環境の構築
------------

コントリビュートの準備はできましたか？ここからは deep_translator の開発環境を構築する方法について説明します。

1. GitHub で deep_translator をフォークする.
2. フォークしたものをローカルリポジトリとしてクローンする。::

    $ git clone git@github.com:your_name_here/deep_translator.git

3. virtualenvの作成とインストールを行う。virtualenvwrapperがインストール済みとすると、以下のコマンドでローカルに開発環境を構築できる::

    $ mkvirtualenv deep_translator
    $ cd deep_translator /
    $ python setup.py develop

4. ローカルで開発を行うために新しいブランチを作成する::

    $ git checkout -b name-of-your-bugfix-or-feature

   これでローカルリポジトリに変更を加えることができるようになります。

5. 変更が終わったらflake8のコードチェックとテストを通過するようにする。この時、toxで複数バージョンのPythonで動作することを確認する::

    $ flake8 deep_translator tests
    $ python setup.py test or pytest
    $ tox

　　flake8とtoxのインストールは、virtualenvでpip installを行うことで可能です。

6. 変更をコミットし、自分のリモートリポジトリにプッシュする::

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature

7. GitHub からプルリクエストを送る.

プルリクエストにあたって
-----------------------

プルリクエストを送る前に以下のガイドラインに従っているか確認してください:

1. プルリクエストにテストが含まれている。

2. プルリクエストで機能が追加された場合、ドキュメントを更新する必要があります。新しい機能について関数内にdocstringで記述し、それに加えてリストREADME.rstのリストに追加してください。

3. プルリクエストによる変更はPython 3.5、3.6、3.7、3.8またはPyPyで動作することが望まれます。https://travisci.com/nidhaloff/deep_translator/pull_requests　を確認し、サポートされている全てのPythonバージョンでテストを通過することを確認してください。


ヒント
----

テストのサブセットを実行するには以下のコマンドが利用できます::

$ pytest tests.test_deep_translator


デプロイの方法
---------

メンテナンス担当者のためにデプロイの方法を記しておきます。まず、全ての変更がコミットされていることを確認してください。(HISTORY.rstのエントリを含む).
次に、以下のコマンドを実行します::

$ bump2version patch # possible: major / minor / patch
$ git push
$ git push --tags

Travisはテストを通過することを確認したら、PyPIにデプロイします。
