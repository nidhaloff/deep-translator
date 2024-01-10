from deep_translator import GlosbeTranslator

res = GlosbeTranslator(source="en",target="zh").translate("What is Lorem Ipsum? Lorem Ipsum is simply dummy text of the printing and typesetting industry.")

print(res)