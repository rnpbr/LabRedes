#!/usr/bin/env python3
"""Fix image links to use correct relative paths based on file depth, and convert external links to HTML."""
import re
from pathlib import Path

root = Path(__file__).resolve().parents[1]
docs = root / 'docs'

# Mapping of relative depths and their corrected paths
# Based on MkDocs suggestions during build
replacements = {
    # pt/index.md (depth 1) -> ../img/
    "('pt/index.md': '../img/',": None,  # placeholder

    # pt/Ferramentas files (depth 2 or 3)
    # For depth 2 use ../../img/
    # For depth 3 use ../../../img/
}

for md in sorted(docs.rglob('*.md')):
    if '.bak' in md.name:
        continue

    text = md.read_text(encoding='utf-8')
    original_text = text

    # Calculate depth: count how many folders from docs/
    relative_path = md.relative_to(docs)
    depth = len(relative_path.parts) - 1  # -1 because last part is filename

    # Build correct relative path to img folder
    back_path = '../' * depth + 'img/'

    # Fix image links: replace /img/ with correct relative path
    # Pattern: ![...](/img/...)
    text = re.sub(r'!\[(.*?)\]\(/img/', f'![\\1]({back_path}', text)

    # Fix external links to use HTML with target="_blank"
    # Pattern: [text](http://...) or [text](https://...)
    # But avoid double-converting already HTML links
    def replace_external_link(match):
        link_text = match.group(1)
        url = match.group(2)
        # Don't convert if already HTML or has target attribute
        if url.startswith('http://') or url.startswith('https://'):
            return f'<a target="_blank" href="{url}">{link_text}</a>'
        return match.group(0)  # Return unchanged if not external

    text = re.sub(r'\[(.*?)\]\((https?://.*?)\)', replace_external_link, text)

    if text != original_text:
        # Create backup
        bak = md.with_suffix(md.suffix + '.bak-fixed')
        bak.write_text(original_text, encoding='utf-8')
        md.write_text(text, encoding='utf-8')
        print(f"Fixed {md}")

print("Done!")

