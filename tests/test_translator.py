import unittest
from deep_translator.new_translator import NewTranslator

class TestNewTranslator(unittest.TestCase):
    def setUp(self):
        self.translator = NewTranslator()

    def test_translation(self):
        result = self.translator.translate("Hello")
        self.assertEqual(result, "Translated Hello")

if __name__ == '__main__':
    unittest.main()
