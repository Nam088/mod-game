import os
import csv
import json
import zipfile

def extract_en_directly_from_game(game_dir=r"C:\Users\nam\Downloads\Compressed\Timberborn-AnkerGames"):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_csv = os.path.join(base_dir, "enUS_extracted.csv")
    output_json = os.path.join(base_dir, "en.json")
    
    zip_path = os.path.join(game_dir, "Timberborn", "Timberborn_Data", "StreamingAssets", "Modding", "Localizations.zip")
    
    if not os.path.exists(zip_path):
        print(f"Error: {zip_path} not found!")
        return

    en_dict = {}
    
    print(f"Extracting English files directly from game zip: {zip_path}")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        for file_name in ["enUS.csv", "enUS_names.csv", "enUS_donottranslate.csv", "enUS_wip.csv"]:
            if file_name in zip_ref.namelist():
                content = zip_ref.read(file_name).decode("utf-8-sig")
                lines = content.splitlines()
                reader = csv.reader(lines)
                count = 0
                for row in reader:
                    if row and len(row) >= 2:
                        key = row[0].strip()
                        val = row[1].strip()
                        if key and key != "ID":
                            en_dict[key] = val
                            count += 1
                print(f"Extracted from {file_name}: {count} keys")

    # Save to en.json
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(en_dict, f, ensure_ascii=False, indent=2)

    # Save to enUS_extracted.csv
    with open(output_csv, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Text"])
        for k, v in en_dict.items():
            writer.writerow([k, v])

    print(f"\nSuccessfully extracted all Timberborn English keys!")
    print(f"  -> JSON: {output_json} ({len(en_dict)} keys)")
    print(f"  -> CSV:  {output_csv} ({len(en_dict)} keys)")

if __name__ == "__main__":
    extract_en_directly_from_game()
