
from deep_translator import PonsTranslator


res = PonsTranslator(source='de', target='en').translate('übersetzen', return_all=False)

print(res)
