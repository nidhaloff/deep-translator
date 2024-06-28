# test_wikimedia.py

import unittest
from deep_translator import WikimediaTranslator

class TestWikimediaTranslator(unittest.TestCase):
    def test_translate(self):
        translator = WikimediaTranslator(source='en', target='fr')
        result = translator.translate('hello')
        self.assertEqual(result, 'Je vous salue .')  # Adjust according to actual API response

if __name__ == '__main__':
    unittest.main()
