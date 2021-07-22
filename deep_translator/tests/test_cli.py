#!/usr/bin/env python

"""Tests for the CLI interface."""

from click.testing import CliRunner
from deep_translator import main

def results_test():
    runner = CliRunner()
    result = runner.invoke(main.translate, [ 'google', 'auto', 'en', '좋은'])
    assert result.exit_code == 0
    assert result == 'good'
    
    api_error = runner.invoke(main.translate, ['microsoft','auto','en','Zwei minimale Dellchen auf der Rückseite.'])
    assert api_error.exit_code == 0
    assert api_error == "This translator requires an api key provided through --api-key"

    language_list_test = runner.invoke(main.languages, ['google'])
    assert language_list_test.exit_code == 0

    language_list_invalid_test = runner.invoke(main.languages, ['notValidTranslator'])
    assert language_list_invalid_test.exception == AttributeError