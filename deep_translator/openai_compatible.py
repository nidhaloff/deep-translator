import json
import logging
import time
from typing import List

from .chatgpt import ChatGptTranslator

logger = logging.getLogger(__name__)


class TranslationFailed(Exception):
    """Raised when a translation attempt could not be completed."""

    def __init__(self, original_text: str, reason: str):
        super().__init__(reason)
        self.original_text = original_text
        self.reason = reason


def _is_retriable(exc: BaseException) -> bool:
    """Return True for transient errors that are worth retrying."""
    # JSON parsing errors are typically partial/empty responses → retry.
    if isinstance(exc, json.JSONDecodeError):
        return True

    name = type(exc).__name__
    # openai SDK exception classes (avoid hard import so the optional
    # dependency isn't forced at import time).
    transient = {
        "RateLimitError",
        "APIConnectionError",
        "APITimeoutError",
        "InternalServerError",
        "APIError",  # base class; covers most transport-level failures
    }
    if name in transient:
        return True

    # HTTP 5xx exposed via status_code attribute on some SDKs.
    status = getattr(exc, "status_code", None)
    if isinstance(status, int) and 500 <= status < 600:
        return True

    return False


class OpenAICompatibleTranslator(ChatGptTranslator):
    """Translator that handles OpenAI compatible APIs with retry + error
    classification. Only transient errors are retried; everything else
    raises TranslationFailed so the UI layer can surface the failure."""

    def __init__(self, source="en", target="zh-CN", **kwargs):
        super().__init__(source=source, target=target, **kwargs)
        self.retry_count = 3
        self.retry_delay = 1  # seconds (exponential backoff base)

    def _call_with_retry(self, fn, original_text: str):
        last_exc = None
        for attempt in range(self.retry_count):
            try:
                logger.debug(
                    "OpenAI-compatible request, base_url=%s attempt=%d",
                    self.base_url,
                    attempt + 1,
                )
                return fn()
            except Exception as exc:  # noqa: BLE001
                last_exc = exc
                if not _is_retriable(exc):
                    logger.error(
                        "Non-retriable translation error: %s", exc
                    )
                    raise TranslationFailed(original_text, str(exc)) from exc
                logger.warning(
                    "Retriable error on attempt %d/%d: %s",
                    attempt + 1,
                    self.retry_count,
                    exc,
                )
                if attempt < self.retry_count - 1:
                    time.sleep(self.retry_delay * (2 ** attempt))
        raise TranslationFailed(
            original_text,
            f"Exhausted {self.retry_count} retries: {last_exc}",
        )

    def translate(self, text: str, **kwargs) -> str:
        if not text or not text.strip():
            return text
        return self._call_with_retry(
            lambda: super(OpenAICompatibleTranslator, self).translate(
                text, **kwargs
            ),
            original_text=text,
        )

    def translate_batch(self, batch: List[str], **kwargs) -> List[str]:
        if not batch:
            return []
        # Empty/whitespace items should pass through without an API call.
        non_empty_idx = [i for i, t in enumerate(batch) if t and t.strip()]
        if not non_empty_idx:
            return list(batch)

        subset = [batch[i] for i in non_empty_idx]
        try:
            translated = self._call_with_retry(
                lambda: super(OpenAICompatibleTranslator, self).translate_batch(
                    subset, **kwargs
                ),
                original_text="\n".join(subset)[:200],
            )
        except TranslationFailed:
            # Bubble up — caller decides how to report partial failures.
            raise

        result = list(batch)
        for i, t in zip(non_empty_idx, translated):
            result[i] = t
        return result
