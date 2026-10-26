"""Compare publication tier labels with a Git baseline and scan added Law 8 text."""
import argparse
from collections import Counter
import csv
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--baseline', default='b3acea3855392b9ac9f01219d63bd89c8d3332d5')
args = parser.parse_args()

def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT).decode('utf-8')

paths = git('ls-files', 'content/').splitlines()
tiers = ['0', '1', '1/2', '2', '3', '4']
pattern = re.compile(r'\[Tier\s+(0|1/2|[1-4])(?=[^\d/]|$)')
labels = re.compile(r'\[Tier\b[^\]\n]*\]')
rows = []
changes = []
removed_all = Counter()
total_before, total_after = Counter(), Counter()
# Read the baseline in one Git process, preserving arbitrary blob lengths.
batch = subprocess.run(['git', 'cat-file', '--batch'], cwd=ROOT,
    input=''.join(f'{args.baseline}:{p}\n' for p in paths).encode(),
    stdout=subprocess.PIPE, check=True).stdout
offset = 0
for path in paths:
    header_end = batch.index(b'\n', offset)
    size = int(batch[offset:header_end].split()[-1])
    start = header_end + 1
    old = batch[start:start+size].decode('utf-8', errors='replace')
    offset = start + size + 1
    new = (ROOT/path).read_text(encoding='utf-8', errors='replace')
    before, after = Counter(pattern.findall(old)), Counter(pattern.findall(new))
    total_before.update(before)
    total_after.update(after)
    for tier in tiers:
        rows.append([path, tier, before[tier], after[tier], after[tier]-before[tier]])
    removed = Counter(labels.findall(old)) - Counter(labels.findall(new))
    added = Counter(labels.findall(new)) - Counter(labels.findall(old))
    removed_all.update(removed)
    if before != after or removed or added:
        changes.append({'file': path, 'before': dict(before), 'after': dict(after),
                        'removed_labels': dict(removed), 'added_labels': dict(added)})
assert removed_all == Counter({'[Tier 1 — Axiom of Presence]': 3}), removed_all

diff = git('diff', '--unified=0', args.baseline, '--', 'content/', 'GCT_Physics_Engine/')
forbidden = re.compile(
    r'\b(?:previously|legacy|pre-audit|post-audit|hotfix|sprint)\b|'
    r'\b(?:19|20)\d{2}-\d{2}-\d{2}\b|'
    r'\b(?:per (?:audit|reviewer)|audit note|round[- ]\d+|finding [A-Z]+\d+)\b', re.I)
violations = [line for line in diff.splitlines()
              if line.startswith('+') and not line.startswith('+++') and forbidden.search(line)]
assert not violations, violations
word_diff = git('diff', '--word-diff=porcelain', '--unified=0', args.baseline,
                '--', 'content/', 'GCT_Physics_Engine/')
process_terms = re.compile(
    r'\b(?:audit|audited|reviewer|previously|legacy|hotfix|sprint|directive)\b|'
    r'\b(?:19|20)\d{2}-\d{2}-\d{2}\b|'
    r'\b(?:round|phase|bug|finding)[- #]+\d+', re.I)
word_violations = [line for line in word_diff.splitlines()
                   if line.startswith('+') and not line.startswith('+++')
                   and process_terms.search(line)]
assert not word_violations, word_violations
out = ROOT/'_publish_prep'
with (out/'TIER0_CENSUS.csv').open('w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['file', 'tier', 'before', 'after', 'delta'])
    writer.writerows(rows)
summary = {'baseline': args.baseline, 'files_checked': len(paths),
           'before': dict(total_before), 'after': dict(total_after),
           'changes': changes, 'removed_labels': dict(removed_all),
           'law8_added_line_violations': violations,
           'law8_added_word_violations': word_violations}
(out/'TIER0_CENSUS.json').write_text(json.dumps(summary, indent=2)+'\n', encoding='utf-8')
print(json.dumps(summary, indent=2))
