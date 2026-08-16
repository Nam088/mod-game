import os
import json
import re

trans_dir = r"D:\mod-game\Manor-Lords\translations"
files = sorted([f for f in os.listdir(trans_dir) if f.endswith(".json")])

print(f"Total translation files: {len(files)}")

issues = []
file_stats = []

for f in files:
    path = os.path.join(trans_dir, f)
    with open(path, "r", encoding="utf-8") as fp:
        try:
            data = json.load(fp)
        except Exception as e:
            issues.append(f"[{f}] JSON Parse Error: {e}")
            continue

    total_strings = len(data)
    empty_strings = 0

    for i, item in enumerate(data):
        en = item.get("en", "")
        vi = item.get("vi", "")

        if not vi and en:
            empty_strings += 1
            issues.append(f"[{f} #{i}] Empty VI for key: {item.get('key')}")

        # Check placeholders like {playerName}, {homeRegion}
        en_placeholders = set(re.findall(r"\{[a-zA-Z0-9_]+\}", en))
        vi_placeholders = set(re.findall(r"\{[a-zA-Z0-9_]+\}", vi))
        # Exclude {br} which is just formatting line break
        en_p = {p for p in en_placeholders if p.lower() != "{br}"}
        vi_p = {p for p in vi_placeholders if p.lower() != "{br}"}
        if en_p != vi_p:
            issues.append(f"[{f} #{i} - {item.get('key')}] Placeholder mismatch: EN {en_p} vs VI {vi_p}")

        # Check img tags
        en_img_ids = set(re.findall(r'id="([^"]+)"', en))
        vi_img_ids = set(re.findall(r'id="([^"]+)"', vi))
        if en_img_ids != vi_img_ids:
            issues.append(f"[{f} #{i} - {item.get('key')}] Image tag mismatch: EN {en_img_ids} vs VI {vi_img_ids}")

    file_stats.append({
        "file": f,
        "count": total_strings,
        "empty": empty_strings
    })

print("\n--- SUMMARY CHECKLIST ---")
for s in file_stats:
    print(f"{s['file']:<42} : {s['count']:>4} strings | Empty: {s['empty']}")

if issues:
    print(f"\n--- ISSUES FOUND ({len(issues)}) ---")
    for iss in issues:
        print(f" - {iss}")
else:
    print("\nALL 39 FILES PASSED COMPLETE INTEGRITY & TAG VALIDATION WITH 0 ERRORS!")
