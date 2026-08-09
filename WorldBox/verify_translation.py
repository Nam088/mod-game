"""
WorldBox Translation Validator
Usage:
  python verify_translation.py

This script compares each Vietnamese translation file with its English baseline
to detect:
  - Missing keys (keys in EN that are missing in VN)
  - Extra keys (keys in VN that don't exist in EN)
  - Untranslated keys (keys where VN value equals EN value)
"""
import os
import json
import sys

# Force UTF-8 stdout
sys.stdout.reconfigure(encoding='utf-8')

WORKSPACE_DIR = os.path.dirname(os.path.abspath(__file__))
EN_DIR = os.path.join(WORKSPACE_DIR, "extracted_locales", "en")
VN_DIR = os.path.join(WORKSPACE_DIR, "extracted_locales", "vn")

def main():
    print("=== WorldBox Translation Verification Tool ===")
    
    if not os.path.exists(EN_DIR) or not os.path.exists(VN_DIR):
        print("ERROR: Missing extracted_locales/en or extracted_locales/vn directories!")
        return

    en_files = {f for f in os.listdir(EN_DIR) if f.endswith('.json')}
    vn_files = {f for f in os.listdir(VN_DIR) if f.endswith('.json')}

    # Check for missing files
    missing_files = en_files - vn_files
    if missing_files:
        print(f"WARNING: The following {len(missing_files)} translation files are missing in VN:")
        for f in sorted(missing_files):
            print(f"  - {f}")
        print()

    total_en_keys = 0
    total_translated = 0
    total_untranslated = 0
    total_missing_keys = 0
    total_extra_keys = 0

    issues_found = False

    print(f"{'File Name':<30} | {'Total':<6} | {'Done':<6} | {'Todo':<6} | {'Missing':<7} | {'Extra':<5}")
    print("-" * 75)

    for file in sorted(en_files):
        if file not in vn_files:
            continue
            
        en_path = os.path.join(EN_DIR, file)
        vn_path = os.path.join(VN_DIR, file)
        
        with open(en_path, 'r', encoding='utf-8') as f:
            en_data = json.load(f)
        with open(vn_path, 'r', encoding='utf-8') as f:
            vn_data = json.load(f)

        en_keys = set(en_data.keys())
        vn_keys = set(vn_data.keys())

        missing = en_keys - vn_keys
        extra = vn_keys - en_keys
        
        untranslated = []
        translated = 0
        
        for k in en_keys:
            if k in vn_data:
                if vn_data[k] == en_data[k]:
                    untranslated.append(k)
                else:
                    translated += 1

        total_en_keys += len(en_keys)
        total_translated += translated
        total_untranslated += len(untranslated)
        total_missing_keys += len(missing)
        total_extra_keys += len(extra)

        file_status = f"{file:<30} | {len(en_keys):<6} | {translated:<6} | {len(untranslated):<6} | {len(missing):<7} | {len(extra):<5}"
        
        # Highlight files with issues (missing or extra keys)
        if len(missing) > 0 or len(extra) > 0:
            print(f"{file_status} <-- ERROR!")
            issues_found = True
            if len(missing) > 0:
                print(f"    Missing keys (deleted by accident): {sorted(list(missing))[:10]}")
            if len(extra) > 0:
                print(f"    Extra keys (invalid keys): {sorted(list(extra))[:10]}")
        else:
            print(file_status)

    print("-" * 75)
    print(f"{'TOTAL':<30} | {total_en_keys:<6} | {total_translated:<6} | {total_untranslated:<6} | {total_missing_keys:<7} | {total_extra_keys:<5}")
    print("-" * 75)
    
    if issues_found or missing_files:
        print("\n❌ VERIFICATION FAILED: Some keys were deleted by accident or are invalid.")
    else:
        print("\n✅ VERIFICATION PASSED: No keys were deleted or added incorrectly. File structures are perfect.")

if __name__ == "__main__":
    main()
