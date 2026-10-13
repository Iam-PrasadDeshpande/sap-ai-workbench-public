"""Text hygiene for anything shown, stored in session state or exported. Retrieved and typed text is untrusted data."""
from __future__ import annotations

import html
import re
import unicodedata

REPLACEMENT = '�'
MARKER = '[unreadable]'
_MD_SPECIAL = re.compile(r'([\\`*_{}\[\]()#+\-.!|<>~$])')
_BAD_SCHEME = re.compile(r'(?i)\b(javascript|data|vbscript)\s*:')


def clean_text(value, max_len: int = 300, multiline: bool = False) -> str:
    """Normalize, strip control characters, mark unreadable runs, bound the length. Never raises on odd input."""
    text = '' if value is None else str(value)
    text = re.sub(f'{REPLACEMENT}+', MARKER, text)
    text = unicodedata.normalize('NFC', text)
    keep = '\n\t' if multiline else ''
    text = ''.join(ch if (ch.isprintable() or ch in keep) else ' ' for ch in text)
    text = re.sub(r'[ \t]+', ' ', text)
    if not multiline:
        text = text.replace('\n', ' ').replace('\r', ' ')
    text = text.strip()
    if len(text) > max_len:
        text = text[: max_len - 1].rstrip() + '…'
    return text


def md_escape(value, max_len: int = 600) -> str:
    """Render stored/remote text literally on screen: no links, images, headings, HTML or inline code."""
    text = clean_text(value, max_len)
    text = _BAD_SCHEME.sub(lambda m: m.group(1) + '\\:', text)
    return _MD_SPECIAL.sub(r'\\\1', text)


def report_text(value, max_len: int = 600) -> str:
    """Neutralizer for exported Markdown: readable plain text that cannot form a link, image, tag or heading."""
    text = clean_text(value, max_len)
    for old, new in (('\\', '\\\\'), ('[', '\\['), (']', '\\]'), ('<', '&lt;'), ('>', '&gt;'), ('`', "'")):
        text = text.replace(old, new)
    return _BAD_SCHEME.sub(lambda m: m.group(1) + '\\:', text.lstrip('#>-*+ '))


def csv_cell(value) -> str:
    """Spreadsheet formula-injection defence: a cell may never start with a formula or control character."""
    text = clean_text(value, 500)
    if text[:1] in ('=', '+', '-', '@', '\t', '\r'):
        text = "'" + text
    return text


def html_text(value, max_len: int = 600) -> str:
    return html.escape(clean_text(value, max_len), quote=True)


def safe_filename(stem: str, suffix: str) -> str:
    stem = re.sub(r'[^A-Za-z0-9_.-]+', '-', clean_text(stem, 60)).strip('-.') or 'report'
    return f'{stem}{suffix}'


def https_url_on(host: str, url) -> str:
    """Return the URL only if it is https on exactly this host; otherwise ''. Used before showing any link."""
    text = clean_text(url, 400)
    m = re.match(r'^https://([A-Za-z0-9.-]+)(/[^\s]*)?$', text)
    return text if m and m.group(1).lower() == host else ''
