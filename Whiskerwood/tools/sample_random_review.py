import json
import random

def create_random_sample():
    random.seed(42)  # For reproducible sampling
    
    files = [
        ("01_Core_UI_Menus.json", 12),
        ("02_Buildings_Logistics.json", 12),
        ("03_Resources_Items_Tech.json", 12),
        ("04_Mice_Traits_Thoughts.json", 12),
        ("05_Nautical_Exploration_World.json", 12),
        ("06_Quests_Events_Story.json", 15),
    ]
    
    samples = []
    
    for filename, count in files:
        filepath = f"translations/{filename}"
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        selected = random.sample(data, min(count, len(data)))
        for item in selected:
            samples.append({
                "file": filename,
                "id": item["id"],
                "key": item["key"],
                "source_en": item["source_en"],
                "target_vi": item["target_vi"]
            })
            
    # Write to a clean readable text file for the QA subagent
    with open("tools/random_review_sample.txt", "w", encoding="utf-8") as out:
        out.write(f"# WHISKERWOOD RANDOM SAMPLE AUDIT SET ({len(samples)} STRINGS)\n\n")
        for i, s in enumerate(samples, 1):
            out.write(f"[{i:02d}] File: {s['file']} | ID: {s['id']} | Key: {s['key']}\n")
            out.write(f"EN: {s['source_en']}\n")
            out.write(f"VI: {s['target_vi']}\n\n")
            
    print(f"Generated random sample of {len(samples)} strings into tools/random_review_sample.txt")

if __name__ == '__main__':
    create_random_sample()
