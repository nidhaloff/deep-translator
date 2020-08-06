
from deep_translator import LingueeTranslator


res = LingueeTranslator(source='de', target='en').translate('laufen', return_all=False)

print(res)
