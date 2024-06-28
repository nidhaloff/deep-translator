# glosbe.py

import requests

class GlosbeTranslator:
    def __init__(self, source='auto', target='en'):
        self.source = source
        self.target = target
        self.base_url = 'https://api.glosbe.com/translate'

    def translate(self, text):
        params = {
            'from': self.source,
            'dest': self.target,
            'phrase': text,
            'format': 'json'
        }
        response = requests.get(self.base_url, params=params)
        response.raise_for_status()
        return response.json()['tuc'][0]['phrase']['text']
