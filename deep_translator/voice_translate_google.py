# Importing necessary modules required
import speech_recognition as spr
from googletrans import Translator
from gtts import gTTS
import playsound
import googletrans

#Creating a dictionary to convert the language to respective code to be used with google translate
code_language_dict = (googletrans.LANGUAGES)
language_code_dict = dict([(value, key) for key, value in code_language_dict.items()])
#print(language_code_dict)

# Creating Recogniser() class object
recog1 = spr.Recognizer()

# Creating microphone instance
mc = spr.Microphone()

# Capture Voice
with mc as source:
    print("Speak 'hello' to initiate the Translation !")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    recog1.adjust_for_ambient_noise(source, duration=0.2)
    audio = recog1.listen(source)
    MyText = recog1.recognize_google(audio)
    MyText = MyText.lower()

# Here initialising the recorder with
# hello, whatever after that hello it
# will recognise it.
if 'hello' in MyText:

    # Translator method for translation
    translator = Translator()

    # short form of english in which
    # you will speak, following code can be uncommented and used to give the user input, by default input is taken in english and 
    #translation is done in hindi language
    #src_language = input("Type your language")
    #from_lang = language_code_dict[src_language]
    from_lang = 'en'
    # In which we want to convert, short
    # form of hindi
    to_lang = 'hi'

    with mc as source:

        print("Speak sentence that's to be translated...")
        recog1.adjust_for_ambient_noise(source, duration=1.2)

        # Storing the speech into audio variable
        audio = recog1.listen(source)

        # Using recognize.google() method to
        # convert audio into text
        get_sentence = recog1.recognize_google(audio)

        # Using try and except block to improve
        # its efficiency.
        try:

            # Printing Speech which need to
            # be translated.
            print("Phase to be Translated :" + get_sentence)

            # Using translate() method which requires
            # three arguments, 1st the sentence which
            # needs to be translated 2nd source language
            # and 3rd to which we need to translate in
  #          text_to_translate = translator.translate(get_sentence, lang_src=from_lang, lang_tgt=to_lang)
            text_to_translate = translator.translate(get_sentence, dest =to_lang)

            # Storing the translated text in text
            # variable
            text = text_to_translate.text
            print(text)
            # Using Google-Text-to-Speech ie, gTTS() method
            # to speak the translated text into the
            # destination language which is stored in to_lang.
            # Also, we have given 3rd argument as False because
            # by default it speaks very slowly
            speak = gTTS(text=text, lang=to_lang, slow=False)
            #playsound.playsound(speak)
            # Using save() method to save the translated
            # speech in capture_voice.mp3
            speak.save("captured_voice.mp3")

            #Used to play the sound, Make sure the volume is up
            playsound.playsound("captured_voice.mp3")

        # Here we are using except block for UnknownValue
        # and Request Error and printing the same to
        # provide better service to the user.
        except spr.UnknownValueError:
            print("Unable to Understand the Input")

        except spr.RequestError as e:
            print("Unable to provide Required Output".format(e))

