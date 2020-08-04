import requests
from deep_translator.configs import config


def detect_language(text):
    """
    function responsible for detecting the language from a text
    """
    response = requests.post(config['url'],
                        json={'q': text},
                        headers=config['headers'])

    body = response.json().get('data')
    detections = body.get('detections')
    lang = detections[0].get('language', None)
    if lang:
        return lang


# lang = detect_language('你好可爱')
# print("detected lang: ", lang)
