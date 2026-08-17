import os
import json
import csv

def build_csv():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    trans_dir = os.path.join(base_dir, 'translations')
    output_csv = os.path.join(base_dir, 'Vietnamese.csv')

    # Load master ordering to preserve exact original term order
    master_path = os.path.join(base_dir, 'master_english.json')
    with open(master_path, 'r', encoding='utf-8') as f:
        master_list = json.load(f)

    # Collect all translated terms from JSON modules
    translated_map = {}
    total_loaded = 0
    for file_name in sorted(os.listdir(trans_dir)):
        if file_name.endswith('.json'):
            file_path = os.path.join(trans_dir, file_name)
            with open(file_path, 'r', encoding='utf-8') as f:
                entries = json.load(f)
                for entry in entries:
                    k = entry["key"]
                    vi = entry.get("vi", entry.get("en", ""))
                    t = entry.get("type", 0)
                    translated_map[k] = (t, vi)
                    total_loaded += 1

    print(f"Loaded {total_loaded} entries from JSON files.")

    # Write output CSV (using utf-8-sig for Unity I2 Localization compatibility)
    with open(output_csv, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Key', 'Type', 'Desc', 'Vietnamese'])
        for item in master_list:
            k = item["key"]
            if k in translated_map:
                t, vi = translated_map[k]
            else:
                t = item.get("type", 0)
                vi = item.get("en", "")
            writer.writerow([k, t, "", vi])

    print(f"Successfully generated {output_csv} with {len(master_list)} rows.")
    return output_csv

if __name__ == '__main__':
    build_csv()
