"""Shared PDF rewriting primitives used by both the Streamlit app and CLI."""

from .core import (
    COLOR_MAP,
    color_to_rgb,
    color_css,
    get_blocks,
    write_translated_block,
    write_translated_page,
)

__all__ = [
    "COLOR_MAP",
    "color_to_rgb",
    "color_css",
    "get_blocks",
    "write_translated_block",
    "write_translated_page",
]
