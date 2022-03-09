#!/usr/bin/env python

"""Tests for the CLI interface."""

import sys

import pytest

from deep_translator.cli import CLI


@pytest.fixture
def mock_args():
    sys.argv[1:] = ["--source", "en", "--target", "de", "--text", "hello"]
    return CLI(sys.argv[1:]).parse_args()


def test_source(mock_args):
    assert mock_args.source == "en"


def test_target(mock_args):
    assert mock_args.target == "de"
