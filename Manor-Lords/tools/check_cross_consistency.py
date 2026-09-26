import json
import glob
import os
import re
from collections import defaultdict
import sys

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

folder = os.path.join(os.path.dirname(__file__), "..", "translations")
files = glob.glob(os.path.join(folder, "*.json"))
en_to_vi = defaultdict(list)

for f in sorted(files):
    fname = os.path.basename(f)
    with open(f, "r", encoding="utf-8") as fp:
        data = json.load(fp)
        for item in data:
            en = item.get("en", "").strip()
            vi = item.get("vi", "").strip()
            key = item.get("key", "")
            if en and vi:
                en_to_vi[en.lower()].append((fname, key, en, vi))

print("=== CROSS-TABLE INCONSISTENCIES (EXACT MATCHES) ===")
count = 0
for en, occ in sorted(en_to_vi.items()):
    vis = set(x[3] for x in occ)
    if len(vis) > 1 and len(en) > 2 and not re.search(r'[\.\?!]$', en) and len(occ) > 1:
        # Check if the English term is a short noun/phrase (<= 4 words)
        if len(en.split()) <= 4:
            count += 1
            print(f'[{count}] EN: "{occ[0][2]}"')
            for v in vis:
                matching = [f"{x[0]}:{x[1]}" for x in occ if x[3] == v]
                print(f'      -> "{v}" ({len(matching)}x) [{matching[0]}]')

