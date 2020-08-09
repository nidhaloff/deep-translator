"""Top-level package for deep_translator."""

from .google_trans import GoogleTranslator
from .pons import PonsTranslator
from .linguee import LingueeTranslator
from .mymemory import MyMemoryTranslator
from .detection import detect_language


__author__ = """Nidhal Baccouri"""
__email__ = 'nidhalbacc@gmail.com'
__version__ = '1.1.6'

__all__ = [GoogleTranslator,
           PonsTranslator,
           LingueeTranslator,
           MyMemoryTranslator,
           detect_language]
