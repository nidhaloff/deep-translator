from deep_translator import LingueeTranslator

res = LingueeTranslator(source="german", target="english").translate(
    "laufen", return_all=False
)

print(res)
