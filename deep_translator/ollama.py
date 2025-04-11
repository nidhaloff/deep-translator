__copyright__ = "Copyright (C) 2025 Brivaldo Junior"

from typing import List, Optional
from deep_translator.base import BaseTranslator


class OllamaTranslator(BaseTranslator):
    """
    class that wraps functions, which use the Ollama
    under the hood to translate word(s)
    """

    def __init__(
        self,
        source: str = "auto",
        target: str = "english",
        model: Optional[str] = "llama3.2:latest",
        **kwargs,
    ):
        """
        @param source: source language
        @param target: target language
        """
        self.model = model

        super().__init__(source=source, target=target, **kwargs)

    def translate(self, text: str, **kwargs) -> str:
        """
        @param text: text to translate
        @return: translated text
        """
        import ollama


        prompt = f"Translate the text below into {self.target}.\n"
        prompt += f'Text: "{text}"'

        response = ollama.chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        return response.message.content

    def translate_file(self, path: str, **kwargs) -> str:
        return self._translate_file(path, **kwargs)

    def translate_batch(self, batch: List[str], **kwargs) -> List[str]:
        """
        @param batch: list of texts to translate
        @return: list of translations
        """
        return self._translate_batch(batch, **kwargs)
