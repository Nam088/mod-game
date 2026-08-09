"""
WorldBox Translation Packager & Installer
Usage:
  python merge_and_copy.py

This script merges all translated files from extracted_locales/vn/ 
(including English fallbacks) and installs them into the active game mods directory.
"""
import os
import json

WORKSPACE_DIR = os.path.dirname(os.path.abspath(__file__))
VN_DIR = os.path.join(WORKSPACE_DIR, "extracted_locales", "vn")
GAME_MOD_VI_JSON = r"C:\Program Files (x86)\Steam\steamapps\common\worldbox\worldbox_Data\StreamingAssets\mods\vi.json"

def main():
    print("=== WorldBox Translation Packager & Installer ===")
    
    if not os.path.exists(VN_DIR):
        print(f"ERROR: Local Vietnamese directory does not exist at {VN_DIR}")
        return

    merged_data = {}
    
    # Sort files to ensure deterministic merging
    for file in sorted(os.listdir(VN_DIR)):
        if file.endswith('.json'):
            filepath = os.path.join(VN_DIR, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                try:
                    data = json.load(f)
                    merged_data.update(data)
                except Exception as e:
                    print(f"  Error reading {file}: {e}")

    print(f"Merged total of {len(merged_data)} keys.")
    
    # Save directly to the game directory
    try:
        os.makedirs(os.path.dirname(GAME_MOD_VI_JSON), exist_ok=True)
        with open(GAME_MOD_VI_JSON, 'w', encoding='utf-8') as f:
            json.dump(merged_data, f, ensure_ascii=False, indent=2, sort_keys=True)
        print(f"SUCCESS: Successfully packaged and installed mod translation to:\n  {GAME_MOD_VI_JSON}")
    except Exception as e:
        print(f"ERROR: Failed to write to game directory: {e}")

if __name__ == "__main__":
    main()
