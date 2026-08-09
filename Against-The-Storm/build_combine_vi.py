import json
import os

def combine_vi_ats():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    plugin_dir = os.path.join(base_dir, "ATS_Vietnamese")
    output_file = os.path.join(plugin_dir, "vi.json")
    translation_file = os.path.join(plugin_dir, "vi_translation.json")

    master_dict = {}

    for p in range(1, 18):
        patch_file = os.path.join(plugin_dir, f"vi_patch_{p}_ready.json")
        if os.path.exists(patch_file):
            with open(patch_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                master_dict.update(data)
                print(f"Loaded vi_patch_{p}_ready.json: {len(data)} keys")

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(master_dict, f, ensure_ascii=False, indent=2)

    with open(translation_file, "w", encoding="utf-8") as f:
        json.dump(master_dict, f, ensure_ascii=False, indent=2)

    print(f"\nSuccessfully combined {len(master_dict)} keys into vi.json and vi_translation.json!")

if __name__ == "__main__":
    combine_vi_ats()
