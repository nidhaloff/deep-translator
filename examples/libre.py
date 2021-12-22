from deep_translator import LibreTranslator

res = LibreTranslator(source='de', target='en').translate('laufen')

print(res)
