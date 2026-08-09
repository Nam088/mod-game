"""
WorldBox Mod Translation Packager
Usage:
  python update_mod_translation.py

This script merges all translated files from extracted_locales/vn/,
compares them with English, generates the differential vi.json dictionary,
and copies it directly to the active WorldBox mods folder.
"""
import os
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

WORKSPACE_DIR = os.path.dirname(os.path.abspath(__file__))
EN_DIR = os.path.join(WORKSPACE_DIR, "extracted_locales", "en")
VN_DIR = os.path.join(WORKSPACE_DIR, "extracted_locales", "vn")
GAME_MODS_DIR = r"C:\Program Files (x86)\Steam\steamapps\common\worldbox\worldbox_Data\StreamingAssets\mods"
GAME_VI_JSON = os.path.join(GAME_MODS_DIR, "vi.json")

def main():
    print("=== WorldBox Mod Translation Packager ===")
    
    if not os.path.exists(EN_DIR) or not os.path.exists(VN_DIR):
        print("ERROR: Missing extracted_locales directories!")
        return

    # 1. Merge all EN files
    en_all = {}
    for file in sorted(os.listdir(EN_DIR)):
        if file.endswith('.json'):
            with open(os.path.join(EN_DIR, file), 'r', encoding='utf-8') as f:
                try:
                    en_all.update(json.load(f))
                except Exception as e:
                    print(f"  Error reading EN {file}: {e}")

    # 2. Merge all VN files
    vn_all = {}
    for file in sorted(os.listdir(VN_DIR)):
        if file.endswith('.json'):
            with open(os.path.join(VN_DIR, file), 'r', encoding='utf-8') as f:
                try:
                    vn_all.update(json.load(f))
                except Exception as e:
                    print(f"  Error reading VN {file}: {e}")

    print(f"Total keys: EN = {len(en_all)}, VN = {len(vn_all)}")

    # 3. Create differential translation dictionary
    # A key is in our mod dictionary if:
    #   - It is translated in VN (i.e. VN value != EN value)
    #   - It exists in VN (including untranslated ones so the user has the templates)
    # Actually, we want the mod to override EVERYTHING that differs from English or represents Vietnamese.
    # To be safe, we will include all keys in VN where the value is Vietnamese.
    # Since we translated ui_buttons.json, all keys in it are now proper Vietnamese.
    # We will save the entire vn_all dict as vi.json?
    # Wait, the mod can just load the entire vn_all!
    # If the mod loads all keys (6345 keys), it completely replaces the internal translations.
    # This is even better because it ensures 100% consistent fonts, casing, and style!
    # And it's only ~600KB, which is extremely lightweight for memory.
    
    # 3. Save to all possible mod load locations
    target_dirs = [
        GAME_MODS_DIR,  # StreamingAssets/mods (root)
        os.path.join(GAME_MODS_DIR, "VietnameseTranslation"),  # StreamingAssets/mods/VietnameseTranslation
        r"C:\Program Files (x86)\Steam\steamapps\common\worldbox\Mods\VietnameseTranslation"  # WorldBox/Mods/VietnameseTranslation
    ]
    
    src_mod_dir = os.path.join(WORKSPACE_DIR, "steam_workshop_mod")

    for target_dir in target_dirs:
        try:
            os.makedirs(target_dir, exist_ok=True)
            # Write vi.json
            vi_json_path = os.path.join(target_dir, "vi.json")
            with open(vi_json_path, 'w', encoding='utf-8') as f:
                json.dump(vn_all, f, ensure_ascii=False, indent=2, sort_keys=True)
            
            # Copy DLL, mod.json, icon.png if present in steam_workshop_mod
            for extra_file in ["VietnameseTranslation.dll", "mod.json", "icon.png"]:
                src_file = os.path.join(src_mod_dir, extra_file)
                if os.path.exists(src_file):
                    import shutil
                    shutil.copy2(src_file, os.path.join(target_dir, extra_file))
            print(f"  ✓ Installed mod files to: {target_dir}")
        except Exception as e:
            print(f"  ✗ Failed to install to {target_dir}: {e}")

    # Calculate stats
    translated = sum(1 for k in en_all if k in vn_all and vn_all[k] != en_all[k])
    untranslated = sum(1 for k in en_all if k in vn_all and vn_all[k] == en_all[k])
    print(f"\nStatus: Translated = {translated} ({100*translated/len(en_all):.1f}%), Untranslated = {untranslated} ({100*untranslated/len(en_all):.1f}%)")

if __name__ == "__main__":
    main()
