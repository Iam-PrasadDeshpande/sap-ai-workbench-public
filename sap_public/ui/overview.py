"""Overview-first navigation layer (R8, public edition): the six-stage evaluation lifecycle as a compact two-row,
three-column grid. Same styling and wording as the private engineering workbench (a separate copy: this edition
imports nothing outside its own folder). Every block links to a public page or view only: no private page or runtime endpoint is reachable.
Static, trusted text; nothing here reads content or claims a result.
"""
from __future__ import annotations

import html
from urllib.parse import quote

import streamlit as st

# (number, title, one line, page url_path, optional view)
STAGES = (
    ('01', 'SAP Sources', 'Official developer resources', 'method', 'Evaluation methodology'),
    ('02', 'Discover', 'Inventory and classify', 'capabilities', ''),
    ('03', 'Evaluate', 'Maturity and usefulness', 'method', 'Maturity & usefulness'),
    ('04', 'Hands-on', 'Controlled experiments', 'findings', ''),
    ('05', 'Verify', 'Receipts and evidence', 'method', 'Evidence & limitations'),
    ('06', 'Publish', 'Approved assessments', 'method', 'Architecture & governance'),
)

# Dark, minimal panel in both themes (high contrast on a light page as well). Grid: 3 columns >= 1100 px viewport,
# 2 columns 600-1099 px, 1 column below 600 px. Reading order is the DOM order 01..06 at every width.
CSS = """
<style>
.wb-ov{background:#131518;border:1px solid #2b2f35;border-radius:10px;padding:10px;display:grid;
  grid-template-columns:repeat(3,minmax(0,1fr));gap:6px;font-family:inherit;margin:4px 0 8px 0}
.wb-ov a.wb-st{display:block;padding:12px 14px;border-radius:7px;text-decoration:none;color:#eceff3;
  border:1px solid transparent;min-width:0}
.wb-ov a.wb-st:hover{background:#1c2025;border-color:#343a42}
.wb-ov a.wb-st:focus-visible{outline:2px solid #8ab4ff;outline-offset:1px;background:#1c2025}
.wb-ov .wb-n{display:block;font-size:12px;color:#8b929b;letter-spacing:.06em;line-height:1.2}
.wb-ov .wb-t{display:block;font-size:16px;font-weight:600;color:#f3f5f7;line-height:1.35;margin-top:2px}
.wb-ov .wb-d{display:block;font-size:13px;color:#aab1b9;line-height:1.35;margin-top:2px;overflow-wrap:anywhere}
.wb-ov .wb-go{color:#7f8790;font-weight:400;font-size:13px;margin-left:4px}
.wb-ov-cap{font-size:12px;color:#8b929b;margin:0 0 2px 2px}
@media (max-width:1099px){.wb-ov{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:599px){.wb-ov{grid-template-columns:1fr;padding:6px;gap:2px}
  .wb-ov a.wb-st{padding:8px 10px}.wb-ov .wb-t{font-size:15px}}
</style>
"""


def href(page: str, view: str = '') -> str:
    return page + (f'?view={quote(view)}' if view else '')


def grid_html(stages=STAGES, label: str = 'Evaluation lifecycle') -> str:
    items = []
    for num, title, line, page, view in stages:
        target = html.escape(href(page, view), quote=True)
        aria = html.escape(f'{num} {title}: {line}. Explore details', quote=True)
        items.append(f'<a class="wb-st" href="{target}" target="_self" aria-label="{aria}" data-step="{num}">'
                     f'<span class="wb-n">{num}</span><span class="wb-t">{html.escape(title)}'
                     f'<span class="wb-go" aria-hidden="true">&rarr;</span></span>'
                     f'<span class="wb-d">{html.escape(line)}</span></a>')
    return (CSS + f'<p class="wb-ov-cap">{html.escape(label)} &middot; select a step to explore details</p>'
            f'<nav class="wb-ov" aria-label="{html.escape(label, quote=True)}">' + ''.join(items) + '</nav>')


def render(stages=STAGES, label: str = 'Evaluation lifecycle') -> None:
    st.html(grid_html(stages, label))


# Compact status overview in the same visual language: one row per item, a few short columns, the status always a word
# (colour is only a supplementary marker). Rows stack into labelled lines below 600 px.
TABLE_CSS = """
<style>
.wb-tb{background:#131518;border:1px solid #2b2f35;border-radius:10px;padding:6px 10px;margin:4px 0 10px 0;
  font-family:inherit;color:#e6e9ed}
.wb-tr{display:grid;grid-template-columns:minmax(0,2.2fr) repeat(var(--wb-cols),minmax(0,1.4fr));gap:10px;
  padding:7px 4px;border-top:1px solid #23272c;align-items:baseline}
.wb-tr:first-child{border-top:none}
.wb-th{font-size:12px;color:#8b929b;letter-spacing:.04em;text-transform:uppercase}
.wb-td{font-size:13.5px;line-height:1.35;min-width:0;overflow-wrap:anywhere}
.wb-td.wb-name{font-weight:600;color:#f3f5f7}
.wb-td .wb-l{display:none;color:#8b929b;font-size:12px;margin-right:6px}
.wb-m{display:inline-block;width:7px;height:7px;border-radius:50%;margin-right:6px;vertical-align:middle;background:#6b7179}
.wb-m.green{background:#3fb37f}.wb-m.blue{background:#5b9cf0}.wb-m.orange{background:#e0a03a}.wb-m.red{background:#e5534b}
@media (max-width:599px){.wb-tr{grid-template-columns:1fr;gap:2px}.wb-tr.wb-head{display:none}
  .wb-td .wb-l{display:inline}}
</style>
"""


def table_html(headers, rows, label: str) -> str:
    """headers: [name, col...]; rows: [(name, [(text, colour), ...]), ...]. All text is escaped."""
    cols = len(headers) - 1
    out = [TABLE_CSS, f'<div class="wb-tb" role="table" aria-label="{html.escape(label, quote=True)}" '
                      f'style="--wb-cols:{cols}">',
           '<div class="wb-tr wb-head" role="row">'
           + ''.join(f'<span class="wb-th wb-td" role="columnheader">{html.escape(h)}</span>' for h in headers)
           + '</div>']
    for name, cells in rows:
        tds = ''.join(f'<span class="wb-td" role="cell"><span class="wb-l">{html.escape(h)}</span>'
                      f'<span class="wb-m {html.escape(c or "")}" aria-hidden="true"></span>{html.escape(t)}</span>'
                      for h, (t, c) in zip(headers[1:], cells, strict=True))
        out.append(f'<div class="wb-tr" role="row"><span class="wb-td wb-name" role="cell">{html.escape(name)}</span>'
                   f'{tds}</div>')
    out.append('</div>')
    return ''.join(out)


def table(headers, rows, label: str) -> None:
    st.html(table_html(headers, rows, label))
