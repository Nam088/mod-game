import json

json_path = r"D:\code\mod-game\Whiskerwood\translations\02_Buildings_Logistics.json"
dump_path = r"D:\code\mod-game\Whiskerwood\tools\phase2_dump.txt"

with open(json_path, "r", encoding="utf-8") as f:
    items = json.load(f)

print(f"Total entries in Phase 2: {len(items)}")

with open(dump_path, "w", encoding="utf-8") as out:
    for idx, it in enumerate(items):
        out.write(f"[{idx:03d}] KEY: {it['key']}\nEN: {it['source_en']}\n---\n")

print("Dumped all 409 items to phase2_dump.txt")
