from deep_translator import GoogleTranslator

english_text = 'happy coding'
chinese_text = '這很好'
result_german = GoogleTranslator(source='english', target='german').translate(payload=english_text)
result_french = GoogleTranslator(source='auto', target='french').translate(payload=chinese_text)

print(f"original english text: {english_text} | translated text: {result_german}")  # result: fröhliche Codierung
print(f"original chinese text: {chinese_text} | translated text: {result_french}")  # result: C' est bon

