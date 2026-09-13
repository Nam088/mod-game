import json
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TRANS_DIR = os.path.join(PROJECT_ROOT, "translations")

def extract_placeholders(text):
    return re.findall(r"\{[^}]+\}", text)

def extract_tags(text):
    return re.findall(r"<[^>]+>", text)

def verify_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        entries = json.load(f)

    errors = []
    warnings = []
    translated_count = 0
    total_count = len(entries)

    for entry in entries:
        en = entry.get("source_en", "")
        vi = entry.get("target_vi", "").strip()
        key = entry.get("key", f"ID_{entry.get('id')}")

        if not vi:
            continue

        translated_count += 1

        # 1. Placeholders
        en_phs = sorted(extract_placeholders(en))
        vi_phs = sorted(extract_placeholders(vi))
        if en_phs != vi_phs:
            errors.append(f"[{key}] Mismatched placeholders! EN: {en_phs} vs VI: {vi_phs}")

        # 2. Rich Text tags
        en_tags = sorted(extract_tags(en))
        vi_tags = sorted(extract_tags(vi))
        if en_tags != vi_tags:
            errors.append(f"[{key}] Mismatched XML/RichText tags! EN: {en_tags} vs VI: {vi_tags}")

        # 3. Newlines
        en_nls = en.count("\n")
        vi_nls = vi.count("\n")
        if en_nls != vi_nls:
            warnings.append(f"[{key}] Mismatched newline count! EN: {en_nls} vs VI: {vi_nls}")

        # 4. Length Guard for short UI strings
        if len(en) > 0 and len(en) < 30 and len(vi) > len(en) * 2.2:
            warnings.append(f"[{key}] UI length warning! EN({len(en)}): '{en}' -> VI({len(vi)}): '{vi}'")

    return total_count, translated_count, errors, warnings

def main():
    print("==================================================")
    print("   WHISKERWOOD TRANSLATION VERIFIER & AUDIT       ")
    print("==================================================")

    json_files = [f for f in sorted(os.listdir(TRANS_DIR)) if f.endswith(".json") and not f.endswith("Master.json")]
    
    grand_total = 0
    grand_translated = 0
    all_errors = []
    all_warnings = []

    for jf in json_files:
        fpath = os.path.join(TRANS_DIR, jf)
        total, trans, errors, warnings = verify_file(fpath)
        grand_total += total
        grand_translated += trans
        all_errors.extend(errors)
        all_warnings.extend(warnings)
        
        pct = (trans / total * 100) if total > 0 else 0
        print(f"[{jf:<35}] {trans:4d}/{total:4d} ({pct:5.1f}%) | Errors: {len(errors):2d}, Warnings: {len(warnings):2d}")

    grand_pct = (grand_translated / grand_total * 100) if grand_total > 0 else 0
    print("--------------------------------------------------")
    print(f"TOTAL PROGRESS: {grand_translated}/{grand_total} ({grand_pct:.2f}%)")
    print(f"TOTAL ERRORS  : {len(all_errors)}")
    print(f"TOTAL WARNINGS: {len(all_warnings)}")
    print("--------------------------------------------------")

    if all_errors:
        print("\nCRITICAL ERRORS:")
        for err in all_errors[:20]:
            print(f" ❌ {err}")
        if len(all_errors) > 20:
            print(f" ... and {len(all_errors) - 20} more errors.")
        sys.exit(1)
    else:
        print("\n✅ ALL TRANSLATION SYNTAX CHECKS PASSED!")

if __name__ == "__main__":
    main()
