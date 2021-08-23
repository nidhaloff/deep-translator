#!/usr/bin/env python

"""Tests for the CLI interface."""

from click.testing import CliRunner
from deep_translator.main import cli


class TestClass:
    def test_translate(self):
        runner = CliRunner()
        result = runner.invoke(cli, ['translate', 'google', '-src=auto', '-tgt=en', '-txt=좋은'])
        assert 'good' in result.output
        assert result.exit_code == 0

    def test_api_key_error(self):
        runner = CliRunner()
        result = runner.invoke(cli, ['translate', 'microsoft','-src=auto','-tgt=en','-txt=\'Zwei minimale Dellchen auf der Rückseite.\''])
        assert "This translator requires an api key provided through --api-key" in result.output
        assert result.exit_code == 1

    def test_language_languages(self):
        runner = CliRunner()
        result = runner.invoke(cli, ['languages', 'google'])
        assert result.exit_code == 0

    def test_invalid_language_languages(self):
        runner = CliRunner()
        result = runner.invoke(cli, ['languages', 'notValidTranslator'])
        assert 'The given translator is not supported.' in str(result.exception)
        assert result.exit_code == 1
