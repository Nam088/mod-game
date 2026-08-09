"""
WorldBox Locale Extractor (Optimized Single Script)
Requirements: pip install UnityPy

Usage:
  python extract_locales.py

This script automatically extracts the English (en) and Vietnamese (vn) locale files 
from the game assets, maps them correctly using the ResourceManager, and creates 
a 'needs_translation.json' file containing all untranslated keys.
"""
import UnityPy
import os
import json
import sys

# Force UTF-8 stdout
sys.stdout.reconfigure(encoding='utf-8')

GAME_PATH = r"C:\Program Files (x86)\Steam\steamapps\common\worldbox\worldbox_Data"
WORKSPACE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(WORKSPACE_DIR, "extracted_locales")

os.makedirs(OUTPUT_DIR, exist_ok=True)

def main():
    print("=== WorldBox Optimized Locale Extractor ===")
    
    # 1. Read ResourceManager from globalgamemanagers
    ggm_path = os.path.join(GAME_PATH, "globalgamemanagers")
    if not os.path.exists(ggm_path):
        print(f"ERROR: Could not find game files at {ggm_path}")
        return
        
    print("Reading ResourceManager mapping...")
    ggm_env = UnityPy.load(ggm_path)
    locales_map = {}  # path_id -> resource_path
    
    for obj in ggm_env.objects:
        if obj.type.name == "ResourceManager":
            data = obj.read()
            for path, pptr in data.m_Container:
                if path.startswith('locales/'):
                    locales_map[pptr.m_PathID] = path
                    
    print(f"Loaded {len(locales_map)} locales paths.")
    if not locales_map:
        print("ERROR: No locale paths found!")
        return

    # 2. Read resources.assets and extract files
    resources_path = os.path.join(GAME_PATH, "resources.assets")
    print(f"Loading game resources from {resources_path}...")
    resources_env = UnityPy.load(resources_path)
    
    extracted_count = 0
    languages = set()
    locale_data = {}  # lang -> {filename: data}
    
    for obj in resources_env.objects:
        if obj.path_id in locales_map:
            resource_path = locales_map[obj.path_id]
            if obj.type.name == "TextAsset":
                data = obj.read()
                text = data.text if hasattr(data, 'text') else data.m_Script
                if isinstance(text, bytes):
                    text = text.decode('utf-8')
                
                try:
                    js_data = json.loads(text)
                    if isinstance(js_data, dict):
                        parts = resource_path.split('/')
                        lang = parts[1] if len(parts) >= 3 else "unknown"
                        filename = parts[2] if len(parts) >= 3 else parts[-1]
                        
                        languages.add(lang)
                        if lang not in locale_data:
                            locale_data[lang] = {}
                        locale_data[lang][filename] = js_data
                        
                        # Save individual file
                        lang_dir = os.path.join(OUTPUT_DIR, lang)
                        os.makedirs(lang_dir, exist_ok=True)
                        with open(os.path.join(lang_dir, f"{filename}.json"), 'w', encoding='utf-8') as f:
                            json.dump(js_data, f, ensure_ascii=False, indent=2)
                        
                        extracted_count += 1
                except Exception as e:
                    print(f"Error parsing {resource_path}: {e}")

    print(f"Successfully extracted {extracted_count} files across {len(languages)} languages.")
    
    # 3. Create merged files for EN and VN
    en_merged = {}
    vn_merged = {}
    
    for lang in ['en', 'vn']:
        if lang in locale_data:
            merged = {}
            for filename, data in locale_data[lang].items():
                merged.update(data)
            
            if lang == 'en':
                en_merged = merged
            else:
                vn_merged = merged
                
            merged_file = os.path.join(OUTPUT_DIR, f"merged_{lang}.json")
            with open(merged_file, 'w', encoding='utf-8') as f:
                json.dump(merged, f, ensure_ascii=False, indent=2, sort_keys=True)
            print(f"Created merged_{lang}.json with {len(merged)} keys")

    # 4. Generate comparison and untranslated keys
    if en_merged and vn_merged:
        missing = sorted(k for k in en_merged if k not in vn_merged)
        untranslated = sorted(k for k in en_merged if k in vn_merged and vn_merged[k] == en_merged[k])
        translated = sorted(k for k in en_merged if k in vn_merged and vn_merged[k] != en_merged[k])
        
        print(f"\n=== Translation Status ===")
        print(f"  Total EN keys: {len(en_merged)}")
        print(f"  Total VN keys: {len(vn_merged)}")
        print(f"  Translated:    {len(translated)} ({100*len(translated)/len(en_merged):.1f}%)")
        print(f"  Untranslated:  {len(untranslated)} ({100*len(untranslated)/len(en_merged):.1f}%)")
        
        needs = {k: en_merged[k] for k in sorted(untranslated + missing)}
        needs_file = os.path.join(OUTPUT_DIR, "needs_translation.json")
        with open(needs_file, 'w', encoding='utf-8') as f:
            json.dump(needs, f, ensure_ascii=False, indent=2, sort_keys=True)
            
        print(f"Created needs_translation.json ({len(needs)} keys) -> Translate these!")

if __name__ == "__main__":
    main()
