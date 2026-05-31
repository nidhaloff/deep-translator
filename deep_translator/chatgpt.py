__copyright__ = "Copyright (C) 2020 Nidhal Baccouri"

import os
import re
from typing import List, Optional

from deep_translator.base import BaseTranslator
from deep_translator.constants import (
    OPEN_AI_ENV_VAR,
    OPEN_AI_BASE_URL_ENV_VAR,
    OPEN_AI_MODEL_ENV_VAR,
)
from deep_translator.exceptions import ApiKeyException


# Sentinel that the model is asked to insert between segments. Chosen to be
# extremely unlikely in natural prose while still being plain ASCII.
BATCH_DELIMITER = "<<<~PDFXLATE_SEP~>>>"

# Preambles models like to prepend even when told not to.
_PREAMBLE_RE = re.compile(
    r"^\s*(sure[,!]?|certainly[,!]?|of course[,!]?|here(?:'s| is)"
    r"(?: the)?(?: translation| translated text)?[:\-]?\s*"
    r"|translation[:\-]\s*|translated text[:\-]\s*)",
    re.IGNORECASE,
)

# Pairs of surrounding quote characters to strip if they wrap the whole reply.
_QUOTE_PAIRS = [
    ('"', '"'),
    ("'", "'"),
    ("“", "”"),
    ("‘", "’"),
    ("「", "」"),
    ("『", "』"),
]


def _clean_llm_output(text: str) -> str:
    """Strip common preambles and balanced surrounding quotes/backticks."""
    if not text:
        return text
    out = text.strip()
    # Strip preamble layers (e.g. "Sure! Here is the translation:") until
    # stable, capped to avoid pathological regex loops.
    for _ in range(5):
        new = _PREAMBLE_RE.sub("", out).strip()
        if new == out:
            break
        out = new
    # Strip matched surrounding quotes / triple-backticks.
    if out.startswith("```") and out.endswith("```") and len(out) >= 6:
        out = out[3:-3].strip()
    for left, right in _QUOTE_PAIRS:
        if len(out) >= 2 and out.startswith(left) and out.endswith(right):
            out = out[len(left):-len(right)].strip()
            break
    return out


class ChatGptTranslator(BaseTranslator):
    """
    class that wraps functions, which use the ChatGPT
    under the hood to translate word(s)
    """

    def __init__(
        self,
        source: str = "auto",
        target: str = "english",
        api_key: Optional[str] = os.getenv(OPEN_AI_ENV_VAR, None),
        model: Optional[str] = os.getenv(OPEN_AI_MODEL_ENV_VAR, "gpt-4o-mini"),
        base_url: Optional[str] = os.getenv(OPEN_AI_BASE_URL_ENV_VAR, None),
        **kwargs,
    ):
        if not api_key:
            raise ApiKeyException(env_var=OPEN_AI_ENV_VAR)

        self.api_key = api_key
        self.model = model
        self.base_url = base_url
        self._client = None

        super().__init__(source=source, target=target, **kwargs)

    def _get_client(self):
        if self._client is None:
            import openai

            self._client = openai.OpenAI(
                api_key=self.api_key,
                base_url=self.base_url if self.base_url else None,
            )
        return self._client

    def _chat(self, prompt: str) -> str:
        client = self._get_client()
        response = client.chat.completions.create(
            model=self.model if self.model else "default_model",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a professional translator. Output only the "
                        "translation with no explanations, no quotes, and no "
                        "additional commentary. Preserve any delimiter tokens "
                        "exactly as they appear."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
        )
        return response.choices[0].message.content

    def translate(self, text: str, **kwargs) -> str:
        prompt = (
            f"Translate the following text into {self.target}. "
            f"Return only the translation.\n\n{text}"
        )
        return _clean_llm_output(self._chat(prompt))

    def translate_file(self, path: str, **kwargs) -> str:
        return self._translate_file(path, **kwargs)

    def translate_batch(self, batch: List[str], **kwargs) -> List[str]:
        """
        Translate a list of texts in a single API call using a delimiter.
        Falls back to per-item translation when the delimiter count mismatches.
        """
        if not batch:
            return []
        if len(batch) == 1:
            return [self.translate(batch[0], **kwargs)]

        joined = f"\n{BATCH_DELIMITER}\n".join(batch)
        prompt = (
            f"Translate each of the following {len(batch)} segments into "
            f"{self.target}. The segments are separated by the exact token "
            f"{BATCH_DELIMITER}. Keep that token between segments in your "
            f"output. Return exactly {len(batch)} segments in the same order. "
            f"Output only the translations.\n\n{joined}"
        )
        result = self._chat(prompt)
        parts = [p.strip() for p in re.split(re.escape(BATCH_DELIMITER), result)]

        if len(parts) != len(batch):
            # delimiter was lost or duplicated; fall back to per-item
            return [self.translate(t, **kwargs) for t in batch]
        return [_clean_llm_output(p) for p in parts]
