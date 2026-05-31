"""Core PDF block rewriting primitives.

Both `app.py` (Streamlit UI) and `translator_cli.py` (CLI with OCG layers)
delegate the per-block rewrite to this module so the rendering details stay
in one place.
"""

from typing import List, Optional, Sequence, Tuple

import pymupdf


COLOR_MAP = {
    "darkred": (0.8, 0, 0),
    "black": (0, 0, 0),
    "blue": (0, 0, 0.8),
    "darkgreen": (0, 0.5, 0),
    "purple": (0.5, 0, 0.5),
}

_WHITE = pymupdf.pdfcolor["white"]


def color_to_rgb(name: str) -> Tuple[float, float, float]:
    """Resolve a color name to an (R, G, B) tuple, defaulting to darkred."""
    return COLOR_MAP.get((name or "").lower(), COLOR_MAP["darkred"])


def color_css(name: str) -> str:
    """Return the CSS used for translated HTML boxes."""
    r, g, b = color_to_rgb(name)
    return (
        f"* {{font-family: sans-serif; "
        f"color: rgb({int(r * 255)}, {int(g * 255)}, {int(b * 255)});}}"
    )


def get_blocks(page) -> List[tuple]:
    """Return text blocks for a page with dehyphenation enabled."""
    return page.get_text("blocks", flags=pymupdf.TEXT_DEHYPHENATE)


def write_translated_block(
    page,
    bbox,
    original_text: str,
    translated_text: str,
    text_color: str = "darkred",
    oc_trans: Optional[int] = None,
    oc_orig: Optional[int] = None,
) -> None:
    """Cover the original block and write the translation.

    - If `oc_orig` is given, the original text is re-inserted on that OCG
      layer (so it can still be toggled on in a PDF reader); the base layer
      is cleared with white.
    - If only `oc_trans` is given, the white-out and translation are drawn
      on that OCG layer (translation as an optional overlay over the
      original). This matches the CLI's "keep_original" mode.
    - If both are None, the original is covered with white on the base
      layer and the translation is drawn on the base layer (the Streamlit
      app's behavior).
    """
    css = color_css(text_color)

    if oc_orig is not None:
        # Move original text to its hidden layer, clear base layer
        page.insert_htmlbox(
            bbox,
            original_text,
            css="* {font-family: sans-serif;}",
            oc=oc_orig,
        )
        page.draw_rect(bbox, color=None, fill=_WHITE)
    elif oc_trans is not None:
        # White-out only in the translation layer (original kept on base)
        page.draw_rect(bbox, color=None, fill=_WHITE, oc=oc_trans)
    else:
        page.draw_rect(bbox, color=None, fill=_WHITE)

    if oc_trans is not None:
        page.insert_htmlbox(bbox, str(translated_text), css=css, oc=oc_trans)
    else:
        page.insert_htmlbox(bbox, str(translated_text), css=css)


def write_translated_page(
    page,
    blocks: Sequence[tuple],
    translated_texts: Sequence[str],
    text_color: str = "darkred",
    oc_trans: Optional[int] = None,
    oc_orig: Optional[int] = None,
) -> None:
    """Apply translations to every block on a page."""
    for block, translated in zip(blocks, translated_texts):
        write_translated_block(
            page,
            block[:4],
            block[4],
            translated,
            text_color=text_color,
            oc_trans=oc_trans,
            oc_orig=oc_orig,
        )
