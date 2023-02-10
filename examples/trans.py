from deep_translator import GoogleTranslator, LingueeTranslator, PonsTranslator

# examples using google translate

english_text = "happy coding"
chinese_text = "這很好"
translator = GoogleTranslator(source="auto", target="german")
result1 = translator.translate(text=english_text)
result2 = translator.translate(text=chinese_text)

print(f"original english text: {english_text} | translated text: {result1}")
print(f"original chinese text: {chinese_text} | translated text: {result2}")

# file translation
result_file = translator.translate_file("./test.txt")
print("file translation: ", result_file)

# examples using linguee:
text = "cute"
translated = LingueeTranslator(source="english", target="german").translate(
    word=text
)
print("Using Linguee ==> the translated text: ", translated)

# examples using pons:
text = "good"
translated = PonsTranslator(source="en", target="ar").translate(word=text)
print("using Pons ==> the translated text: ", translated)
