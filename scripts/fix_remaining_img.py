#!/usr/bin/env python3
"""Final pass: fix remaining absolute /img/ links to relative paths."""
import re
from pathlib import Path

root = Path(__file__).resolve().parents[1]
docs = root / 'docs'

for md in sorted(docs.rglob('*.md')):
    if '.bak' in md.name:
        continue

    text = md.read_text(encoding='utf-8')
    original_text = text

    # Calculate depth: count how many folders from docs/
    relative_path = md.relative_to(docs)
    depth = len(relative_path.parts) - 1
    back_path = '../' * depth + 'img/'

    # Replace remaining /img/ with correct relative path
    text = re.sub(r'\]\(/img/', f']({back_path}', text)

    if text != original_text:
        bak = md.with_suffix(md.suffix + '.bak-final')
        bak.write_text(original_text, encoding='utf-8')
        md.write_text(text, encoding='utf-8')
        print(f"Fixed remaining /img/ in {md.name}")

print("Done!")

