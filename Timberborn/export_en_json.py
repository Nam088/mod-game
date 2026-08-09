import os
import json
import csv

def extract_en_timberborn():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    original_dir = os.path.join(base_dir, "Original_Localizations")
    output_en = os.path.join(base_dir, "en.json")
    
    if not os.path.exists(original_dir):
        print(f"Error: {original_dir} does not exist.")
        return

    en_dict = {}
    
    for file_name in ["enUS.csv", "enUS_names.csv", "enUS_donottranslate.csv", "enUS_wip.csv"]:
        csv_p = os.path.join(original_dir, file_name)
        if os.path.exists(csv_p):
            with open(csv_p, mode="r", encoding="utf-8-sig") as f:
                reader = csv.reader(f)
                count = 0
                for row in reader:
                    if row and len(row) >= 2:
                        key = row[0].strip()
                        val = row[1].strip()
                        if key and key != "ID":
                            en_dict[key] = val
                            count += 1
                print(f"Extracted from {file_name}: {count} keys")

    with open(output_en, "w", encoding="utf-8") as f:
        json.dump(en_dict, f, ensure_ascii=False, indent=2)

    print(f"\nSuccessfully extracted all Timberborn English keys to: {output_en} ({len(en_dict)} keys total)!")

if __name__ == "__main__":
    extract_en_timberborn()
