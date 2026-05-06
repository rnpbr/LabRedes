#!/usr/bin/env python3
"""Replace incorrect anchor '#31-configurando-a-rede-docker' with '#41-configurando-a-rede-docker' across docs."""
from pathlib import Path
root = Path(__file__).resolve().parents[1]
docs = root / 'docs'
old = '#31-configurando-a-rede-docker'
new = '#41-configurando-a-rede-docker'
count = 0
for md in docs.rglob('*.md'):
    text = md.read_text(encoding='utf-8')
    if old in text:
        bak = md.with_suffix(md.suffix + '.bak3')
        bak.write_text(text, encoding='utf-8')
        md.write_text(text.replace(old, new), encoding='utf-8')
        count += 1
print(f'Modified {count} files')

