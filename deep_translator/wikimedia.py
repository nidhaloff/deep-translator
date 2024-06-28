# wikimedia.py

import requests

class WikimediaTranslator:
    def __init__(self, source='en', target='fr'):
        self.source = source
        self.target = target
        self.base_url = 'https://translate.wmcloud.org/api/translate'

    def translate(self, text):
        data = {
            'format': 'text',  # Assuming the format is 'text'
            'content': text,
            'source_language': self.source,
            'target_language': self.target
        }
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.post(self.base_url, json=data, headers=headers)
        print("Request Data:", data)  # Debugging line
        print("Response Status Code:", response.status_code)  # Debugging line
        print("Response Text:", response.text)  # Debugging line
        response.raise_for_status()
        return response.json()['translation']
