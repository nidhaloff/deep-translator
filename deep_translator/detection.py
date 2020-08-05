import requests
from deep_translator.configs import config


def detect_language(text, api_key=None):
    """
    function responsible for detecting the language from a text
    """
    if not api_key:
        raise Exception("you need to get an API_KEY for this to work. "
                        "Get one for free here: https://detectlanguage.com/documentation")
    if not text:
        raise Exception("Please provide an input text")

    else:
        headers = config['headers']
        headers['Authorization'] = headers['Authorization'].format(api_key)

        try:
            response = requests.post(config['url'],
                                     json={'q': text},
                                     headers=headers)

            body = response.json().get('data')
            detections = body.get('detections')
            lang = detections[0].get('language', None)
            if lang:
                return lang

        except Exception as e:
            print("Error occured while requesting from server: ", e.args)
            raise e
