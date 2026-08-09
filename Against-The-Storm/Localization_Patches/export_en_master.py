import json
import os

PATCHES_DIR = r"C:\Users\nam\Downloads\Compressed\Against-The-Storm-AnkerGames\Localization_Patches"
OUTPUT_FILE = r"C:\Users\nam\Downloads\Compressed\Against-The-Storm-AnkerGames\Localization_Patches\en.json"

master_en = {}

for p in range(1, 18):
    patch_path = os.path.join(PATCHES_DIR, f"patch_{p}.json")
    if os.path.exists(patch_path):
        with open(patch_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            master_en.update(data)
            print(f"Loaded patch_{p}.json: {len(data)} keys")

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(master_en, f, ensure_ascii=False, indent=2)

print(f"\nSuccessfully generated master {OUTPUT_FILE} with total {len(master_en)} English keys!")
