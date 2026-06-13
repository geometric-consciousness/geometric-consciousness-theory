"""Scan content/ for non-ASCII characters outside protected regions (code, math)."""
import re, sys, unicodedata
from pathlib import Path

# Force UTF-8 on Windows so we can print arbitrary Unicode
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).parent.parent
files = list((ROOT / 'content').rglob('*.md'))
print(f'Scanning {len(files)} files...')

def strip_protected(text: str) -> str:
    # Strip fenced code blocks
    text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
    # Strip inline code
    text = re.sub(r'`[^`]+`', '', text)
    # Strip display math $$...$$
    text = re.sub(r'\$\$.*?\$\$', '', text, flags=re.DOTALL)
    # Strip display math \[...\]
    text = re.sub(r'\\\[.*?\\\]', '', text, flags=re.DOTALL)
    # Strip inline math $...$
    text = re.sub(r'\$[^$\n]+\$', '', text)
    return text

char_count = {}
char_files = {}

for f in files:
    try:
        text = f.read_text(encoding='utf-8')
    except Exception as e:
        print(f'Skip {f}: {e}', file=sys.stderr)
        continue
    text = strip_protected(text)
    for ch in text:
        cp = ord(ch)
        if cp < 128:
            continue
        char_count[ch] = char_count.get(ch, 0) + 1
        char_files.setdefault(ch, set()).add(f.relative_to(ROOT).as_posix())

for ch in sorted(char_count.keys(), key=ord):
    cp = ord(ch)
    name = unicodedata.name(ch, '?')
    print(f'U+{cp:04X} {ch!r:6} x{char_count[ch]:5} ({len(char_files[ch])} files) {name}')

print()
print(f'Total distinct non-ASCII codepoints (outside protected regions): {len(char_count)}')
