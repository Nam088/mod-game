import json

with open('translations/06_Quests_Events_Story.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

part_a = data[:335]

with open('tools/phase6a_dump.txt', 'w', encoding='utf-8') as f:
    for i, item in enumerate(part_a):
        f.write(f"[{i:03d}] ID:{item['id']} | KEY: {item['key']}\nEN: {item['source_en']}\n\n")

print(f"Dumped {len(part_a)} items for Phase 6A (indices 0..334)")
