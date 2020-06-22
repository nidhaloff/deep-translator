"""Top-level package for deep_translator."""

from .google_trans import GoogleTranslator
from .pons import PonsTranslator
from .linguee import LingueeTranslator

__author__ = """Nidhal Baccouri"""
__email__ = 'nidhalbacc@gmail.com'
__version__ = '1.0.0'

__all__ = [GoogleTranslator, PonsTranslator, LingueeTranslator]
