"""Top-level package for deep_translator."""

from deep_translator.google_trans import GoogleTranslator
from deep_translator.pons import PonsTranslator
from deep_translator.linguee import LingueeTranslator
from deep_translator.mymemory import MyMemoryTranslator
from deep_translator.yandex import YandexTranslator
from deep_translator.qcri import QCRI
from deep_translator.deepl import DeepL
from deep_translator.detection import single_detection, batch_detection
from deep_translator.microsoft import MicrosoftTranslator
from deep_translator.cli import main


__author__ = """Nidhal Baccouri"""
__email__ = 'nidhalbacc@gmail.com'
__version__ = '1.4.4'

__all__ = [GoogleTranslator,
           PonsTranslator,
           LingueeTranslator,
           MyMemoryTranslator,
           YandexTranslator,
           MicrosoftTranslator,
           QCRI,
           DeepL,
           main,
           single_detection,
           batch_detection]
