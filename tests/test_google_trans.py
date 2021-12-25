#!/usr/bin/env python

"""Tests for `deep_translator` package."""

import pytest
from deep_translator import exceptions, GoogleTranslator
from deep_translator.constants import GOOGLE_CODES_TO_LANGUAGES


test_text_standard = 'Hello world.'

TRANSLATED_RESULTS = {
    "afrikaans": "Hello Wêreld.",
    "albanian": "Përshendetje Botë.",
    "amharic": "ሰላም ልዑል.",
    "arabic": "مرحبا بالعالم.",
    "armenian": "Բարեւ աշխարհ.",
    "azerbaijani": "Salam dünya.",
    "basque": "Kaixo Mundua.",
    "belarusian": "Прывітанне Сусвет.",
    "bengali": "ওহে বিশ্ব.",
    "bosnian": "Zdravo svijete.",
    "bulgarian": "Здравей свят.",
    "catalan": "Hola món.",
    "cebuano": "Kumusta kalibutan.",
    "chichewa": "Moni Dziko Lapansi.",
    "chinese (simplified)": "你好，世界。",
    "chinese (traditional)": "你好，世界。",
    "corsican": "Bonghjornu mondu.",
    "croatian": "Pozdrav svijete.",
    "czech": "Ahoj světe.",
    "danish": "Hej Verden.",
    "dutch": "Hallo Wereld.",
    "esperanto": "Saluton mondo.",
    "estonian": "Tere, Maailm.",
    "filipino": "Kamusta mundo",
    "finnish": "Hei maailma.",
    "french": "Bonjour le monde.",
    "frisian": "Hallo wrâld.",
    "galician": "Ola mundo.",
    "georgian": "Გამარჯობა მსოფლიო.",
    "german": "Hallo Welt.",
    "greek": "Γειά σου Κόσμε.",
    "gujarati": "હેલો વર્લ્ડ.",
    "haitian creole": "Bonjou mond.",
    "hausa": "Sannu Duniya.",
    "hawaiian": "Aloha honua.",
    "hebrew": "שלום עולם.",
    "hindi": "नमस्ते दुनिया।",
    "hmong": "Nyob zoo ntiaj teb.",
    "hungarian": "Helló Világ.",
    "icelandic": "Halló heimur.",
    "igbo": "Ndewo Ụwa.",
    "indonesian": "Halo Dunia.",
    "irish": "Dia duit ar domhan.",
    "italian": "Ciao mondo.",
    "japanese": "こんにちは世界。",
    "javanese": "Halo jagad.",
    "kannada": "ಹಲೋ ವಿಶ್ವ.",
    "kazakh": "Сәлем Әлем.",
    "khmer": "សួស្តី​ពិភពលោក។",
    "kinyarwanda": "Mwaramutse isi.",
    "korean": "안녕하세요 세계입니다.",
    "kurdish": "Hello cîhanê.",
    "kyrgyz": "Салам дүйнө.",
    "lao": "ສະ​ບາຍ​ດີ​ຊາວ​ໂລກ.",
    "latin": "Salve mundi.",
    "latvian": "Sveika pasaule.",
    "lithuanian": "Labas pasauli.",
    "luxembourgish": "Moien Welt.",
    "macedonian": "Здраво свету.",
    "malagasy": "Hello World.",
    "malay": "Hai dunia.",
    "malayalam": "ഹലോ വേൾഡ്.",
    "maltese": "Hello dinja.",
    "maori": "Kia ora te ao.",
    "marathi": "नमस्कार जग.",
    "mongolian": "Сайн уу ертөнц.",
    "myanmar": "မင်္ဂလာပါကမ္ဘာလောက။",
    "nepali": "नमस्कार संसार।",
    "norwegian": "Hei Verden.",
    "odia": "ନମସ୍କାର ବିଶ୍ୱବାସି।",
    "pashto": "سلام نړی.",
    "persian": "سلام دنیا.",
    "polish": "Witaj świecie.",
    "portuguese": "Olá Mundo.",
    "punjabi": "ਸਤਿ ਸ੍ਰੀ ਅਕਾਲ ਦੁਨਿਆ.",
    "romanian": "Salut Lume.",
    "russian": "Привет, мир.",
    "samoan": "Talofa lalolagi.",
    "scots gaelic": "Hàlo a Shaoghail.",
    "serbian": "Здраво Свете.",
    "sesotho": "Lefatše Lumela.",
    "shona": "Mhoro nyika.",
    "sindhi": "هيلو دنيا.",
    "sinhala": "හෙලෝ වර්ල්ඩ්.",
    "slovak": "Ahoj svet.",
    "slovenian": "Pozdravljen, svet.",
    "somali": "Salaamu calaykum.",
    "spanish": "Hola Mundo.",
    "sundanese": "Halo Dunya.",
    "swahili": "Salamu, Dunia.",
    "swedish": "Hej världen.",
    "tajik": "Салом Ҷаҳон.",
    "tamil": "வணக்கம் உலகம்.",
    "tatar": "Сәлам, Дөнья.",
    "telugu": "హలో వరల్డ్.",
    "thai": "สวัสดีชาวโลก.",
    "turkish": "Selam Dünya.",
    "turkmen": "Salam dünýä.",
    "ukrainian": "Привіт Світ.",
    "urdu": "سلام دنیا۔",
    "uyghur": "ياخشىمۇسىز دۇنيا.",
    "uzbek": "Salom Dunyo.",
    "vietnamese": "Chào thế giới.",
    "welsh": "Helo Byd.",
    "xhosa": "Molo Lizwe.",
    "yiddish": "העלא וועלט.",
    "yoruba": "Mo ki O Ile Aiye.",
    "zulu": "Sawubona Mhlaba."
}


@pytest.fixture
def google_translator():
    """Sample pytest fixture.
    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    return GoogleTranslator(target='en')


def test_content(google_translator):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string
    assert google_translator.translate(text='좋은') == "good"

def test_abbreviations_and_languages_mapping():
    for abb, lang in GOOGLE_CODES_TO_LANGUAGES.items():
        if abb != 'en':
            g1 = GoogleTranslator(abb)
            g2 = GoogleTranslator(lang)
            assert g1._source == g2._source

def test_inputs():
    with pytest.raises(exceptions.LanguageNotSupportedException):
        GoogleTranslator(source="", target="")

    with pytest.raises(exceptions.LanguageNotSupportedException):
        GoogleTranslator(source="auto", target="nothing")

def test_payload(google_translator):

    with pytest.raises(exceptions.NotValidPayload):
        google_translator.translate(text="")
        google_translator.translate(text='1234')
        google_translator.translate(text='{}')
        google_translator.translate(text='%@')

    with pytest.raises(exceptions.NotValidPayload):
        google_translator.translate(text=123)

    with pytest.raises(exceptions.NotValidPayload):
        google_translator.translate(text={})

    with pytest.raises(exceptions.NotValidPayload):
        google_translator.translate(text=[])

    with pytest.raises(exceptions.NotValidLength):
        google_translator.translate("a"*5001)

def test_one_character_words():
    assert GoogleTranslator(source='es', target='en').translate('o') == 'or'
