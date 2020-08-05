
import requests
from bs4 import BeautifulSoup


# res = requests.get('https://translate.google.com/?sl=auto&tl=en#view=home&op=translate&sl=auto&tl=de&text=cute')
# soup = BeautifulSoup(res.text, 'html.parser')
# print(soup)
# a = soup.find('div', {'class': 'goog-inline-block jfk-button jfk-button-standard jfk-button-collapse-right jfk-button-checked'})

# print(a)
from bs4 import BeautifulSoup
from requests_html import HTMLSession

session = HTMLSession()
r = session.get('https://translate.google.com/m?hl=en&sl=auto&tl=de&ie=UTF-8&prev=_m&q=here+is+a+sentence')
r.html.render()

print(r.html.html)
#soup = BeautifulSoup(r.html.html, 'html.parser')

