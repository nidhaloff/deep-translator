.. highlight:: shell

============
Contributing
============

Contributions are welcome, and they are greatly appreciated! Every little bit
helps, and credit will always be given.

You can contribute in many ways:

Types of Contributions
----------------------

Report Bugs
~~~~~~~~~~~

Report bugs at https://github.com/nidhaloff/deep_translator/issues.

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.
* If the bug includes a tracelog, include that in your bug report. Remember on github, you can enclose code or console output in ``` insert code here ```.

Fix Bugs
~~~~~~~~

Look through the GitHub issues for bugs. Anything tagged with "bug" and "help wanted" is open to whoever wants to implement it.

Implement Features
~~~~~~~~~~~~~~~~~~

Look through the GitHub issues for features. Anything tagged with "enhancement" and "help wanted" is open to whoever wants to implement it.

.. note::

    You can contact @nothead31 or comment on the issue if you wish to be listed under 'Assigned'.

Write Documentation
~~~~~~~~~~~~~~~~~~~

deep_translator could always use more documentation, whether as part of the official deep_translator docs, in docstrings, or even on the web in blog posts, articles, and such. If you do a write-up on your own site, please let us know and we will add a link to it in the official documentation!

Submit Feedback
~~~~~~~~~~~~~~~

The best way to send feedback is to file an issue at https://github.com/nidhaloff/deep_translator/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

Get Started!
------------

Ready to contribute? Here's how to set up `deep_translator` for local development.

1. Fork the `deep_translator` repo on GitHub.
2. Clone your fork locally::

    $ git clone git@github.com:your_name_here/deep_translator.git

3. Install your local copy into a virtualenv. Assuming you have virtualenvwrapper installed, this is how you set up your fork for local development::

    $ cd path/to/project
    $ poetry shell
    $ poetry install

 .. note::

    ``poetry install`` will automatically install all package dependencies AND development dependencies. If you only want to run the package, append --no-dev to the command.

4. Create a branch for local development::

    $ git checkout -b name-of-your-bugfix-or-feature

   Now you can make your changes locally.

5. Ensure your changes are covered by test modules and that the tests pass with pytest before committing.

6. Commit your changes and push your branch to GitHub::

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature

7. Submit a pull request through the GitHub website.

Pull Request Guidelines
-----------------------

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include any relevant tests (located under :file:`.deep_translator/tests`)
2. If the pull request adds functionality, the docs should be updated. Put your new functionality into a function with a docstring, and add the feature to the list in README.rst.
3. Pull requests are automatically tested on GitHub for compatability with Python version 3.7, 3.8, and 3.9. Please review your test results and ensure your request passes all tests.

Tips
----

To run only certain tests::

   $ pytest -ra

.. note::

   will run all tests, excluding any that previously passed, and provides a simple test report.

    $ pytest test_mod.py

.. note::

   Runs only the tests in the named testing module. Useful for only testing a subset of functionality.

Deploying
---------

A reminder for the maintainers on how to deploy.
Make sure all your changes are committed (including an entry in HISTORY.rst).
Then run::

   $ poetry version major|minor|patch
   $ git push
   $ git push --tags

After pushing a new version to the master branch, github will build a package and upload it to PyPI.