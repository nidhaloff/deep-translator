#!/usr/bin/env python

"""Tests for `deep_translator` package."""

from click.testing import CliRunner
import cli

def cli():
    runner = CliRunner()
    result = runner.invoke(cli.translate, [ 'google', 'auto', 'en', '좋은'])
    assert result.exit_code == 0
    assert result == 'good'