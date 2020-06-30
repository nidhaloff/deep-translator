from deep_translator import GoogleTranslator, PonsTranslator, LingueeTranslator


# examples using google translate

english_text = 'happy coding'
chinese_text = '這很好'

result_german = GoogleTranslator(source='english', target='german').translate(text=english_text)
result_french = GoogleTranslator(source='auto', target='french').translate(text=chinese_text)

print(f"original english text: {english_text} | translated text: {result_german}")  # result: fröhliche Codierung
print(f"original chinese text: {chinese_text} | translated text: {result_french}")  # result: C' est bon

# examples using linguee:
text = 'cute'
translated = LingueeTranslator(source='english', target='german').translate(word=text)
print("Using Linguee ==> the translated text: ", translated)

# examples using pons:
text = 'good'
translated = PonsTranslator(source='english', target='arabic').translate(word=text)
print("using Pons ==> the translated text: ", translated)
