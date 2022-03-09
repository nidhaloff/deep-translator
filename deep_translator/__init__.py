"""Top-level package for Deep Translator"""

from .google import GoogleTranslator
from .pons import PonsTranslator
from .linguee import LingueeTranslator
from .mymemory import MyMemoryTranslator
from .yandex import YandexTranslator
from .qcri import QcriTranslator
from .deepl import DeeplTranslator
from .detection import single_detection, batch_detection
from .microsoft import MicrosoftTranslator
from .papago import PapagoTranslator
from .libre import LibreTranslator

__author__ = """Nidhal Baccouri"""
__email__ = 'nidhalbacc@gmail.com'
__version__ = '1.7.1'

__all__ = [
    "GoogleTranslator",
    "PonsTranslator",
    "LingueeTranslator",
    "MyMemoryTranslator",
    "YandexTranslator",
    "MicrosoftTranslator",
    "QcriTranslator",
    "DeeplTranslator",
    "LibreTranslator",
    "PapagoTranslator",
    "single_detection",
    "batch_detection"
]
