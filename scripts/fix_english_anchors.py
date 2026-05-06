#!/usr/bin/env python3
"""Replace Portuguese anchor in English files to English anchor."""
from pathlib import Path
root = Path(__file__).resolve().parents[1]
docs = root / 'docs' / 'en'
old = '#41-configurando-a-rede-docker'
new = '#41-configuring-the-docker-network'
count = 0
for md in docs.rglob('*.md'):
    text = md.read_text(encoding='utf-8')
    if old in text:
        bak = md.with_suffix(md.suffix + '.bak4')
        bak.write_text(text, encoding='utf-8')
        md.write_text(text.replace(old, new), encoding='utf-8')
        count += 1
print(f'Modified {count} files')

