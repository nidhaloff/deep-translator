import os
import json
import hashlib
from pathlib import Path
import streamlit as st
import pymupdf
from deep_translator import (
    GoogleTranslator,
)
from deep_translator.openai_compatible import (
    OpenAICompatibleTranslator,
    TranslationFailed,
)
import logging
import argparse
import translation_cache
from pdf_translator import COLOR_MAP, get_blocks, write_translated_page

# Constants
DEFAULT_PAGES_PER_LOAD = 2
DEFAULT_MODEL = "default_model"
DEFAULT_API_BASE = "http://localhost:8080/v1"

# Supported translators
TRANSLATORS = {
    'OpenAI Compatible': OpenAICompatibleTranslator,
    'OpenAI': OpenAICompatibleTranslator,
    'Google': GoogleTranslator,
}

# Target language options for ChatGPT
LANGUAGE_OPTIONS = {
    "简体中文": "zh-CN",
    "繁體中文": "zh-TW",
    "English": "en",
    "日本語": "ja",
    "한국어": "ko",
    "Español": "es",
    "Français": "fr",
    "Deutsch": "de",
}

# Add source language options
SOURCE_LANGUAGE_OPTIONS = {
    "English": "en",
    "简体中文": "zh-CN",
    "繁體中文": "zh-TW",
    "日本語": "ja",
    "한국어": "ko",
    "Español": "es",
    "Français": "fr",
    "Deutsch": "de",
    "Auto": "auto",
}

# Global translation configuration
TRANSLATOR_CONFIG = {
    "type": "Google",  # Options: "Google" or "OpenAI"
    # OpenAI settings (used only if type is "OpenAI")
    "openai": {
        "default_api_base": DEFAULT_API_BASE,
        "default_model": DEFAULT_MODEL, # "gpt-4o-mini",
        "default_api_key": "sk-xxx"
    },
    # Google settings (used only if type is "Google")
    "google": {
        "default_api_base": "https://translate.googleapis.com"
    }
}

# Add argument parser
def parse_args():
    parser = argparse.ArgumentParser(description='PDF Translator Application')
    parser.add_argument(
        '--translator', 
        type=str, 
        choices=['google', 'openai'], 
        default='google',
        help='Specify translator type: google or openai'
    )
    parser.add_argument(
        '--api-base',
        type=str,
        help='API base URL for the translator'
    )
    parser.add_argument(
        '--api-key',
        type=str,
        help='API key for OpenAI compatible translator'
    )
    parser.add_argument(
        '--model',
        type=str,
        help='Model name for OpenAI compatible translator'
    )
    return parser.parse_args()

# Update TRANSLATOR_CONFIG based on command line arguments
def update_translator_config(args):
    global TRANSLATOR_CONFIG
    
    TRANSLATOR_CONFIG["type"] = "Google" if args.translator.lower() == "google" else "OpenAI"
    
    if args.translator.lower() == "google":
        if args.api_base:
            TRANSLATOR_CONFIG["google"]["default_api_base"] = args.api_base
    else:  # OpenAI
        if args.api_base:
            TRANSLATOR_CONFIG["openai"]["default_api_base"] = args.api_base
        if args.api_key:
            TRANSLATOR_CONFIG["openai"]["default_api_key"] = args.api_key
        if args.model:
            TRANSLATOR_CONFIG["openai"]["default_model"] = args.model

def get_cache_dir():
    """Get or create cache directory"""
    cache_dir = Path('.cached')
    cache_dir.mkdir(exist_ok=True)
    return cache_dir

def get_cache_key(doc_info: dict, page_num: int, translator_name: str, target_lang: str, text_content: str):
    """Generate cache key for a specific page translation.

    Uses SHA-256 over the full (doc_meta, page, translator, target, content)
    tuple so collisions across large books are not possible in practice.
    """
    payload = "\x1f".join([
        str(doc_info.get('title', '')),
        str(doc_info.get('author', '')),
        str(doc_info.get('pagecount', '')),
        str(page_num),
        translator_name,
        target_lang,
        text_content,
    ])
    digest = hashlib.sha256(payload.encode('utf-8')).hexdigest()
    return f"{digest}.pdf"

def get_cached_translation(cache_key: str) -> pymupdf.Document:
    """Get cached translation if exists"""
    cache_path = get_cache_dir() / cache_key
    if cache_path.exists():
        try:
            return pymupdf.open(str(cache_path))
        except Exception as e:
            logging.error(f"Error loading cache: {str(e)}")
            return None
    return None

def save_translation_cache(doc: pymupdf.Document, cache_key: str):
    """Save translation to cache"""
    cache_path = get_cache_dir() / cache_key
    doc.save(str(cache_path))  # 确保提供文件路径字符串

def _translator_model_id(translator, translator_name: str) -> str:
    """Stable identifier used as part of the block-cache key."""
    model = getattr(translator, "model", "") or ""
    return f"{translator_name}:{model}"


def translate_blocks(texts, translator, translator_name: str, target_lang: str):
    """Translate a list of block texts using the block-level cache and a
    single batched LLM/Google call for the misses. Returns
    (translated_texts, failed_count). Failed blocks keep their original text.
    """
    model_id = _translator_model_id(translator, translator_name)
    source = getattr(translator, "_source", "auto")
    target = target_lang

    results = [None] * len(texts)
    misses_idx = []
    misses_text = []

    for i, text in enumerate(texts):
        if not text or not text.strip():
            results[i] = text
            continue
        cached = translation_cache.get(
            translator_name, source, target, model_id, text
        )
        if cached is not None:
            results[i] = cached
        else:
            misses_idx.append(i)
            misses_text.append(text)

    failed = 0
    if misses_text:
        try:
            if hasattr(translator, "translate_batch"):
                translated = translator.translate_batch(misses_text)
            else:
                translated = [translator.translate(t) for t in misses_text]
            for idx, text, out in zip(misses_idx, misses_text, translated):
                out = str(out) if out is not None else text
                results[idx] = out
                translation_cache.put(
                    translator_name, source, target, model_id, text, out
                )
        except TranslationFailed as exc:
            logging.error("Batch translation failed: %s", exc)
            # fall back per-block so partial success is still possible
            for idx, text in zip(misses_idx, misses_text):
                try:
                    out = str(translator.translate(text))
                    results[idx] = out
                    translation_cache.put(
                        translator_name, source, target, model_id, text, out
                    )
                except Exception as inner:
                    logging.error("Per-block fallback failed: %s", inner)
                    results[idx] = text
                    failed += 1
        except Exception as exc:  # noqa: BLE001
            logging.error("Unexpected translation error: %s", exc)
            for idx, text in zip(misses_idx, misses_text):
                results[idx] = text
            failed = len(misses_idx)

    return results, failed


def translate_pdf_pages(doc, doc_bytes, start_page, num_pages, translator, text_color, translator_name, target_lang):
    """Translate specific pages of a PDF document with progress and caching"""
    # Log translator information
    logging.info(f"Using translator: {translator_name}, source: {translator._source}, target: {translator._target}")
    logging.info(f"Selected translator: {translator_name}, Class: {translator.__class__.__name__}")
    
    translated_pages = []
    total_pages = min(start_page + num_pages, doc.page_count) - start_page
    cache_hits = 0
    
    # Create a progress bar
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for i, page_num in enumerate(range(start_page, min(start_page + num_pages, doc.page_count))):
        status_text.text(f"Translating page {page_num + 1}...")
        
        # Extract text content for cache key
        page = doc[page_num]
        text_content = page.get_text("text")
        
        # Check cache first using text content
        cache_key = get_cache_key(
            doc.metadata,
            page_num,
            translator_name,
            target_lang,
            text_content
        )
        
        cached_doc = get_cached_translation(cache_key)
        
        if cached_doc is not None:
            translated_pages.append(cached_doc)
            cache_hits += 1
            logging.info(f"Cache hit: Using cached translation for page {page_num + 1}")
            status_text.text(f"Using cached translation for page {page_num + 1}")
        else:
            logging.info(f"Cache miss: Translating page {page_num + 1}")
            status_text.text(f"Translating page {page_num + 1} (not in cache)")
            
            # Create a new PDF document for this page
            new_doc = pymupdf.open()
            new_doc.insert_pdf(doc, from_page=page_num, to_page=page_num)
            page = new_doc[0]

            # Extract text blocks and translate via batch + block-level cache
            blocks = get_blocks(page)
            translated_texts, failed = translate_blocks(
                [b[4] for b in blocks],
                translator,
                translator_name,
                target_lang,
            )
            if failed:
                st.warning(
                    f"Page {page_num + 1}: {failed} block(s) failed to "
                    "translate; original text kept."
                )

            write_translated_page(
                page, blocks, translated_texts, text_color=text_color
            )

            # Save page-level PDF cache as a secondary cache layer
            save_translation_cache(new_doc, cache_key)
            translated_pages.append(new_doc)
            logging.info(f"Cached new translation for page {page_num + 1}")
        
        # Update progress
        progress = (i + 1) / total_pages
        progress_bar.progress(progress)
    
    # Clear progress indicators and show summary
    progress_bar.empty()
    if cache_hits > 0:
        st.info(f"Used cache for {cache_hits} out of {total_pages} pages")
    
    return translated_pages

def get_page_image(page, scale=2):
    """Get high quality image from PDF page"""
    # 计算缩放后的尺寸
    zoom = scale
    mat = pymupdf.Matrix(zoom, zoom)
    
    # 使用较低分辨率渲染页面，但保持清晰度
    pix = page.get_pixmap(
        matrix=mat,
        alpha=False,
        colorspace="rgb",  # Use RGB instead of RGBA
    )
    
    return pix

def translate_all_pages(
    input_doc,
    output_doc,
    translator,
    progress_bar,
    batch_size=1,
    **kwargs
):
    """Translate all pages of the PDF document"""
    # Log translator information for full document translation
    logging.info(f"Starting full document translation with: {kwargs.get('translator_name', 'unknown')}")
    logging.info(f"Translator settings - source: {translator._source}, target: {translator._target}")

    total_pages = input_doc.page_count
    
    # Create a progress bar for overall progress
    status_text = st.empty()
    
    # Translate all pages using translate_pdf_pages
    translated_pages = translate_pdf_pages(
        input_doc,
        None,  # doc_bytes not needed as we're using text content for cache
        0,  # start from first page
        total_pages,  # translate all pages
        translator,
        kwargs.get('text_color', 'darkred'),
        kwargs.get('translator_name', 'google'),
        kwargs.get('target_lang', 'zh-CN')
    )
    
    # Combine all pages into one PDF with compression
    output_path = kwargs.get('output_path', 'output.pdf')
    for trans_doc in translated_pages:
        output_doc.insert_pdf(trans_doc)
    
    # Save with compression options
    output_doc.save(
        output_path,
        garbage=4,
        deflate=True,
        clean=True,
        linear=True
    )
    
    return output_doc

def init_session_state():
    """Initialize session state variables"""
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 0
    if 'translation_started' not in st.session_state:
        st.session_state.translation_started = True
    if 'all_translated' not in st.session_state:
        st.session_state.all_translated = False
    if 'translated_doc' not in st.session_state:
        st.session_state.translated_doc = None
    if 'previous_file' not in st.session_state:
        st.session_state.previous_file = None
    if 'api_settings' not in st.session_state:
        st.session_state.api_settings = {}

def main():
    st.set_page_config(layout="wide", page_title="PDF Translator for Human")
    st.title("PDF Translator for Human")

    # Initialize session state
    init_session_state()

    # Sidebar configuration
    with st.sidebar:
        st.header("Settings")
        
        uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
        
        # Reset session state when a new file is uploaded
        if uploaded_file is not None and (st.session_state.previous_file is None or 
                                        uploaded_file.name != st.session_state.previous_file):
            st.session_state.current_page = 0
            st.session_state.translation_started = True
            st.session_state.all_translated = False
            st.session_state.translated_doc = None
            st.session_state.previous_file = uploaded_file.name
            st.rerun()
            
        # Add source language selection
        source_lang_name = st.selectbox(
            "Source Language",
            options=list(SOURCE_LANGUAGE_OPTIONS.keys()),
            index=0  # Default to English
        )
        source_lang = SOURCE_LANGUAGE_OPTIONS[source_lang_name]
        
        pages_per_load = st.number_input(
            "Pages per load",
            min_value=1,
            max_value=5,
            value=DEFAULT_PAGES_PER_LOAD
        )
        
        text_color = st.selectbox(
            "Translation Color",
            options=list(COLOR_MAP.keys()),
            index=0
        )
        
        target_lang = st.selectbox(
            "Target Language",
            options=list(LANGUAGE_OPTIONS.keys()),
            index=0
        )
        target_lang_code = LANGUAGE_OPTIONS[target_lang]
        
        # Add translator selection
        st.subheader("Translator Settings")
        translator_type = st.radio(
            "Translator",
            options=["Google", "OpenAI Compatible"],
            index=0 if TRANSLATOR_CONFIG["type"] == "Google" else 1
        )
        
        # API Configuration based on translator selection
        if translator_type == "OpenAI Compatible":
            api_key = st.text_input(
                "API Key",
                value=TRANSLATOR_CONFIG["openai"]["default_api_key"],
                type="password"
            )
            api_base = st.text_input(
                "API Base URL",
                value=TRANSLATOR_CONFIG["openai"]["default_api_base"]
            )
            model = st.text_input(
                "Model Name",
                value=TRANSLATOR_CONFIG["openai"]["default_model"]
            )
            
            # Store API settings
            st.session_state.api_settings.update({
                'api_key': api_key,
                'api_base': api_base,
                'model': model
            })
        else:  # Google Translator
            # No configuration needed for Google Translator
            st.session_state.api_settings.update({
                'api_base': TRANSLATOR_CONFIG["google"]["default_api_base"]
            })

    # Main content area
    if uploaded_file is not None:
        doc_bytes = uploaded_file.read()
        doc = pymupdf.open(stream=doc_bytes)
        
        # Create two columns for side-by-side display
        col1, col2 = st.columns(2)
        
        # Display original pages
        with col1:
            st.header("Original")
            for page_num in range(st.session_state.current_page,
                                min(st.session_state.current_page + pages_per_load, doc.page_count)):
                page = doc[page_num]
                pix = get_page_image(page)
                st.image(pix.tobytes(), caption=f"Page {page_num + 1}", use_container_width=True)
        
        # Translation column
        with col2:
            st.header("Translated")
            
            try:
                # Initialize translator based on user selection
                if translator_type == "Google":
                    translator = GoogleTranslator(
                        source=source_lang,
                        target=target_lang_code
                    )
                else:
                    translator = OpenAICompatibleTranslator(
                        source=source_lang,
                        target=target_lang_code,
                        api_key=st.session_state.api_settings.get('api_key'),
                        base_url=st.session_state.api_settings.get('api_base'),
                        model=st.session_state.api_settings.get('model')
                    )

                # Translate current batch of pages
                translated_pages = translate_pdf_pages(
                    doc,
                    doc_bytes,
                    st.session_state.current_page,
                    pages_per_load,
                    translator,
                    text_color,
                    translator_type,
                    target_lang_code
                )
                
                # Display translated pages
                for i, trans_doc in enumerate(translated_pages):
                    page = trans_doc[0]
                    pix = get_page_image(page)
                    st.image(pix.tobytes(), caption=f"Page {st.session_state.current_page + i + 1}", use_container_width=True)
            
            except Exception as e:
                st.error(f"Translation error: {str(e)}")
                logging.error(f"Translation error: {str(e)}")
                return

        # Navigation and action buttons
        st.markdown("---")  # Add a separator
        button_col1, button_col2, button_col3, button_col4 = st.columns(4)
        
        # Previous Pages button
        with button_col1:
            if st.session_state.current_page > 0:
                if st.button("Previous Pages", use_container_width=True):
                    st.session_state.current_page = max(0, st.session_state.current_page - pages_per_load)
                    st.rerun()
            else:
                st.button("Previous Pages", disabled=True, use_container_width=True)
        
        # Next Pages button
        with button_col2:
            if st.session_state.current_page + pages_per_load < doc.page_count:
                if st.button("Next Pages", use_container_width=True):
                    st.session_state.current_page = min(
                        doc.page_count - 1,
                        st.session_state.current_page + pages_per_load
                    )
                    st.rerun()
            else:
                st.button("Next Pages", disabled=True, use_container_width=True)
        
        # Translate All button
        with button_col3:
            if st.button("Translate All", 
                        disabled=st.session_state.all_translated,
                        use_container_width=True):
                try:
                    # Initialize translator based on user selection
                    if translator_type == "Google":
                        translator = GoogleTranslator(
                            source=source_lang,
                            target=target_lang_code
                        )
                    else:
                        translator = OpenAICompatibleTranslator(
                            source=source_lang,
                            target=target_lang_code,
                            api_key=st.session_state.api_settings.get('api_key'),
                            base_url=st.session_state.api_settings.get('api_base'),
                            model=st.session_state.api_settings.get('model')
                        )

                    # Translate all pages
                    output_doc = pymupdf.open()
                    output_path = f"translated_{uploaded_file.name}"
                    output_doc = translate_all_pages(
                        doc,
                        output_doc,
                        translator,
                        st.empty(),
                        pages_per_load,
                        text_color=text_color,
                        translator_name=translator_type,
                        target_lang=target_lang_code,
                        output_path=output_path
                    )
                    
                    st.session_state.all_translated = True
                    st.session_state.translated_doc = output_path
                    st.rerun()
                except Exception as e:
                    st.error(f"Translation error: {str(e)}")
                    logging.error(f"Translation error: {str(e)}")
                    return
        
        # Download button
        with button_col4:
            if not st.session_state.all_translated:
                st.markdown(
                    """
                    <div title="You can download the translated file after all content has been translated">
                        <button style="width: 100%" disabled>Download</button>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            else:
                with open(st.session_state.translated_doc, "rb") as file:
                    st.download_button(
                        "Download",
                        file,
                        file_name=f"translated_{uploaded_file.name}",
                        mime="application/pdf",
                        use_container_width=True
                    )
    else:
        st.info("Please upload a PDF file to begin translation")


    # 使用Google翻译（默认）：
    # streamlit run app.py

    # 使用Google翻译并指定API base：
    # streamlit run app.py --translator google --api-base https://translate.googleapis.com

    # 使用OpenAI兼容模型：
    # python app.py --translator openai --model default_model --api-key sk-xxx --api-base http://localhost:8080/v1

    # 使用OpenAI翻译并指定API base：
    # python app.py --translator openai --api-base https://api.openai.com/v1 --model gpt-4o-mini --api-key sk-xxx


if __name__ == "__main__":
    args = parse_args()
    update_translator_config(args)
    main() 