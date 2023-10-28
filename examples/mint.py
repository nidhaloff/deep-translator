from deep_translator import WikimediaMinTMachineTranslator

res = WikimediaMinTMachineTranslator(source="en",target="ace").translate("What is Lorem Ipsum? Lorem Ipsum is simply dummy text of the printing and typesetting industry.")

print(res)

# if you want detailed response then set detail=True
res = WikimediaMinTMachineTranslator(source="en",target="ace").translate("What is Lorem Ipsum? Lorem Ipsum is simply dummy text of the printing and typesetting industry.",detail=True)

print(res)
