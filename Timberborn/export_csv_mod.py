import os
import json
import csv

def export_json_to_csv_timberborn():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    json_vi_path = os.path.join(base_dir, "vi.json")
    
    mod_loca_dir = os.path.join(base_dir, "Mods", "VietnameseLanguage", "Localizations")
    os.makedirs(mod_loca_dir, exist_ok=True)
    csv_vi_path = os.path.join(mod_loca_dir, "viVN.csv")
    
    if not os.path.exists(json_vi_path):
        print(f"Notice: {json_vi_path} not found. Creating mod CSV structure from existing Localizations.")
        return

    with open(json_vi_path, "r", encoding="utf-8") as f:
        vi_dict = json.load(f)

    with open(csv_vi_path, mode="w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        for key, val in vi_dict.items():
            writer.writerow([key, val])

    print(f"Successfully exported {len(vi_dict)} keys from vi.json to {csv_vi_path} CSV Mod File!")

if __name__ == "__main__":
    export_json_to_csv_timberborn()
