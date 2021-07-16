#!/usr/bin/env python

"""Tests for the CLI interface."""

from click.testing import CliRunner
from deep_translator import cli

def results_test():
    runner = CliRunner()
    result = runner.invoke(cli.main, [ 'google', 'auto', 'en', '좋은'])
    assert result.exit_code == 0
    assert result == 'good'
    
    api_error = runner.invoke(cli.main, ['microsoft','auto','en','Zwei minimale Dellchen auf der Rückseite.'])
    assert api_error.exit_code == 0
    assert api_error == "This translator requires an api key provided through --api-key"