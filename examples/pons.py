
from deep_translator import PonsTranslator


res = PonsTranslator(source='de', target='en').translate('übersetzen', return_all=False)


e2a = PonsTranslator('ar', 'en').translate('آخُذ اَلْباص.', return_all=True)

print(e2a)
