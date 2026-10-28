#!/usr/bin/env python3
"""Render reviewed SIGNAL website text into a static HTML page (offline)."""
import html
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
CONFIG = HERE / 'content' / 'site.json'
TEMPLATE = HERE / 'templates' / 'index.template.html'
OUTPUT = HERE / 'index.html'
FIELDS = ('umbrella','umbrella_short','program','director','current_affiliation','headline','subhead','about','copyright_year','meta_description','program_home','director_title','join_contact')


def build():
    data = json.loads(CONFIG.read_text(encoding='utf-8'))
    template = TEMPLATE.read_text(encoding='utf-8')
    for key in FIELDS:
        value = data.get(key)
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f'Missing or invalid website field: {key}')
        template = template.replace('{{'+key+'}}',html.escape(value, quote=True))
    if '{{' in template or '}}' in template:
        raise ValueError('Unreplaced placeholders in website template')
    return template


def render():
    OUTPUT.write_text(build(),encoding='utf-8')
    print(f'Rendered {OUTPUT}')


def check():
    """Exit nonzero if index.html is stale relative to site.json + template (writes nothing)."""
    if OUTPUT.read_text(encoding='utf-8') != build():
        raise SystemExit('FAIL: index.html is out of date; run python3 tools/render_site.py')
    print('PASS: index.html matches content/site.json and the template')


if __name__ == '__main__':
    check() if sys.argv[1:] == ['--check'] else render()
