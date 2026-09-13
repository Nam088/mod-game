import json

with open('translations/04_Mice_Traits_Thoughts.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

with open('tools/phase4_dump.txt', 'w', encoding='utf-8') as f:
    for i, item in enumerate(data):
        f.write(f"[{i:03d}] ID:{item['id']} | KEY: {item['key']}\nEN: {item['source_en']}\n\n")

print(f"Successfully dumped {len(data)} Phase 4 entries to tools/phase4_dump.txt")
