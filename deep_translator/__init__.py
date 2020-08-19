"""Top-level package for deep_translator."""

from .google_trans import GoogleTranslator
from .pons import PonsTranslator
from .linguee import LingueeTranslator
from .mymemory import MyMemoryTranslator
from .detection import single_detection, batch_detection


__author__ = """Nidhal Baccouri"""
__email__ = 'nidhalbacc@gmail.com'
__version__ = '1.2.0'

__all__ = [GoogleTranslator,
           PonsTranslator,
           LingueeTranslator,
           MyMemoryTranslator,
           single_detection,
           batch_detection]
