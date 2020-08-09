
from deep_translator import PonsTranslator


res = PonsTranslator(source='en', target='de').translate('good', return_all=False)

print(res)
