import json

with open('translations/06_Quests_Events_Story.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Total entries in Phase 6: {len(data)}")

# Let's inspect category distribution or key prefix distribution
key_prefixes = {}
for i, item in enumerate(data):
    prefix = item['key'].split('.')[0]
    key_prefixes[prefix] = key_prefixes.get(prefix, 0) + 1

print("\nKey prefixes:")
for k, v in sorted(key_prefixes.items(), key=lambda x: x[1], reverse=True):
    print(f"  {k}: {v}")

print("\nSample checkpoints:")
checkpoints = [0, 100, 200, 330, 335, 340, 500, 670, 675, 680, 800, 1000]
for cp in checkpoints:
    if cp < len(data):
        item = data[cp]
        print(f"Index {cp:04d} | ID:{item['id']} | Key: {item['key']} | EN: {item['source_en'][:60]}")
