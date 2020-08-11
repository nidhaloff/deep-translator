import requests
from deep_translator.configs import config
from requests.exceptions import HTTPError


def get_request_body(text, api_key, *args):

    if not api_key:
        raise Exception("you need to get an API_KEY for this to work. "
                        "Get one for free here: https://detectlanguage.com/documentation")
    if not text:
        raise Exception("Please provide an input text")

    else:
        try:
            headers = config['headers']
            headers['Authorization'] = headers['Authorization'].format(api_key)
            response = requests.post(config['url'],
                                     json={'q': text},
                                     headers=headers)

            body = response.json().get('data')
            return body

        except HTTPError as e:
            print("Error occured while requesting from server: ", e.args)
            raise e


def single_detection(text, api_key=None, detailed=False, *args, **kwargs):
    """
    function responsible for detecting the language from a text
    """
    body = get_request_body(text, api_key)
    detections = body.get('detections')
    if detailed:
        return detections[0]

    lang = detections[0].get('language', None)
    if lang:
        return lang


def batch_detection(text_list, api_key, detailed=False, *args):
    body = get_request_body(text_list, api_key)
    detections = body.get('detections')
    res = [obj[0] for obj in detections]
    if detailed:
        return res
    else:
        return [obj['language'] for obj in res]

