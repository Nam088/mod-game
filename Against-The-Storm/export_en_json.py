import json
import os

def export_en_ats():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    patches_dir = os.path.join(base_dir, "Localization_Patches")
    output_en = os.path.join(patches_dir, "en.json")
    
    if not os.path.exists(patches_dir):
        print(f"Error: {patches_dir} does not exist.")
        return

    master_en = {}
    for p in range(1, 18):
        patch_file = os.path.join(patches_dir, f"patch_{p}.json")
        if os.path.exists(patch_file):
            with open(patch_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                master_en.update(data)
                print(f"Loaded patch_{p}.json: {len(data)} keys")

    with open(output_en, "w", encoding="utf-8") as f:
        json.dump(master_en, f, ensure_ascii=False, indent=2)

    print(f"\nSuccessfully exported master {output_en} with {len(master_en)} English keys!")

if __name__ == "__main__":
    export_en_ats()
