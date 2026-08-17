import os
import json
import re
import sys

# Ensure UTF-8 stdout on Windows console
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def verify():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    trans_dir = os.path.join(base_dir, 'translations')
    
    total_keys = 0
    total_translated = 0
    total_errors = 0
    total_warnings = 0

    print("=" * 65)
    print("🔍 GOING MEDIEVAL TRANSLATION VERIFICATION & PROGRESS REPORT")
    print("=" * 65)

    module_stats = []

    for file_name in sorted(os.listdir(trans_dir)):
        if not file_name.endswith('.json'):
            continue
        
        file_path = os.path.join(trans_dir, file_name)
        with open(file_path, 'r', encoding='utf-8') as f:
            entries = json.load(f)

        mod_keys = len(entries)
        mod_translated = 0
        mod_errors = 0
        mod_warnings = 0

        for idx, item in enumerate(entries):
            k = item.get("key", "")
            en = item.get("en", "")
            vi = item.get("vi", "")

            # Check if translated (different from en and not empty)
            is_translated = bool(vi and vi.strip() != en.strip())
            if is_translated:
                mod_translated += 1

            # Check 1: Placeholders {0}, {1}, {name}, {item}, etc.
            en_placeholders = sorted(re.findall(r'\{[A-Za-z0-9_]+\}', en))
            vi_placeholders = sorted(re.findall(r'\{[A-Za-z0-9_]+\}', vi))
            if en_placeholders != vi_placeholders:
                print(f"❌ [PLACEHOLDER ERROR] {file_name} -> Key: '{k}'")
                print(f"   EN: {en}")
                print(f"   VI: {vi}")
                print(f"   Expected: {en_placeholders}, Got: {vi_placeholders}")
                mod_errors += 1

            # Check 2: RichText tags <style=...>, <color=...>, <b>, <i>, etc.
            en_tags = sorted(re.findall(r'</?[A-Za-z0-9_=\"#]+>', en))
            vi_tags = sorted(re.findall(r'</?[A-Za-z0-9_=\"#]+>', vi))
            if len(en_tags) != len(vi_tags):
                print(f"⚠️  [TAG WARNING] {file_name} -> Key: '{k}'")
                print(f"   EN: {en}")
                print(f"   VI: {vi}")
                print(f"   Expected tags: {en_tags}, Got: {vi_tags}")
                mod_warnings += 1

            # Check 3: Escape sequences count (\n, \t)
            if en.count('\n') != vi.count('\n'):
                print(f"⚠️  [NEWLINE MISMATCH] {file_name} -> Key: '{k}'")
                print(f"   EN newlines: {en.count(chr(10))}, VI newlines: {vi.count(chr(10))}")
                mod_warnings += 1

            # Check 4: UI Length Guard (> 2.0x length of EN string for short UI elements)
            if len(en) > 0 and len(en) < 30 and len(vi) > len(en) * 2.2 and is_translated:
                print(f"⚠️  [UI LENGTH OVERFLOW] {file_name} -> Key: '{k}'")
                print(f"   EN ({len(en)}): {en}")
                print(f"   VI ({len(vi)}): {vi}")
                mod_warnings += 1

        pct = (mod_translated / mod_keys * 100) if mod_keys > 0 else 0
        module_stats.append((file_name, mod_keys, mod_translated, pct, mod_errors, mod_warnings))
        total_keys += mod_keys
        total_translated += mod_translated
        total_errors += mod_errors
        total_warnings += mod_warnings

    print("\n📊 SUMMARY BY MODULE:")
    print("-" * 65)
    print(f"{'Module Name':<35} | {'Total':<6} | {'Done':<6} | {'Progress':<8}")
    print("-" * 65)
    for name, m_tot, m_done, m_pct, errs, warns in module_stats:
        status_symbol = "🟢" if m_pct >= 99.9 else ("🟡" if m_pct > 0 else "⚪")
        print(f"{status_symbol} {name:<33} | {m_tot:<6} | {m_done:<6} | {m_pct:>6.1f}%")
    print("-" * 65)
    overall_pct = (total_translated / total_keys * 100) if total_keys > 0 else 0
    print(f"🎯 OVERALL PROGRESS: {total_translated} / {total_keys} keys ({overall_pct:.2f}%)")
    print(f"❌ Total Errors: {total_errors}")
    print(f"⚠️  Total Warnings: {total_warnings}")
    print("=" * 65)

    return total_errors == 0

if __name__ == '__main__':
    verify()
