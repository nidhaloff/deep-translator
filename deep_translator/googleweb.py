# Requirement: pip3 install setuptools selenium undetected-chromedriver
# xpz3

import undetected_chromedriver as uc
import urllib.parse
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

class GoogleTranslatorWeb:
    """
    Google Translate scraper using headless Chrome by directly parsing the translation page.
    """

    def __init__(self, headless: bool = True, driver_wait: int = 3):
        """
        Initialize the translator.
        :param headless: Run Chrome in headless mode.
        """
        self.headless = headless
        self.driver_wait = driver_wait
        options = uc.ChromeOptions()
        if self.headless:
            options.headless = True
            options.add_argument("--headless=new")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--window-size=1200,800")

        self.driver = uc.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, self.driver_wait)

    def translate(self, text: str, source_lang: str = "auto", target_lang: str = "en") -> str:
        """
        Translate text using Google Translate by directly loading the translation page.
        :param text: The text to translate.
        :param source_lang: Source language (default: auto-detect).
        :param target_lang: Target language.
        :return: Full translated text.
        """
        if not text.strip():
            return ""

        encoded_text = urllib.parse.quote(text)

        translate_url = f"https://translate.google.com/?hl=en&q={encoded_text}&sl={source_lang}&tl={target_lang}&text={encoded_text}&op=translate"

        self.driver.get(translate_url)
        #sleep(3)

        try:
            output_box_xpath = '//span[@class="ryNqvb"]'
            translated_elements = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, output_box_xpath)))

            translated_text = " ".join([elem.text.strip() for elem in translated_elements if elem.text.strip()])
            return translated_text if translated_text else "Translation not found"

        except Exception:
            return "Translation not found"


    def close(self):
        """Properly close the Selenium browser session."""
        if self.driver:
            try:
                self.driver.quit()
                del self.driver
                self.driver = None
            except Exception as e:
                print(f"Warning: Issue while closing the browser: {e}")
