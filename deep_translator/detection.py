"""
Language Detection API
"""
import sys
import requests
from requests.exceptions import HTTPError

# Module global config
config = {"url": 'https://ws.detectlanguage.com/0.2/detect',
          "headers": {'User-Agent': 'Detect Language API Python Client 1.4.0', 'Authorization': 'Bearer {}', }}


def get_request_body(text, api_key, *_, **__):
    """
    Send a request and return the response body parsed as dictionary
    Args:
        text: str: target text that you want to detect its language.
        api_key: str: your private API key.
    Raises:
        HTTPError
        Exception
    """
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
            print("Error occurred while requesting from server: ", e.args, file=sys.stderr)
            raise e


def single_detection(text, api_key=None, detailed=False, *_, **__):
    """
    Function responsible for detecting the language from a text
    Args:
        text: str: target text that you want to detect its language.
        api_key: str: your private API key.
        detailed: bool: set to True if you want to get detailed information about the detection process.
    Returns:
        None or str
    """
    body = get_request_body(text, api_key)
    detections = body.get('detections')
    if detailed:
        return detections[0]

    lang = detections[0].get('language', None)
    if lang:
        return lang


def batch_detection(text_list, api_key, detailed=False, *_, **__):
    """
    Function responsible for detecting the language from a text
    Args:
        text_list: list:target batch that you want to detect its language
        api_key: str: your private API key
        detailed: bool: set to True if you want to get detailed information about the detection process
    Returns:
        str or list of languages
    """
    body = get_request_body(text_list, api_key)
    detections = body.get('detections')
    res = [obj[0] for obj in detections]
    if detailed:
        return res
    else:
        return [obj['language'] for obj in res]
