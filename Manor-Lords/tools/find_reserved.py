import os
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')
trans_dir = r"D:\mod-game\Manor-Lords\translations"

for f in sorted(os.listdir(trans_dir)):
    if not f.endswith(".json"): continue
    path = os.path.join(trans_dir, f)
    with open(path, "r", encoding="utf-8") as fp:
        data = json.load(fp)
    for item in data:
        vi = str(item.get("vi", ""))
        en = str(item.get("en", ""))
        key = str(item.get("key", ""))
        if "dành riêng" in vi.lower() or "reserve" in en.lower():
            print(f"{f} [{key}] -> EN: {en} | VI: {vi}")
