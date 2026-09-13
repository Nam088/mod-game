import json

with open(r"D:\code\mod-game\Whiskerwood\translations\01_Core_UI_Menus.json", "r", encoding="utf-8") as f:
    items = json.load(f)

print(f"Total entries in Phase 1: {len(items)}")

with open(r"D:\code\mod-game\Whiskerwood\tools\phase1_dump.txt", "w", encoding="utf-8") as out:
    for idx, it in enumerate(items):
        out.write(f"[{idx:03d}] KEY: {it['key']}\nEN: {it['source_en']}\n---\n")

print("Dumped all 391 items to phase1_dump.txt")
